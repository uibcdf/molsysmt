
def is_string_aminoacids1(string):

    from molsysmt.elements.group.aminoacid import aa1s

    output = False

    if string.isalnum():

        n_aa1 = 0

        for aa1 in string:
            if (aa1.upper() in aa1s):
                    n_aa1+=1

        if (n_aa1*1.0)/(len(string)*1.0) > 0.8:
            output = True

    return output

