import argparse

def cuboid_volume(length, width, height):
    return length * width * height

def main():
    parser = argparse.ArgumentParser(description="Calculate the volume of a cuboid")

    parser.add_argument("length", type=float, help="Length of the cuboid")
    parser.add_argument("width", type=float, help="Width of the cuboid")
    parser.add_argument("height", type=float, help="Height of the cuboid")

    args = parser.parse_args()

    volume = cuboid_volume(args.length, args.width, args.height)
    print(volume)

if __name__ == "__main__":
    main()
 