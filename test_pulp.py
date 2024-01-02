import pulp
from itertools import combinations

# Parameters
num_customers = 4
num_vehicles = 3
vehicle_capacity = 12
demand = [0, 3, 6, 9, 12]  # Including depot as first element
depot = 0

# Distance matrix (symmetric)
distance = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 20],
    [20, 25, 30, 0, 15],
    [25, 30, 20, 15, 0]
]

# Create the model
model = pulp.LpProblem("CVRP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(num_customers + 1) 
                                for j in range(num_customers + 1) 
                                for k in range(num_vehicles)),
                          cat='Binary')

# Objective function
model += pulp.lpSum(distance[i][j] * x[i, j, k] for i in range(num_customers + 1)
                    for j in range(num_customers + 1) 
                    for k in range(num_vehicles) if i != j)

# Constraints
# Each customer is visited exactly once
for j in range(1, num_customers + 1):
    model += sum(x[i, j, k] for i in range(num_customers + 1) 
                 for k in range(num_vehicles) if i != j) == 1

# Enter and leave each location for each vehicle
for k in range(num_vehicles):
    for i in range(num_customers + 1):
        model += sum(x[i, j, k] for j in range(num_customers + 1) if i != j) == \
                 sum(x[j, i, k] for j in range(num_customers + 1) if i != j)

# Vehicle capacity constraints
for k in range(num_vehicles):
    model += sum(demand[j] * sum(x[i, j, k] for i in range(num_customers + 1) if i != j) 
                 for j in range(1, num_customers + 1)) <= vehicle_capacity

# Subtour elimination constraints
for s in range(2, num_customers + 1):
    for subset in combinations(range(1, num_customers + 1), s):
        model += sum(x[i, j, k] for i in subset for j in subset if i != j for k in range(num_vehicles)) <= len(subset) - 1

# Solve the problem
solution = model.solve()

# Print the solution
for k in range(num_vehicles):
    print(f"Vehicle {k}:")
    for i in range(num_customers + 1):
        for j in range(num_customers + 1):
            if i != j and pulp.value(x[i, j, k]) > 0:
                print(f" {i} -> {j}")
