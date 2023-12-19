def dual_simplex_python(A,b,c, basis_indexes, non_basis_indexes):
    # initialize dual simplex 
    keep_going = True
    while keep_going:
        
        A_b, A_n = A[:,basis_indexes], A[:,non_basis_indexes]
        c_b, c_n = c[basis_indexes], c[non_basis_indexes]

        A_b_inv = inv(A_b)
        pi = np.dot(c_b,A_b_inv) 
        current_solution = np.dot(A_b_inv,b)
        
        # express x basis according to xn
        # x_b = x_b_opt - H @ x_n
        H = np.dot(A_b_inv, A_n)

        # compute reduced costs
        reduced_cost = c_n - np.dot(pi, A_n)

        if all(current_solution>=0):
            keep_going = False
        else:
            # find the variable that will leave, the basis, this is the one the first negative beta
            min_val = np.inf
            exiting_index = None
            for i in range(number_of_constraints):
                if current_solution[i] < min_val and current_solution[i]<0:
                    exiting_index = i
                    min_val = current_solution[i]
                    break
            if all(val>=0 for val in H[exiting_index,:]):
                print("model infeasible")
                break
            else:
                # we choose the variable that enters the basis
                min_val = np.inf
                entering_index = None
                for i in range(number_of_variables-number_of_constraints):
                    if H[exiting_index,i] < 0 and reduced_cost[i]/np.abs(H[exiting_index,i]) < min_val:
                        min_val = reduced_cost[i]/np.abs(H[exiting_index,i]) 
                        entering_index = i 

                # permute entering and exiting values
                non_basis_indexes[entering_index], basis_indexes[exiting_index] = basis_indexes[exiting_index],non_basis_indexes[entering_index]
    # compute current optimal value 
    current_optimal_value = np.dot(pi,b)
    return