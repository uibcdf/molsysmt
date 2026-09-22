#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################


import types

form = "string:aminoacids3"
# List of functions to be imported
__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
