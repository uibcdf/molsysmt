
def is_molsysmt_TrajectoryDict(item):

    output = False

    if type(item) is dict:

        from molsysmt.native.trajectory_dict import trajectory_parameters

        keys = set(item.keys())
        output = (keys <= trajectory_parameters)

    return output

