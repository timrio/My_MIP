from .constraints_and_var import Variable, Constraint, Objective, Expression
from my_mip.core.cutting_planes.gomory_cuts import find_gomory_cuts, add_gomory_cuts_to_model
from my_mip.core.simplex_solvers.dual_simplex import dual_simplex
from my_mip.core.simplex_solvers.primal_simplex import primal_simplex
import numpy as np
from numpy.linalg import inv


class Model:
    def __init__(self):
        self.variables = []
        self.constraints = []
        self.objective = None
        self.H = None
        self.current_optimal_value = None
        self.current_solution = None


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

    def NewSlackVar(self):
        # Method to create and return a new slack or surplus variable
        # Adjust the implementation as per your requirements
        slack_var = Variable(f"slack_{len(self.variables)}", lb=0, vtype='continuous')
        return slack_var

    def Add(self, constraint):
        if not isinstance(constraint, Constraint):
            raise ValueError("Argument must be of type Constraint")
        self.constraints.append(constraint)

    def SetObjective(self, expression, sense='minimize'):
        if not isinstance(expression, Expression):
            raise ValueError("Objective must be an Expression")
        if sense not in ['minimize', 'maximize']:
            raise ValueError("Sense must be 'minimize' or 'maximize'")
        self.objective = Objective(expression, sense)

    def define_matrices(self):
        # Initialize c, A, and b
        c = [0] * len(self.variables)
        A = []
        b = []

        # Define c vector based on the objective function
        for i, var in enumerate(self.variables):
            coeff = self.objective.expression.terms.get(var, 0)
            if self.objective.sense == 'maximize':
                coeff = -coeff
            c[i] = coeff

        # Define A matrix and b vector based on the constraints
        for constraint in self.constraints:
            row = [0] * len(self.variables)
            for var, coeff in constraint.expression.terms.items():
                if constraint.sense == '>=':
                    coeff = -coeff
                row[self.variables.index(var)] = coeff

            # Handling slack/surplus variables for inequalities
            if constraint.sense != '==':
                # Add a slack or surplus variable
                slack_var = self.NewSlackVar()
                self.variables.append(slack_var)
                c.append(0)  # Slack/surplus variables have zero cost in the objective
                
                # Update existing rows in A to account for the new variable
                for existing_row in A:
                    existing_row.append(0)

                # Coefficient for slack/surplus variable
                row.append(1)

            # Add row to A matrix and corresponding value to b vector
            A.append(row)
            b_value = constraint.rhs if constraint.sense == '<=' else -constraint.rhs
            b.append(b_value)

        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)

        # initialize basis_indexes as the slack variables
        self.basis_indexes = list(range(len(self.variables)-len(self.constraints), len(self.variables)))
        self.non_basis_indexes = list(range(len(self.variables)-len(self.constraints)))

        return 


    @property
    def number_of_variables(self): 
        return self.A.shape[1]

    @property
    def number_of_constraints(self):
        return self.A.shape[0]


    def solve(self):
        self.define_matrices()

        # reach first optimal relaxed solution with simplex
        self.current_solution, self.current_optimal_value, self.H, self.basis_indexes, self.non_basis_indexes = primal_simplex(self.A, self.b, self.c, self.basis_indexes, self.non_basis_indexes)

        # if the solution is not integer, add gomory cuts and resolve
        while not np.allclose(self.current_solution, np.round(self.current_solution)):
            # Find Gomory cuts
            gomory_cuts = find_gomory_cuts(self)
            # Add cuts to the model
            add_gomory_cuts_to_model(self, gomory_cuts)
            # resolve
            self.current_solution, self.current_optimal_value, self.H, self.basis_indexes, self.non_basis_indexes = dual_simplex(self.A, self.b, self.c, self.basis_indexes, self.non_basis_indexes, self.number_of_variables, self.number_of_constraints)



