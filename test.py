from my_mip.solver.solver import Model

# Initialize the model
model = Model()

# Cities and distance matrix (symmetric)
cities = ['A', 'B', 'C', 'D']
distance = {
    ('A', 'B'): 10, ('B', 'A'): 10,
    ('A', 'C'): 15, ('C', 'A'): 15,
    ('A', 'D'): 20, ('D', 'A'): 20,
    ('B', 'C'): 35, ('C', 'B'): 35,
    ('B', 'D'): 25, ('D', 'B'): 25,
    ('C', 'D'): 30, ('D', 'C'): 30
}

# Decision variables: x[i, j] is 1 if the path from i to j is chosen
x = {}
for i in cities:
    for j in cities:
        if i != j:
            x[(i, j)] = model.NewBoolVar(f"x_{i}_{j}")

# Objective function: Minimize the total distance
model.SetObjective(sum(distance[i, j] * x[i, j] for i in cities for j in cities if i != j), sense='minimize')

# Constraints
# Each city must be entered and left exactly once
for city in cities:
    model.Add(sum(1*x[city, j] for j in cities if j != city) == 1)  # leave city
    model.Add(sum(1*x[i, city] for i in cities if i != city) == 1)  # enter city

# Solve the problem
solution = model.solve()

# [Code to extract and display the solution based on your solver's methods]



from my_mip.solver.solver import Model

# # Initialize the model
# model = Model()

# # Define integer variables
# x1 = model.NewIntegerVar("x1", lb=0, ub=10)
# x2 = model.NewIntegerVar("x2", lb=0, ub=10)
# x3 = model.NewIntegerVar("x3", lb=0, ub=10)
# x4 = model.NewIntegerVar("x4", lb=0, ub=10)
# x5 = model.NewIntegerVar("x5", lb=0, ub=10)
# x6 = model.NewIntegerVar("x6", lb=0, ub=10)

# # Define binary variables
# b1 = model.NewBoolVar("b1")
# b2 = model.NewBoolVar("b2")

# # Add constraints
# model.Add(2*x1 + 3*x2 + 1*x3 + 4*x4 + 5*b1 <= 20)
# model.Add(1*x1 + (-1)* 1*x2 + 1*x5 <= 4)
# model.Add(1*x3 + 2*x4 + (-3)*b2 >= 12)
# model.Add(x5 + x6 + (-1)*b1 + 1*b2 <= 5)
# model.Add(x6 + b2 <= 7)

# # Set the objective
# model.SetObjective(3*x1 + 2*x2 + 2*x3 + x4 + 5*b1 + 4*b2, sense='maximize')

# # Solve the model
# solution = model.solve()

