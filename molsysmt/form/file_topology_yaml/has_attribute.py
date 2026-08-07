from molsysmt._private.argdigest import arg_digest


@arg_digest(form='file:topology_yaml')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    from .to_molsysmt_TopologyDict import to_molsysmt_TopologyDict
    from molsysmt.form.molsysmt_TopologyDict.has_attribute import has_attribute as dict_has_attribute

    item = to_molsysmt_TopologyDict(molecular_system, skip_digestion=True)
    return dict_has_attribute(item, attribute=attribute, include_none=include_none, skip_digestion=True)
