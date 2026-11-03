from molsysmt.attribute import attributes as _catalogue
from molsysmt.form.molsysmt_MolSys.attributes import attributes as _native

attributes = dict(_native)


for _name, _definition in _catalogue.items():
    if _definition["mechanical"] and not _definition["chemical_state"]:
        attributes[_name] = False
