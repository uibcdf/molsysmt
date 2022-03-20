def is_list_or_tuple(obj):

    if type(obj) in [list, tuple]:
        return True
    else:
        return False

def list_to_csv_string(obj):

    return ",".join([str(ii) for ii in obj])

def list_to_ssv_string(obj):

    return " ".join([str(ii) for ii in obj])

def are_equal_sets(objects1, objects2):

    if not is_list_or_tuple(objects1):
        objects1=[objects1]
    if not is_list_or_tuple(objects2):
        objects2=[objects2]

    output = False
    if set(objects1)==set(objects2):
        output = True

    return output

