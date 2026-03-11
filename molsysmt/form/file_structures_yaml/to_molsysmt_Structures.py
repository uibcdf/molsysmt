from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='file:structures_yaml')
def to_molsysmt_Structures(item, skip_digestion=False):
    from .to_molsysmt_StructuresDict import to_molsysmt_StructuresDict
    from molsysmt.form.molsysmt_StructuresDict.to_molsysmt_Structures import to_molsysmt_Structures as _to_structures

    tmp_item = to_molsysmt_StructuresDict(item, skip_digestion=True)
    return _to_structures(tmp_item, skip_digestion=True)
