import numpy as np
from my_mip.solver.constraints_and_var import Constraint, Variable, Expression
from my_mip.core.simplex_solvers.primal_simplex import primal_simplex
from my_mip.core.simplex_solvers.dual_simplex import dual_simplex
from my_mip.core.cutting_planes.gomory_cuts import find_gomory_cuts, add_gomory_cuts_to_model
from my_mip.solver.node import Node
from numpy.linalg import inv
import copy

M = 1e6  # Big M value
class BranchAndBound:
    def __init__(self):
        self.best_node = None
        self.best_objective = np.inf
        self.active_nodes = []

    def is_valid_solution(self, node):
        for i, var in enumerate(iterable=node.variables):
            if not(i in node.basis_indexes):
                continue
            position = node.basis_indexes.index(i)
            if var.vtype == 'integer':
                if np.round(node.current_solution[position],0)!=node.current_solution[position]:
                    return False
            elif var.vtype == 'binary':
                if not(np.isclose(node.current_solution[position],0) or np.isclose(node.current_solution[position],1)):
                    return False
        return True

    def compute_primal_dual_gap(self, node):
        return (node.current_optimal_value - self.best_objective)/np.abs(self.best_objective)

    def branch_and_bound(self, root_node):
        root_node = primal_simplex(root_node)
        if root_node.status == 'infeasible':
            print("no solution can be found")
            return self.best_solution, self.best_objective
        self.active_nodes.append(root_node)
        while self.active_nodes:
            current_node = self.select_next_node()
            current_node = self.solve_lp_relaxation(current_node)
            if current_node.current_optimal_value > self.best_objective or current_node.status == 'infeasible':
                # here we prune the node
                continue
            if self.is_valid_solution(current_node):
                self.update_best_solution(current_node)
            elif np.abs(self.compute_primal_dual_gap(current_node)) <= self.mip_gap:
                break
            else:
                self.branch(current_node)
        return self.best_node, self.best_objective

    def select_next_node(self):
        # Select the next node to explore
        # Adjust the implementation as per your requirements
        return self.active_nodes.pop()

    def update_best_solution(self, node):
        if node.current_optimal_value < self.best_objective:
            self.best_node = node
            self.best_objective = node.current_optimal_value


    def solve_lp_relaxation(self, node):
        # Find Gomory cuts
        gomory_cuts = find_gomory_cuts(node)
        # # Add cuts to the model
        node = add_gomory_cuts_to_model(node, gomory_cuts)
        # resolve
        node = dual_simplex(node)
        return node


    def branch(self, node: Node):
        """
        Branch on a variable at the given node.

        Args:
            node (Node): The node to branch on.
        """
        branching_var_index, branching_var_value = self.select_branching_variable(node)
        if branching_var_index is None:  # No suitable variable found for branching
            return

        var = node.variables[branching_var_index]

        # Handle branching for binary variables
        if var.vtype == 'binary':
            constraint_down = Constraint(Expression()._add_variable(var), sense='<=', rhs=0)  # Force binary var to 0
            constraint_up = Constraint(Expression()._add_variable(var), sense='>=', rhs=1)  # Force binary var to 1
        else:
            # Branch down (floor) and up (ceil) for integer variables
            constraint_down = Constraint(Expression()._add_variable(var), sense='<=', rhs=np.floor(branching_var_value))
            constraint_up = Constraint(Expression()._add_variable(var), sense='>=', rhs=np.ceil(branching_var_value))

        node_down = self.create_child_node(node, constraint_down)
        node_up = self.create_child_node(node, constraint_up)

        self.active_nodes.extend([node_down, node_up])


    def select_branching_variable(self, node: Node) -> tuple:
        """
        Select an integer or binary variable to branch on based on the current solution of the node.
        The chosen variable is the one furthest away from being an integer.

        Args:
            node (Node): The node to select a branching variable for.

        Returns:
            tuple: Index of the variable and its value in the current solution,
                or (None, None) if no suitable variable is found.
        """
        max_distance = 0
        selected_index = None
        selected_value = None
        for i, var in enumerate(iterable=node.variables):
            if var.vtype == "slack":
                continue
            if not (i in node.basis_indexes):
                continue
            position = node.basis_indexes.index(i)
            value = node.current_solution[position]

            if var.vtype in ['integer', 'binary']:
                distance = abs(value - np.round(value))
                if distance > max_distance:
                    max_distance = distance
                    selected_index = i
                    selected_value = value

        return (selected_index, selected_value) if selected_index is not None else (None, None)



    def create_child_node(self, parent_node: Node, additional_constraint: Constraint) -> Node:
        """
        Create a child node by adding an additional constraint to the parent node.

        Args:
            parent_node (Node): The parent node.
            additional_constraint (Constraint): The constraint to add for branching.

        Returns:
            Node: The new child node.
        """
        # Create a new row for A corresponding to the additional constraint
        new_row = [0] * len(parent_node.variables)
        for var, coeff in additional_constraint.expression.terms.items():
            var_index = parent_node.variables.index(var)
            new_row[var_index] = coeff if additional_constraint.sense in ['<=', '=='] else -coeff

        # Append the RHS of the constraint to b
        rhs = additional_constraint.rhs

        # Handle the addition of a slack or artificial variable
        if additional_constraint.sense != '==':
            # Inequality constraint: add a slack variable
            rhs = (rhs if additional_constraint.sense == '<=' else -rhs)
            new_row.append(1)  # Slack variable coefficient
            new_A = np.hstack([parent_node.A, np.zeros((parent_node.A.shape[0], 1))])
            new_A = np.vstack([new_A, new_row])
            new_c = np.append(parent_node.c, 0)  # Slack variable has zero cost
        else:
            # Equality constraint: add an artificial variable
            new_row.append(1)  # Artificial variable coefficient
            new_A = np.hstack([parent_node.A, np.zeros((parent_node.A.shape[0], 1))])
            new_A = np.vstack([new_A, new_row])
            new_c = np.append(parent_node.c, M)  # Artificial variable with a Big M penalty

        new_b = np.append(parent_node.b, rhs)
        child_node = Node(new_A, new_b, new_c, parent_node.basis_indexes[:], parent_node.non_basis_indexes[:], parent_node.variables[:], parent_node.constraints[:])

        if additional_constraint.sense != '==':
            new_slack_var = child_node.NewSlackVar()
            child_node.variables.append(new_slack_var)
            child_node.basis_indexes.append(len(new_c) - 1)
        else:
            new_artificial_var = child_node.NewSlackVar()
            child_node.variables.append(new_artificial_var)
            child_node.basis_indexes.append(len(new_c) - 1)


        child_node.status = "Not solved"
        child_node.current_solution = parent_node.current_solution.copy()
        child_node.current_optimal_value = parent_node.current_optimal_value

        return child_node

