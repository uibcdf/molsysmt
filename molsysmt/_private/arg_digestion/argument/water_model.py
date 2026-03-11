from molsysmt._private.smonitor import ArgumentError

def digest_water_model(water_model, caller=None):


    if caller=='molsysmt.basic.get.get':
        if isinstance(water_model, bool):
            return water_model

    if isinstance(water_model, str):
        from molsysmt.attribute import attributes
        values = attributes['water_model']['values']
        for value in values:
            if water_model.lower() == value.lower():
                return value
    elif water_model is None:
        return None

    raise ArgumentError('water_model', value=water_model, caller=caller, message=None)

