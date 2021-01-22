def is_list_or_tuple(obj):

    if type(obj) in [list, tuple]:
        return True
    else:
        return False

def list_to_csv_string(list):

    return ",".join([str(ii) for ii in list])

def list_to_ssv_string(list):

    return " ".join([str(ii) for ii in list])



