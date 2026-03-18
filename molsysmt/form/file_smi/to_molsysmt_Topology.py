from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:smi')
@dep_digest('rdkit')
def to_molsysmt_Topology(item, skip_digestion=False):

    from .to_rdkit_Mol import to_rdkit_Mol
    from molsysmt.form.rdkit_Mol.to_molsysmt_Topology import to_molsysmt_Topology as rdkit_to_topology

    tmp_item = to_rdkit_Mol(item, skip_digestion=True)

    if isinstance(tmp_item, list):
        from molsysmt.basic.merge import merge
        topologies = [rdkit_to_topology(mol, skip_digestion=True) for mol in tmp_item]
        return merge(topologies, skip_digestion=True)

    return rdkit_to_topology(tmp_item, skip_digestion=True)
