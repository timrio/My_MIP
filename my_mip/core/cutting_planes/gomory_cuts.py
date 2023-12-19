def find_gomory_cuts():
    gomory_cuts = []
    for i, basic_value in enumerate(current_solution):
        # check if basic value is an int
        if np.round(basic_value,0)!=basic_value:
            new_cut = {}
            new_cut["b"] = -(basic_value - np.floor(basic_value))
            for j, val in enumerate(H[i,:]):
                new_cut[non_basis_indexes[j]] = -(val - np.floor(val))
            gomory_cuts.append(new_cut)
    return gomory_cuts


def add_cuts(cuts, A, b, c, basis_indexes, number_of_variables):
    for cut in cuts:
        # add the constraint
        new_line = np.zeros(A.shape[1])
        new_b = None
        for k, v in cut.items():
            if k == "b":
                new_b = v
                continue
            new_line[k] = v


        A = np.r_[A, [new_line]]
        new_col = np.zeros(A.shape[0])
        new_col[-1] = 1
        A = np.c_[A, new_col]
        #update b
        b = np.append(b, new_b)
        # update c
        c = np.append(c, 0)
        basis_indexes.append(number_of_variables-1)
    return 