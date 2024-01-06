import numpy as np
from numpy.linalg import inv
from my_mip.solver.node import Node


def primal_simplex(node:Node):  

    tolerance = 1e-5  # Tolerance level for numerical comparisons
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

        # Compute reduced costs
        reduced_cost = c_n - np.dot(pi, A_n)

        # Check for optimality using a tolerance level
        if all(np.round(reduced_cost,5) >= 0):
            keep_going = False
        else:
            # Determine entering variable
            entering_index = np.argmin(reduced_cost)

            # Ratio test to determine exiting variable
            
            ratio = current_solution / H[:, entering_index]
            ratio[(ratio < -tolerance) | (np.round(H[:, entering_index],5) <= 0)] = np.inf  # Set negative or very small ratios to infinity
                
            exiting_index = np.argmin(ratio)
            if ratio[exiting_index] == np.inf:
                # If all ratios are inf, the problem is unbounded
                node.status = "unbounded"
                return node

            # Update basis and non-basis indexes
            node.non_basis_indexes[entering_index], node.basis_indexes[exiting_index] = node.basis_indexes[exiting_index], node.non_basis_indexes[entering_index]


    # compute current optimal value 
    current_optimal_value = np.dot(pi,node.b)
    node.current_solution = current_solution
    node.current_optimal_value = current_optimal_value
    node.status = "solved"   
    node.H = H    
    return node
    
