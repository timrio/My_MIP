from my_mip.solver.solver import Model

# # # # Initialize the model
model = Model()

# # # Parameters
# num_customers = 2
# num_vehicles = 2
# vehicle_capacity = 15
# demand = [0, 3, 6, 9, 12]  #Including depot (0) as the first element
# depot = 0

# # # Distance matrix (symmetric)
# distance = [
#     [0, 10, 15, 20, 25],
#     [10, 0, 35, 25, 30],
#     [15, 35, 0, 30, 20],
#     [20, 25, 30, 0, 15],
#     [25, 30, 20, 15, 0]
# ]

# # # Decision variables: x[i, j, k] is 1 if vehicle k travels from i to j
# x = {}
# for i in range(num_customers + 1):
#     for j in range(num_customers + 1):
#         for k in range(num_vehicles):
#             if i != j:
#                 x[(i, j, k)] = model.NewBoolVar(f"x_{i}_{j}_{k}")

# # # Objective function: Minimize the total distance
# model.SetObjective(sum(distance[i][j] * x[i, j, k] for i in range(num_customers + 1)
#                        for j in range(num_customers + 1) 
#                        for k in range(num_vehicles) if i != j), sense='minimize')

# # # Constraints
# # # Each customer is visited exactly once

# for j in range(1, num_customers + 1):
#     model.Add(sum(1*x[i, j, k] for i in range(num_customers + 1) 
#                   for k in range(num_vehicles) if i != j) == 1)

# # # Capacity constraints for each vehicle
# for k in range(num_vehicles):
#     model.Add(sum(demand[j] * sum(1*x[i, j, k] for i in range(num_customers + 1) if i != j) 
#                   for j in range(1, num_customers + 1)) <= vehicle_capacity)

# for k in range(num_vehicles):
#     for i in range(num_customers + 1):
#         model.Add((sum(1*x[i, j, k] for j in range(num_customers + 1) if i != j) == sum(1*x[j, i, k] for j in range(num_customers + 1) if i != j)))  #Enter and leave each location

# # # Solve the problem
# solution = model.solve()

# [Code to extract and display the solution based on your solver's methods]


# from my_mip.solver.solver import Model

# # # Initialize the model
# model = Model()

# #  #Define integer variables
x1 = model.NewIntegerVar("x1", lb=0, ub=10)
x2 = model.NewIntegerVar("x2", lb=0, ub=10)
x3 = model.NewIntegerVar("x3", lb=0, ub=10)
x4 = model.NewIntegerVar("x4", lb=0, ub=10)
x5 = model.NewIntegerVar("x5", lb=0, ub=10)
x6 = model.NewIntegerVar("x6", lb=0, ub=10)

# #  #Define binary variables
b1 = model.NewBoolVar("b1")
b2 = model.NewBoolVar("b2")

# # # Add constraints
model.Add(2*x1 + 3*x2 + 1*x3 + 4*x4 + 5*b1 <= 20)
model.Add(1*x1 + (-1)* 1*x2 + 1*x5 <= 4)
model.Add(1*x3 + 2*x4 + (-3)*b2 == 12)
model.Add(x5 + x6 + (-1)*b1 + 1*b2 <= 5)
model.Add(x6 + b2 <= 7)
model.Add(b1 + b2 == 1)
model.Add(b1 + b2 == 0)

# # Set the objective
model.SetObjective(3*x1 + 2*x2 + 2*x3 + x4 + 5*b1 + 4*b2, sense='maximize')

# # # Solve the model
solution = model.solve()

