
def is_string_aminoacids3(string):

    output = False

    if string.isalnum():

        import re
        from molsysmt.elements.groups.aminoacid import name as aminoacid_name
        from molsysmt.elements.groups.water import name as water_name

        if len(string)%3==0:
            n_aa3 = 0
            aa3_list = re.findall('...', string)
            for aa3 in aa3_list:
                if (aa3.upper() in aminoacid_name) or (aa3.upper() in water_name):
                    n_aa3+=1
            if (n_aa3*1.0)/(len(aa3_list)*1.0) > 0.8:
                output = True

    return output

