from .name_and_type import name_to_type

def is_aminoacid(name):
    return (name in name_to_type)

