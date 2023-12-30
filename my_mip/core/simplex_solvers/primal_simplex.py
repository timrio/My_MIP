import numpy as np
from numpy.linalg import inv
from my_mip.solver.node import Node


def primal_simplex(node:Node, artificial_vars = None):  

    keep_going = True

    while keep_going:
        A_b, A_n = node.A[:,node.basis_indexes], node.A[:,node.non_basis_indexes]
        c_b, c_n = node.c[node.basis_indexes], node.c[node.non_basis_indexes]

        A_b_inv = inv(A_b)
        pi = np.dot(c_b,A_b_inv) 
        current_solution = np.dot(A_b_inv,node.b)
        
        # express x basis according to xn
        # x_b = x_b_opt - H @ x_n
        H = np.dot(A_b_inv, A_n)

        # compute reduced costs
        reduced_cost = c_n - np.dot(pi, A_n)
        if all(np.round(reduced_cost,5) >= 0):
            keep_going = False

        else:
            # we need find entering and exiting variable
            entering_index = np.argmin(reduced_cost)
            ratio = (current_solution / H[:, entering_index])
            ratio[(ratio < 0) | (np.round(H[:, entering_index],5) <= 0)] = np.inf

            # Check for ties and prefer artificial variables to leave the basis
            min_ratio = np.min(ratio)
            tied_indices = [i for i, r in enumerate(ratio) if r == min_ratio]
            
            # Prefer artificial variable if in a tie
            if artificial_vars is not None:
                exiting_candidates = [i for i in tied_indices if i in artificial_vars and np.round(H[i, entering_index],5) > 0]
                if exiting_candidates:
                    exiting_index = min(exiting_candidates)  # Prefer artificial variable
                else:
                    exiting_index = min(i for i in tied_indices if np.round(H[i, entering_index],5) > 0)
            else:
                exiting_index = min(i for i in tied_indices if np.round(H[i, entering_index],5) > 0)

            # permute entering and exiting values
            node.non_basis_indexes[entering_index], node.basis_indexes[exiting_index] = node.basis_indexes[exiting_index],node.non_basis_indexes[entering_index]

    # compute current optimal value 
    current_optimal_value = np.dot(pi,node.b)
    node.current_solution = current_solution
    node.current_optimal_value = current_optimal_value
    node.status = "solved"   
    node.H = H    
    return node
    
