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
model.Add(1*x3 + 2*x4 + (-3)*b2 <= 12)
model.Add(x5 + x6 + (-1)*b1 + 1*b2 <= 5)
model.Add(x6 + b2 <= 7)

# Set the objective
model.SetObjective(3*x1 + 2*x2 + 2*x3 + x4 + 5*b1 + 4*b2, sense='maximize')

# Solve the model
solution = model.solve()