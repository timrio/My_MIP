from my_mip.solver.solver import Model

# Initialize the model
model = Model()

# Boolean variables: grid[i, j, num] is 1 if the cell at row i, column j contains the number num
grid = {}
for i in range(1, 10):
    for j in range(1, 10):
        for num in range(1, 10):
            grid[(i, j, num)] = model.NewBoolVar(f'grid_{i}_{j}_{num}')

# Constraint: Each cell contains exactly one number
for i in range(1, 10):
    for j in range(1, 10):
        model.Add(sum(1*grid[i, j, num] for num in range(1, 10)) == 1)

# Constraint: Each number appears exactly once in each row and each column
for num in range(1, 10):
    for i in range(1, 10):
        model.Add(sum(1*grid[i, j, num] for j in range(1, 10)) == 1)
        model.Add(sum(1*grid[j, i, num] for j in range(1, 10)) == 1)

# Constraint: Each number appears exactly once in each 3x3 subgrid
for num in range(1, 10):
    for block_row in range(3):
        for block_col in range(3):
            model.Add(sum(1*grid[i, j, num] for i in range(1 + block_row * 3, 4 + block_row * 3)
                            for j in range(1 + block_col * 3, 4 + block_col * 3)) == 1)

# Pre-filled cells for a realistic Sudoku puzzle
prefilled = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

for i in range(9):
    for j in range(9):
        num = prefilled[i][j]
        if num != 0:
            model.Add(1*grid[i+1, j+1, num] == 1)

# Dummy Objective: Sum of all variables (this is constant for any valid solution)
model.SetObjective(sum(1*grid[i, j, num] for i in range(1, 10) for j in range(1, 10) for num in range(1, 10)))

# Solve the problem
solution = model.solve()

# Print solution
for i in range(1, 10):
    for j in range(1, 10):
        for num in range(1, 10):
            if solution.Value(grid[i, j, num]) == 1:
                print(num, end=' ')
                break
    print()  # Newline after each row
