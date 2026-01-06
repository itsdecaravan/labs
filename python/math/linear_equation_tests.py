from linear_equation_solver import solve_linear, check_solution, solve_many


# Test 1: simple integer solution
x = solve_linear(2, 4)
assert x == -2
assert check_solution(2, 4, x)


# Test 2: negative coefficient
x = solve_linear(-3, 6)
assert x == 2
assert check_solution(-3, 6, x)


# Test 3: no solution case
result = solve_linear(0, 5)
assert result == "no solution"


# Test 4: infinite solutions case
result = solve_linear(0, 0)
assert result == "infinite solutions"


# Test 5: float coefficients
x = solve_linear(0.5, 1.0)
assert check_solution(0.5, 1.0, x)


# Bonus: multiple cases
cases = [(2, 4), (-3, 6)]
results = solve_many(cases)
assert results == [-2, 2]


print("All tests passed!")
