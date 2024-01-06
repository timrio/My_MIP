import pulp

# Initialize the model
model = pulp.LpProblem("Sudoku_Problem", pulp.LpMinimize)

# Boolean variables: grid[i, j, num] is 1 if the cell at row i, column j contains the number num
grid = {}
for i in range(1, 10):
    for j in range(1, 10):
        for num in range(1, 10):
            grid[(i, j, num)] = pulp.LpVariable(f'grid_{i}_{j}_{num}', cat='Binary')

# Dummy objective (since this is a feasibility problem)
model += 0

# Constraint: Each cell contains exactly one number
for i in range(1, 10):
    for j in range(1, 10):
        model += sum(grid[i, j, num] for num in range(1, 10)) == 1

# Constraint: Each number appears exactly once in each row and each column
for num in range(1, 10):
    for i in range(1, 10):
        model += sum(grid[i, j, num] for j in range(1, 10)) == 1
        model += sum(grid[j, i, num] for j in range(1, 10)) == 1

# Constraint: Each number appears exactly once in each 3x3 subgrid
for num in range(1, 10):
    for block_row in range(3):
        for block_col in range(3):
            model += sum(grid[i, j, num] for i in range(1 + block_row * 3, 4 + block_row * 3)
                            for j in range(1 + block_col * 3, 4 + block_col * 3)) == 1

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
            model += grid[i+1, j+1, num] == 1

# Solve the problem
model.solve()

# Print solution
for i in range(1, 10):
    for j in range(1, 10):
        for num in range(1, 10):
            if pulp.value(grid[i, j, num]) == 1:
                print(num, end=' ')
                break
    print()  # Newline after each row
