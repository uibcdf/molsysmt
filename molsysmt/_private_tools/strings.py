
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
        raise ValueError('There must be an opened parenthesis in the string')

    return output


