from z3 import Solver, Bool, Bools, Or, And, Not, Implies, If, BoolVector

# Create one variable at at time
a = Bool('a')

# Create multiple variables at once
b, c, d, e, f, g = Bools('b c d e f g')

arr = [
    [0,0,0,0,0,0],
    [1,0,0,0,3,0],
    [2,0,0,0,0,0],
    [0,0,0,0,1,0],
    [0,0,3,0,0,2]
]

#
n = 6
numColors = 3

# create a 3d matrix of boolean vars

m = []
colorClause = []
for i in range(0,numColors):
    m.append([BoolVector(n)])
    for j in range(1,n):
        m.append([BoolVector(n)])
for k in range(0,numColors-1): # each color
    for i in range(0,n): # each row
        for j in range(0,n): # each colum
            for k2 in range(k+1,numColors): # each color
                colorClause.append( Or(Not(m[k][i][j]), m[k2][i][j])) # color in this cell implies no other color in other cells



s = Solver()



# Construct clauses
c1 = Or(b, d, Not(f))
c1.add(a)
c2 = Or(a, Not(c), e)
c3 = Or(Not(a), f)
c4 = a

# AND all clauses together
formula = And(c1, c2, c3, c4)

# Add formula to solver
s.add(formula)

# Alternatively, you can call s.add() multiple times and
# the effect is the same as ANDing all clauses
# s.add(c1)
# s.add(c2)
# s.add(c3)


# Check if satisfiable
if s.check().r > 0:
    print('Satisfiable')
# Not satisfiable
else:
    print('Unsatisfiable')



#######################################
# Now do the same but more dynamic... #
#######################################


# Construct a solver from an array of clauses in CNF form
def construct_solver(vars, clauses):
    for (i, cl) in enumerate(clauses):
        clauses[i] = [vars[key] if key[0] != '-' else Not(vars[key[1:]]) for key in cl]

    clauses = map(lambda clause: Or(*clause), clauses)
    formula = And(*clauses)

    s = Solver()
    s.add(formula)

    return s


# Print the solution
def print_solution(vars, solver):
    if solver.check().r > 0:
        print('Satisfiable')
        model = solver.model()
        values = {key: model.get_interp(value) for (key, value) in vars.items()}

        # Alternatively, you can extract the variables from the solver itself
        # values = { key.name(): model.get_interp(key) for key in model }

        solution = ' & '.join([key if value else '-' + key for (key, value) in values.items()])
        print(solution)
    else:
        print('Unsatisfiable')


# Now just call the functions...
vars = {c: Bool(c) for c in 'abcdefg'}
clauses = [['b', 'd', '-f'], ['a', '-c', 'e'], ['-a', 'f'], ['a']]
solver = construct_solver(vars, clauses)
print_solution(vars, solver)