'''Solve linear equations of the form:

ax + b = 0
'''

def solve_linear(a, b):
    '''
    Returns:
        number -> solution for x
        string -> 'no solution' or 'infinite solutions'
    '''
    if a == 0 and b == 0:
        return "infinite solutions"

    if a == 0 and b != 0:
        return "no solution"

    # a is not zero
    x = -b / a
    return x


def check_solution(a, b, x):
    '''
    Substitute x back into ax + b
    '''
    return a * x + b == 0


def solve_many(cases):
    '''
    Solve a list of (a, b) equations
    '''
    answers = []

    for a, b in cases:
        answers.append(solve_linear(a, b))

    return answers
