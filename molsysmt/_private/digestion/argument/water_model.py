from molsysmt._private.exceptions import ArgumentError

def digest_water_model(water_model, caller=None):

    if isinstance(water_model, str):
        return water_model

    raise ArgumentError('water_model', value=water_model, caller=caller, message=None)

