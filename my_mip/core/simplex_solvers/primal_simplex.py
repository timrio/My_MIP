def simplex_iteration(A,b,c, basis_indexes, non_basis_indexes):   
    if any(b<0):           
        print("cannot find initial basis")
        return False

    keep_going = True

    while keep_going:
        A_b, A_n = A[:,basis_indexes], A[:,non_basis_indexes]
        c_b, c_n = c[basis_indexes], c[non_basis_indexes]

        if np.linalg.det(A_b) == 0:
            return 'matrice non inversible'

        A_b_inv = inv(A_b)
        pi = np.dot(c_b,A_b_inv) 
        current_solution = np.dot(A_b_inv,b)
        
        # express x basis according to xn
        # x_b = x_b_opt - H @ x_n
        H = np.dot(A_b_inv, A_n)

        # compute reduced costs
        reduced_cost = c_n - np.dot(pi, A_n)

        if all(reduced_cost >= 0):
            keep_going = False

        else:
            # we need find entering and exiting variable
            entering_index = np.argmin(reduced_cost)
            ratio = (current_solution / H[:, entering_index])
            
            # Avoid division by zero in case of non-positive entries in H[:, entering_index]
            ratio[(ratio < 0)] = np.inf
            exiting_index = np.argmin([value if H[i, entering_index]>0 else np.inf for i,value in enumerate(ratio)])

            # permute entering and exiting values
            non_basis_indexes[entering_index], basis_indexes[exiting_index] = basis_indexes[exiting_index],non_basis_indexes[entering_index]

    # compute current optimal value 
    current_optimal_value = np.dot(pi,b)
    return