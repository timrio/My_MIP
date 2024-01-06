import pulp

# Initialize the model
model = pulp.LpProblem("Sudoku Problem", pulp.LpMinimize)

# Adjusting the ranges for a 4x4 Sudoku
grid = {}
for i in range(1, 5):
    for j in range(1, 5):
        for num in range(1, 5):
            grid[(i, j, num)] = pulp.LpVariable(f'grid_{i}_{j}_{num}', cat='Binary')

# Constraint: Each cell contains exactly one number
for i in range(1, 5):
    for j in range(1, 5):
        model += sum(grid[i, j, num] for num in range(1, 5)) == 1

# Constraint: Each number appears exactly once in each row and each column
for num in range(1, 5):
    for i in range(1, 5):
        model += sum(grid[i, j, num] for j in range(1, 5)) == 1
        model += sum(grid[j, i, num] for j in range(1, 5)) == 1

# Constraint: Each number appears exactly once in each 2x2 subgrid
for num in range(1, 5):
    for block_row in range(2):
        for block_col in range(2):
            model += sum(grid[i, j, num] for i in range(1 + block_row * 2, 3 + block_row * 2)
                            for j in range(1 + block_col * 2, 3 + block_col * 2)) == 1

# Pre-filled cells for a 4x4 Sudoku puzzle
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
            model += grid[i+1, j+1, num] == 1

# Dummy Objective (required by PuLP, even if irrelevant)
model += 0, "Arbitrary Objective Function"

# Solve the problem
model.solve()

# Print solution
for i in range(1, 5):
    for j in range(1, 5):
        for num in range(1, 5):
            if pulp.value(grid[i, j, num]) == 1:
                print(num, end=' ')
                break
    print()  # Newline after each row
