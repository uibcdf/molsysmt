from molsysmt._private.exceptions import ArgumentError
from molsysmt.attribute import attributes

def digest_water_model(water_model, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(water_model, bool):
            return water_model
    elif caller=='molsysmt.basic.convert.convert':
        if water_model is None:
            return water_model
    elif caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        if water_model is None:
            return water_model

    if isinstance(water_model, str):
        if water_model in attributes['water_model']['values']:
            return water_model


    raise ArgumentError('water_model', value=water_model, caller=caller, message=None)

