from .constraints_and_var import Variable, Constraint, Objective, Expression
import numpy as np
from numpy.linalg import inv
from my_mip.solver.branch_and_bound import BranchAndBound
from my_mip.solver.node import Node


class Model(BranchAndBound):
    def __init__(self, mip_gap = 0.01):
        self.variables = []
        self.constraints = []
        self.objective = None
        self.initial_basis_indexes = []
        self.mip_gap = mip_gap
        super().__init__()


    def NewBoolVar(self, name):
        var = Variable(name, lb=0, ub=1, vtype='binary')
        self.variables.append(var)
        return var
    
    def NewIntegerVar(self, name, lb, ub):
        var = Variable(name, lb=0, ub=ub, vtype='integer')
        self.variables.append(var)
        return var

    def NewContinuousVar(self, name, lb, ub):
        var = Variable(name, lb=0, ub=ub, vtype='continuous')
        self.variables.append(var)
        return var

    def NewSlackVar(self):
        # Method to create and return a new slack or surplus variable
        # Adjust the implementation as per your requirements
        slack_var = Variable(f"slack_{len(self.variables)}", lb=0, vtype='slack')
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

            # Adding lower and upper bound constraints for each variable
        for i, var in enumerate(self.variables):
            # Lower bound constraint
            if var.lb >0:
                for existing_row in A:
                    existing_row.append(0)

                lower_bound_row = [0] * len(A[-1])
                lower_bound_row[i] = -1  # Coefficient for the variable
                lower_bound_row[-1] = 1
                A.append(lower_bound_row)
                b.append(-var.lb)
                slack_var = self.NewSlackVar()
                self.variables.append(slack_var)
                c.append(0)  # Slack/surplus variables have zero cost in the objective



            # Upper bound constraint
            if var.ub < float('inf'):
                for existing_row in A:
                    existing_row.append(0)
                upper_bound_row = [0] * len(A[-1])
                upper_bound_row[i] = 1  # Coefficient for the variable
                upper_bound_row[-1] = 1
                A.append(upper_bound_row)
                b.append(var.ub)
                slack_var = self.NewSlackVar()
                self.variables.append(slack_var)
                c.append(0)  # Slack/surplus variables have zero cost in the objective


        # initialize basis_indexes as the slack variables
        basis_indexes = list(range(len(A[0])-len(A), len(A[0])))
        non_basis_indexes = list(range(len(A[0])-len(A)))
        return Node(A, b, c, basis_indexes, non_basis_indexes, variables=self.variables, constraints=self.constraints)




    def solve(self):
        root_node = self.create_root_node()
        self.initial_basis_indexes = root_node.basis_indexes[:]

        best_node, best_value = self.branch_and_bound(root_node)

        self.print_solution(best_node, best_value)
        return



    def print_solution(self, node, value):
        if self.objective.sense == 'maximize':
            value = -value
        print(f"Optimal value = {value}")
        for i, var in enumerate(iterable=node.variables):
            if var.vtype == "slack":
                continue
            if not (i in node.basis_indexes):
                print(f"variable {var.name} = 0")
                continue
            position = node.basis_indexes.index(i)
            value = node.current_solution[position]
            print(f"variable {var.name} = {np.round(value,2)}")