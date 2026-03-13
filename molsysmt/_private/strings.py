from molsysmt._private.smonitor import ArgumentError, FormatError
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError

def get_parenthesis(string):

    output = []
    initial_positions = []

    for ii in range(len(string)):
        if string[ii]=='(':
            initial_positions.append(ii)
        elif string[ii]==')':
            in_parenthesis = string[(initial_positions[-1]+1):ii]
            output.append(in_parenthesis)
            initial_positions = initial_positions[:-1]

    if len(initial_positions)>0:
        from molsysmt._private.smonitor import FormatError
        raise FormatError("Missing opened parenthesis in string", caller="molsysmt._private.strings")

    return output


