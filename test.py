from my_mip.solver.solver import Model


model = Model()
x = model.NewIntegerVar("x", lb=0, ub=10)
y = model.NewIntegerVar("y",lb=0, ub=10)


model.Add(3*x + 2*y <= 6)
model.Add(-3*x + 2*y <= 0)

model.SetObjective(1*y, sense='maximize')


model.solve()