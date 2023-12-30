import numpy as np
from numpy.linalg import inv
from my_mip.solver.node import Node



def find_gomory_cuts(node: Node):
    gomory_cuts = []

    A_b, A_n = node.A[:,node.basis_indexes], node.A[:,node.non_basis_indexes]
    A_b_inv = inv(A_b)
    H = np.dot(A_b_inv, A_n)

    for i, basic_value in enumerate(node.current_solution):
        # check if basic value is an int
        if np.round(basic_value,0)!=basic_value:
            cut = np.zeros(node.number_of_variables + len(gomory_cuts))
            cut_rhs = -(basic_value - np.floor(basic_value))
            for j, val in enumerate(H[i,:]):
                cut[node.non_basis_indexes[j]] = -(val - np.floor(val))
            gomory_cuts.append((cut, cut_rhs))
            break
    return gomory_cuts


def add_gomory_cuts_to_model(node: Node, gomory_cuts):
    for cut, cut_b in gomory_cuts:
        # Create a new column for the slack variable in A
        # This column is all zeros except for the last entry, which will be 1
        new_col = np.zeros((node.A.shape[0], 1))
        node.A = np.hstack([node.A, new_col])

        # Append the new cut row to A
        # The new row includes the cut and a 1 for the new slack variable
        new_row = np.append(cut, 1)  # Include the slack variable in the new row
        node.A = np.vstack([node.A, new_row])

        # Append the new element to b
        node.b = np.append(node.b, cut_b)

        # Add a new slack variable to the node, update c and variables list
        new_slack_var = node.NewSlackVar()
        node.c = np.append(node.c, 0)  # Assuming no cost for slack variables
        node.variables.append(new_slack_var)
        node.basis_indexes.append(node.A.shape[1] - 1)
    return node
