from .constraints_and_var import Variable, Constraint


class Model:
    def __init__(self):
        self.variables = []
        self.constraints = []
        self.objective = None

    def NewBoolVar(self, name):
        var = Variable(name, lb=0, ub=1, vtype='binary')
        self.variables.append(var)
        return var
    
    def NewIntegerVar(self, name, lb, ub):
        var = Variable(name, lb=lb, ub=ub, vtype='integer')
        self.variables.append(var)
        return var

    def NewContinuousVar(self, name, lb, ub):
        var = Variable(name, lb=lb, ub=ub, vtype='continuous')
        self.variables.append(var)
        return var

    def Add(self, constraint):
        if not isinstance(constraint, Constraint):
            raise ValueError("Argument must be of type Constraint")
        self.constraints.append(constraint)

