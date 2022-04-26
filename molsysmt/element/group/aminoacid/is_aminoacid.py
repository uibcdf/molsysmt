from .get_aminoacid_type_from_name import name_to_type

def is_aminoacid(name):
    return (name in name_to_type)

