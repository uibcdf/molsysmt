from molsysmt._private.exceptions import ArgumentError

def digest_water_model(water_model, caller=None):


    if caller=='molsysmt.basic.get.get':
        if isinstance(water_model, bool):
            return water_model

    if isinstance(water_model, str):
        from molsysmt.attribute import attributes
        if water_model in attributes['water_model']['values']:
            return water_model
    elif water_model is None:
        return None

    raise ArgumentError('water_model', value=water_model, caller=caller, message=None)

