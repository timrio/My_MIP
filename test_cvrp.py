from my_mip.solver.solver import Model
from itertools import combinations

# # # Initialize the model
model = Model()

# # Parameters
num_customers = 4
num_vehicles = 3
vehicle_capacity = 12
demand = [0, 3, 6, 9, 12]  #Including depot (0) as the first element
depot = 0

# # Distance matrix (symmetric)
distance = [
    [0, 10, 15, 20, 25],
    [10, 0, 35, 25, 30],
    [15, 35, 0, 30, 20],
    [20, 25, 30, 0, 15],
    [25, 30, 20, 15, 0]
]

# # Decision variables: x[i, j, k] is 1 if vehicle k travels from i to j
x = {}
for i in range(num_customers + 1):
    for j in range(num_customers + 1):
        for k in range(num_vehicles):
            if i != j:
                x[(i, j, k)] = model.NewBoolVar(f"x_{i}_{j}_{k}")

# # Objective function: Minimize the total distance
model.SetObjective(sum(distance[i][j] * x[i, j, k] for i in range(num_customers + 1)
                       for j in range(num_customers + 1) 
                       for k in range(num_vehicles) if i != j), sense='minimize')

# # Constraints
# # Each customer is visited exactly once

for j in range(1, num_customers + 1):
    model.Add(sum(1*x[i, j, k] for i in range(num_customers + 1) 
                  for k in range(num_vehicles) if i != j) == 1)

# # Capacity constraints for each vehicle
for k in range(num_vehicles):
    model.Add(sum(demand[j] * sum(1*x[i, j, k] for i in range(num_customers + 1) if i != j) 
                  for j in range(1, num_customers + 1)) <= vehicle_capacity)

for k in range(num_vehicles):
    for i in range(num_customers + 1):
        model.Add((sum(1*x[i, j, k] for j in range(num_customers + 1) if i != j) == sum(1*x[j, i, k] for j in range(num_customers + 1) if i != j)))  #Enter and leave each location

for s in range(2, num_customers + 1):
    for subset in combinations(range(1, num_customers + 1), s):
        model.Add(sum(x[i, j, k] for i in subset for j in subset if i != j for k in range(num_vehicles)) <= len(subset) - 1)

# # Solve the problem
solution = model.solve()