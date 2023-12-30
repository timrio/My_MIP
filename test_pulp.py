import pulp

# Parameters
num_customers = 4
num_vehicles = 2
vehicle_capacity = 15
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
for j in range(1, num_customers + 1):
    model += sum(x[i, j, k] for i in range(num_customers + 1) 
                 for k in range(num_vehicles) if i != j) == 1  # Each customer is visited once

for k in range(num_vehicles):
    for i in range(num_customers + 1):
        model += sum(x[i, j, k] for j in range(num_customers + 1) if i != j) == \
                 sum(x[j, i, k] for j in range(num_customers + 1) if i != j)  # Enter and leave each location

for k in range(num_vehicles):
    model += sum(demand[j] * sum(x[i, j, k] for i in range(num_customers + 1) if i != j) 
                 for j in range(1, num_customers + 1)) <= vehicle_capacity  # Vehicle capacity

# Solve the problem
model.solve()

# Print the solution
for k in range(num_vehicles):
    print(f"Vehicle {k}:")
    for i in range(num_customers + 1):
        for j in range(num_customers + 1):
            if i != j and pulp.value(x[i, j, k]) > 0:
                print(f" {i} -> {j}")



# import pulp

# # Create a new LP problem
# model = pulp.LpProblem("Complex_LP_Problem", pulp.LpMaximize)

# # Define integer variables
# x1 = pulp.LpVariable('x1', lowBound=0, upBound=10, cat='Integer')
# x2 = pulp.LpVariable('x2', lowBound=0, upBound=10, cat='Integer')
# x3 = pulp.LpVariable('x3', lowBound=0, upBound=10, cat='Integer')
# x4 = pulp.LpVariable('x4', lowBound=0, upBound=10, cat='Integer')
# x5 = pulp.LpVariable('x5', lowBound=0, upBound=10, cat='Integer')
# x6 = pulp.LpVariable('x6', lowBound=0, upBound=10, cat='Integer')

# # Define binary variables
# b1 = pulp.LpVariable('b1', cat='Binary')
# b2 = pulp.LpVariable('b2', cat='Binary')

# # Add constraints
# model += (2*x1 + 3*x2 + x3 + 4*x4 + 5*b1 <= 20, "Constraint_1")
# model += (x1 - x2 + x5 <= 4, "Constraint_2")
# model += (x3 + 2*x4 - 3*b2 >= 12, "Constraint_3")
# model += (x5 + x6 - b1 + b2 <= 5, "Constraint_4")
# model += (x6 + b2 <= 7, "Constraint_5")

# # Set the objective
# model += 3*x1 + 2*x2 + 2*x3 + x4 + 5*b1 + 4*b2, "Objective"

# # Solve the model
# model.solve()

# # Print the status of the solution
# print("Status:", pulp.LpStatus[model.status])

# # Print the optimal values of the variables
# for variable in model.variables():
#     print(f"{variable.name} = {variable.varValue}")

# # Print the optimal objective value
# print("Optimal Objective Value:", pulp.value(model.objective))