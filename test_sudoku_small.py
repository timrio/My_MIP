from my_mip.solver.solver import Model

# Initialize the model
model = Model()

# Adjusting the ranges for a 4x4 Sudoku
grid = {}
for i in range(1, 5):
    for j in range(1, 5):
        for num in range(1, 5):
            grid[(i, j, num)] = model.NewBoolVar(f'grid_{i}_{j}_{num}')

# Constraint: Each cell contains exactly one number
for i in range(1, 5):
    for j in range(1, 5):
        model.Add(sum(1*grid[i, j, num] for num in range(1, 5)) == 1)

# Constraint: Each number appears exactly once in each row and each column
for num in range(1, 5):
    for i in range(1, 5):
        model.Add(sum(1*grid[i, j, num] for j in range(1, 5)) == 1)
        model.Add(sum(1*grid[j, i, num] for j in range(1, 5)) == 1)

# Constraint: Each number appears exactly once in each 2x2 subgrid
for num in range(1, 5):
    for block_row in range(2):
        for block_col in range(2):
            model.Add(sum(1*grid[i, j, num] for i in range(1 + block_row * 2, 3 + block_row * 2)
                            for j in range(1 + block_col * 2, 3 + block_col * 2)) == 1)

# Pre-filled cells for a 4x4 Sudoku puzzle
# Update this section with the actual pre-filled values for your 4x4 puzzle
prefilled = [
    [1, 0, 0, 0],
    [0, 0, 0, 2],
    [0, 0, 0, 0],
    [0, 3, 0, 0]
]

for i in range(4):
    for j in range(4):
        num = prefilled[i][j]
        if num != 0:
            model.Add(1*grid[i+1, j+1, num] == 1)

# Dummy Objective: Sum of all variables (this is constant for any valid solution)
model.SetObjective(0*grid[1,1,1])

# Solve the problem
solution = model.solve()

# Print solution
for i in range(1, 5):
    for j in range(1, 5):
        for num in range(1, 5):
            if solution.Value(grid[i, j, num]) == 1:
                print(num, end=' ')
                break
    print()  # Newline after each row
