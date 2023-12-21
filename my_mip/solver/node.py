import numpy as np 
from .constraints_and_var import Variable

class Node:
    def __init__(self, A, b, c, basis_indexes, non_basis_indexes,variables, constraints):
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.basis_indexes = basis_indexes
        self.non_basis_indexes = non_basis_indexes
        self.current_solution = None
        self.current_optimal_value = np.inf
        self.variables=variables
        self.constraints=constraints
        self.status = "Not solved"

    def NewSlackVar(self):
        # Method to create and return a new slack or surplus variable
        # Adjust the implementation as per your requirements
        slack_var = Variable(f"slack_{len(self.variables)}", lb=0, vtype='slack')
        return slack_var


    @property
    def number_of_variables(self): 
        return self.A.shape[1]

    @property
    def number_of_constraints(self):
        return self.A.shape[0]