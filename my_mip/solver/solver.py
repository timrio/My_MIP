from .constraints_and_var import Variable, Constraint, Objective, Expression
import numpy as np
from numpy.linalg import inv
from my_mip.solver.branch_and_bound import BranchAndBound
from my_mip.solver.node import Node


class Model(BranchAndBound):
    def __init__(self):
        self.variables = []
        self.constraints = []
        self.objective = None
        self.initial_basis_indexes = []
        super().__init__()


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

    def create_root_node(self):
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

        # initialize basis_indexes as the slack variables
        basis_indexes = list(range(len(self.variables)-len(self.constraints), len(self.variables)))
        non_basis_indexes = list(range(len(self.variables)-len(self.constraints)))
        return Node(A, b, c, basis_indexes, non_basis_indexes, variables=self.variables, constraints=self.constraints)




    def solve(self):
        root_node = self.create_root_node()
        self.initial_basis_indexes = root_node.basis_indexes

        best_solution = self.branch_and_bound(root_node)

        return best_solution




