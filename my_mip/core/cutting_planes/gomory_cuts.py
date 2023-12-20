import numpy as np



def find_gomory_cuts(model):
    gomory_cuts = []
    for i, basic_value in enumerate(model.current_solution):
        # check if basic value is an int
        if np.round(basic_value,0)!=basic_value:
            cut = np.zeros(model.number_of_variables)
            cut_rhs = -(basic_value - np.floor(basic_value))
            for j, val in enumerate(model.H[i,:]):
                cut[model.non_basis_indexes[j]] = -(val - np.floor(val))
            gomory_cuts.append((cut, cut_rhs))
    return gomory_cuts


def add_gomory_cuts_to_model(model, gomory_cuts):
    for cut, cut_b in gomory_cuts:
        # Create a new column for the slack variable in A
        # This column is all zeros except for the last entry, which will be 1
        new_col = np.zeros((model.A.shape[0], 1))
        model.A = np.hstack([model.A, new_col])

        # Append the new cut row to A
        # The new row includes the cut and a 1 for the new slack variable
        new_row = np.append(cut, 1)  # Include the slack variable in the new row
        model.A = np.vstack([model.A, new_row])

        # Append the new element to b
        model.b = np.append(model.b, cut_b)

        # Add a new slack variable to the model, update c and variables list
        new_slack_var = model.NewSlackVar()
        model.c = np.append(model.c, 0)  # Assuming no cost for slack variables
        model.variables.append(new_slack_var)
        model.basis_indexes.append(len(model.variables) - 1)
    return
