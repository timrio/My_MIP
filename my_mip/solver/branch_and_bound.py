import numpy as np
from my_mip.solver.constraints_and_var import Constraint, Variable, Expression
from my_mip.core.simplex_solvers.primal_simplex import primal_simplex
from my_mip.core.simplex_solvers.dual_simplex import dual_simplex
from my_mip.core.cutting_planes.gomory_cuts import find_gomory_cuts, add_gomory_cuts_to_model
from my_mip.solver.node import Node


class BranchAndBound:
    def __init__(self):
        self.root_node = None
        self.best_solution = None
        self.best_objective = np.inf
        self.active_nodes = []

    def is_integer_solution(self, node):
        for val in node.current_solution[self.initial_basis_indexes]:
            if np.round(val,0)!=val:
                return False
        return True

    def branch_and_bound(self, root_node):
        self.root_node = root_node
        self.active_nodes.append(root_node)
        while self.active_nodes:
            current_node = self.select_next_node()
            current_node = self.solve_lp_relaxation(current_node)
            if current_node.current_optimal_value > self.best_objective:
                # here we prune the node
                continue
            if self.is_integer_solution(current_node):
                self.update_best_solution(current_node)
            else:
                self.branch(current_node)
        return self.best_solution

    def select_next_node(self):
        # Select the next node to explore
        # Adjust the implementation as per your requirements
        return self.active_nodes.pop()

    def update_best_solution(self, node):
        if node.current_optimal_value < self.best_objective:
            self.best_solution = node.current_solution
            self.best_objective = node.current_optimal_value


    def solve_lp_relaxation(self, node):
        # reach first optimal relaxed solution with simplex
        node = primal_simplex(node)

        # if the solution is not integer, add gomory cuts and resolve
        if not np.allclose(node.current_solution, np.round(node.current_solution)):
            # Find Gomory cuts
            gomory_cuts = find_gomory_cuts(node)
            # Add cuts to the model
            node = add_gomory_cuts_to_model(node, gomory_cuts)
            # resolve
            node = dual_simplex(node)
        return node


    def branch(self, node):
        # Identify a variable for branching
        branching_var_index, branching_var_value = self.select_branching_variable(node)

        # Create constraints for the two branches
        var = node.variables[branching_var_index]

        # Branch down (floor)
        constraint_down = Constraint(Expression()._add_variable(var), sense='<=', rhs=np.floor(branching_var_value))
        node_down = self.create_child_node(node, constraint_down)

        # Branch up (ceil)
        constraint_up = Constraint(Expression()._add_variable(var), sense='>=', rhs=np.ceil(branching_var_value))
        node_up = self.create_child_node(node, constraint_up)

        # Add child nodes to the active nodes list
        self.active_nodes.extend([node_down, node_up])

    def select_branching_variable(self, node):
        # Select a variable to branch on
        # This could be the first non-integer variable in the current solution
        for i, value in enumerate(node.current_solution):
            if not np.isclose(value, np.round(value)):
                return i, value
        raise Exception("No non-integer variables found for branching")

    def create_child_node(self, parent_node, additional_constraint):
        # Create a new row for A corresponding to the additional constraint
        new_row = [0] * parent_node.number_of_variables
        for var, coeff in additional_constraint.expression.terms.items():
            var_index = parent_node.variables.index(var)  # Assuming self.variables is accessible and contains all variables including slacks
            new_row[var_index] = coeff

        # If the constraint is an inequality, add a new slack variable
        if additional_constraint.sense != '==':
            # Add a 1 or -1 for the slack variable at the end of the new row
            new_row.append(1 if additional_constraint.sense == '<=' else -1)
            # Add a 0 column for the slack variable in the existing rows of A
            new_A = np.hstack([parent_node.A, np.zeros((parent_node.A.shape[0], 1))])
            # Append the new row to A
            new_A = np.vstack([new_A, new_row])
            # Append 0 to c for the new slack variable
            new_c = np.append(parent_node.c, 0)
        else:
            new_A = np.vstack([parent_node.A, new_row])
            new_c = parent_node.c.copy()

        # Append the RHS of the constraint to b
        new_b = np.append(parent_node.b, additional_constraint.rhs)

        # Create and return the new node with updated A, b, c
        return Node(new_A, new_b, new_c, parent_node.basis_indexes[:], parent_node.non_basis_indexes[:], parent_node.variables[:], parent_node.constraints[:])


