# from my_mip.solver.solver import Model

# def solve_sudoku_custom(puzzle):
#     model = Model()

#     # Create binary variables for each cell and possible number
#     a = [[[model.NewBoolVar(f'a_{i}_{j}_{k}') for k in range(9)] for j in range(9)] for i in range(9)]

#     # Constraints

#     # Each cell must contain exactly one number
#     for i in range(9):
#         for j in range(9):
#             model.Add(sum(1 * a[i][j][k] for k in range(9)) == 1)

#     # Each number appears exactly once in each row
#     for k in range(9):
#         for i in range(9):
#             model.Add(sum(1 * a[i][j][k] for j in range(9)) == 1)

#     # Each number appears exactly once in each column
#     for k in range(9):
#         for j in range(9):
#             model.Add(sum(1 * a[i][j][k] for i in range(9)) == 1)

#     # Each number appears exactly once in each 3x3 subgrid
#     for k in range(9):
#         for x in range(3):
#             for y in range(3):
#                 model.Add(sum(1 * a[3*x + i][3*y + j][k] for i in range(3) for j in range(3)) == 1)

#     # Add clues from the puzzle
#     for i in range(9):
#         for j in range(9):
#             if puzzle[i][j] > 0:
#                 model.Add(1*a[i][j][puzzle[i][j] - 1] == 1)

#     # Objective: Dummy objective, as this is a feasibility problem
#     model.SetObjective(sum(1 * a[0][0][k] for k in range(9)), 'minimize')

#     # Solve the model
#     model.solve()

# # Example Sudoku puzzle
# example_puzzle = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]]

# # Solve the Sudoku puzzle
# solution = solve_sudoku_custom(example_puzzle)


from my_mip.solver.solver import Model

# Initialize the model
model = Model()

# Define integer variables
x1 = model.NewIntegerVar("x1", lb=0, ub=10)
x2 = model.NewIntegerVar("x2", lb=0, ub=10)
x3 = model.NewIntegerVar("x3", lb=0, ub=10)
x4 = model.NewIntegerVar("x4", lb=0, ub=10)
x5 = model.NewIntegerVar("x5", lb=0, ub=10)
x6 = model.NewIntegerVar("x6", lb=0, ub=10)

# Define binary variables
b1 = model.NewBoolVar("b1")
b2 = model.NewBoolVar("b2")

# Add constraints
model.Add(2*x1 + 3*x2 + 1*x3 + 4*x4 + 5*b1 <= 20)
model.Add(1*x1 + (-1)* 1*x2 + 1*x5 <= 4)
model.Add(1*x3 + 2*x4 + (-3)*b2 >= 12)
model.Add(x5 + x6 + (-1)*b1 + 1*b2 <= 5)
model.Add(x6 + b2 <= 7)

# Set the objective
model.SetObjective(3*x1 + 2*x2 + 2*x3 + x4 + 5*b1 + 4*b2, sense='maximize')

# Solve the model
solution = model.solve()

