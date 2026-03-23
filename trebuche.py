import argparse

import math

import sys

import matplotlib.pyplot as plt

 

# ----------------------------

# Physics

# ----------------------------

 

def steel_ball_mass_kg(diameter_mm: float, density_kg_m3: float = 7850.0) -> float:

    """Mass of a steel sphere from diameter (mm)."""

    r_m = (diameter_mm / 1000.0) / 2.0

    volume = (4.0 / 3.0) * math.pi * (r_m ** 3)

    return density_kg_m3 * volume

 

def potential_energy_j(counterweight_kg: float, drop_m: float, g: float) -> float:

    """Gravitational potential energy m g h (J)."""

    return counterweight_kg * g * drop_m

 

def projectile_speed_m_s(energy_j: float, projectile_kg: float, efficiency: float) -> float:

    """

    v from E = 1/2 m v^2, but we only give the projectile a fraction of energy (efficiency).

    """

    useful = max(0.0, efficiency) * max(0.0, energy_j)

    if projectile_kg <= 0:

        return 0.0

    return math.sqrt((2.0 * useful) / projectile_kg)

 

def lever_tip_speed(arm_tip_speed: float, a_m: float, b_m: float) -> float:

    """

    Simple lever idea:

    If you know some reference speed at the short end, tip speed scales as b/a.

    Here we treat arm_tip_speed as coming from energy already, so this function

    is mainly used to apply a lever scaling knob if desired.

    """

    if a_m <= 0:

        return 0.0

    return arm_tip_speed * (b_m / a_m)

 

def sling_radius_m(b_m: float, s_m: float) -> float:

    """Effective radius to projectile at release (very simplified)."""

    return max(0.0, b_m + s_m)

 

def projectile_range_m(v_m_s: float, angle_deg: float, g: float) -> float:

    """Range on level ground: R = v^2 sin(2θ)/g"""

    theta = math.radians(angle_deg)

    return (v_m_s ** 2) * math.sin(2.0 * theta) / g

 

# ----------------------------

# Model (simple learning model)

# ----------------------------

 

def model_release_speed(

    cw_kg: float,

    drop_m: float,

    a_m: float,

    b_m: float,

    sling_m: float,

    projectile_kg: float,

    g: float,

    efficiency: float,

    use_lever_scaling: bool

) -> float:

    """

    A simple GCSE-friendly speed estimate:

 

    1) Counterweight energy: E = M g h

    2) Give projectile a fraction: E_proj = efficiency * E

    3) Convert to a base speed from energy: v_base = sqrt(2 E_proj / m_projectile)

    4) Optionally apply lever ratio scaling (b/a) as a learning knob.

    5) Optionally scale with sling radius relative to arm length:

       v ~ v_base * ( (b+s) / b )  (keeps it simple, shows sling effect)

 

    Note: This is not a rigorous dynamics model — it’s a teaching model.

    """

    E = potential_energy_j(cw_kg, drop_m, g)

    v_base = projectile_speed_m_s(E, projectile_kg, efficiency)

 

    # Sling effect: longer radius means higher linear speed for similar rotation.

    # Multiply by (b+s)/b. If b=0, just skip.

    if b_m > 0:

        sling_factor = sling_radius_m(b_m, sling_m) / b_m

    else:

        sling_factor = 1.0

 

    v = v_base * sling_factor

 

    # Lever factor (optional): shows why b/a matters.

    if use_lever_scaling:

        if a_m > 0:

            v *= (b_m / a_m)

 

    return v

 

# ----------------------------

# CLI + plotting

# ----------------------------

 

def parse_args(argv):

    p = argparse.ArgumentParser(

        description="GCSE Trebuchet Maths CLI (Energy + Lever + Sling + Projectile Range)"

    )

 

    # Launch object

    p.add_argument("--diameter-mm", type=float, default=15.0, help="Ball diameter in mm (default: 15)")

    p.add_argument("--density", type=float, default=7850.0, help="Steel density kg/m^3 (default: 7850)")

    p.add_argument("--g", type=float, default=9.8, help="Gravity m/s^2 (default: 9.8)")

 

    # Trebuchet parameters

    p.add_argument("--cw-kg", type=float, default=2.0, help="Counterweight mass in kg (default: 2.0)")

    p.add_argument("--drop-m", type=float, default=0.30, help="Counterweight drop height in m (default: 0.30)")

    p.add_argument("--a-m", type=float, default=0.10, help="Short arm length a in m (default: 0.10)")

    p.add_argument("--b-m", type=float, default=0.40, help="Long arm length b in m (default: 0.40)")

    p.add_argument("--sling-m", type=float, default=0.35, help="Sling length s in m (default: 0.35)")

 

    # Real-world losses

    p.add_argument("--eff", type=float, default=0.35,

                   help="Efficiency 0..1 (default: 0.35). 0.2-0.5 is typical for a simple model.")

    p.add_argument("--use-lever-scaling", action="store_true",

                   help="If set, multiplies speed by b/a (educational knob).")

 

    # Plot controls

    p.add_argument("--angle-deg", type=float, default=45.0, help="Single launch angle in degrees (default: 45)")

    p.add_argument("--plot", action="store_true", help="Plot range vs angle")

    p.add_argument("--plot-sling", action="store_true", help="Plot range vs sling length (uses fixed angle)")

    p.add_argument("--sling-min", type=float, default=0.10, help="Min sling length for plot-sling (m)")

    p.add_argument("--sling-max", type=float, default=0.80, help="Max sling length for plot-sling (m)")

    p.add_argument("--steps", type=int, default=181, help="Steps for plots (default: 181)")

 

    return p.parse_args(argv)

 

def print_summary(args, m_ball):

    lever_ratio = args.b_m / args.a_m if args.a_m > 0 else float("inf")

    E = potential_energy_j(args.cw_kg, args.drop_m, args.g)

    v = model_release_speed(

        cw_kg=args.cw_kg,

        drop_m=args.drop_m,

        a_m=args.a_m,

        b_m=args.b_m,

        sling_m=args.sling_m,

        projectile_kg=m_ball,

        g=args.g,

        efficiency=args.eff,

        use_lever_scaling=args.use_lever_scaling

    )

    R = projectile_range_m(v, args.angle_deg, args.g)

 

    print("\n=== GCSE Trebuchet Maths Summary ===")

    print(f"Ball diameter:        {args.diameter_mm:.1f} mm")

    print(f"Ball mass:            {m_ball*1000:.2f} g")

    print(f"Gravity:              {args.g:.2f} m/s^2")

    print()

    print(f"Counterweight mass:   {args.cw_kg:.2f} kg")

    print(f"Drop height:          {args.drop_m:.2f} m")

    print(f"Potential energy mgh: {E:.2f} J")

    print()

    print(f"Short arm a:          {args.a_m:.3f} m")

    print(f"Long arm b:           {args.b_m:.3f} m")

    print(f"Lever ratio b/a:      {lever_ratio:.2f}x")

    print(f"Sling length s:       {args.sling_m:.3f} m")

    print(f"Effective radius r:   {(args.b_m + args.sling_m):.3f} m (b+s)")

    print()

    print(f"Efficiency:           {args.eff:.2f} (fraction of mgh to projectile)")

    print(f"Use lever scaling:    {args.use_lever_scaling}")

    print()

    print(f"Launch angle:         {args.angle_deg:.1f}°")

    print(f"Estimated speed:      {v:.2f} m/s")

    print(f"Estimated range:      {R:.1f} m (no air resistance)")

    print("===================================\n")

 

def plot_range_vs_angle(args, m_ball):

    angles = [i for i in range(0, 91)]

    v = model_release_speed(

        cw_kg=args.cw_kg,

        drop_m=args.drop_m,

        a_m=args.a_m,

        b_m=args.b_m,

        sling_m=args.sling_m,

        projectile_kg=m_ball,

        g=args.g,

        efficiency=args.eff,

        use_lever_scaling=args.use_lever_scaling

    )

    ranges = [max(0.0, projectile_range_m(v, ang, args.g)) for ang in angles]

 

    plt.figure()

    plt.plot(angles, ranges)

    plt.xlabel("Launch angle (degrees)")

    plt.ylabel("Range (m)")

    plt.title("Range vs launch angle (Simple)")

    plt.grid(True)

 

    # Mark best angle

    best_i = max(range(len(ranges)), key=lambda i: ranges[i])

    plt.scatter([angles[best_i]], [ranges[best_i]])

    plt.text(angles[best_i], ranges[best_i], f"  best ~{angles[best_i]}°", va="bottom")

 

    plt.show()

 

def plot_range_vs_sling(args, m_ball):

    if args.steps < 2:

        raise ValueError("--steps must be >= 2")

 

    s_min = args.sling_min

    s_max = args.sling_max

    if s_max <= s_min:

        raise ValueError("--sling-max must be > --sling-min")

 

    sling_vals = [s_min + (s_max - s_min) * i / (args.steps - 1) for i in range(args.steps)]

    ranges = []

 

    for s in sling_vals:

        v = model_release_speed(

            cw_kg=args.cw_kg,

            drop_m=args.drop_m,

            a_m=args.a_m,

            b_m=args.b_m,

            sling_m=s,

            projectile_kg=m_ball,

            g=args.g,

            efficiency=args.eff,

            use_lever_scaling=args.use_lever_scaling

        )

        R = max(0.0, projectile_range_m(v, args.angle_deg, args.g))

        ranges.append(R)

 

    plt.figure()

    plt.plot(sling_vals, ranges)

    plt.xlabel("Sling length s (m)")

    plt.ylabel("Range (m)")

    plt.title(f"Range vs sling length (angle={args.angle_deg:.0f}°, simple model)")

    plt.grid(True)

 

    best_i = max(range(len(ranges)), key=lambda i: ranges[i])

    plt.scatter([sling_vals[best_i]], [ranges[best_i]])

    plt.text(sling_vals[best_i], ranges[best_i], f"  best ~{sling_vals[best_i]:.2f} m", va="bottom")

 

    plt.show()

 

def main(argv):

    args = parse_args(argv)

 

    m_ball = steel_ball_mass_kg(args.diameter_mm, args.density)

 

    print_summary(args, m_ball)

 

    if args.plot:

        plot_range_vs_angle(args, m_ball)

 

    if args.plot_sling:

        plot_range_vs_sling(args, m_ball)

 

    return 0

 

if __name__ == "__main__":

    raise SystemExit(main(sys.argv[1:]))

 