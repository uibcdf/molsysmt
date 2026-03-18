from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='string:smiles')
@dep_digest('rdkit')
def to_molsysmt_Topology(item, skip_digestion=False):

    from .to_rdkit_Mol import to_rdkit_Mol
    from molsysmt.form.rdkit_Mol.to_molsysmt_Topology import to_molsysmt_Topology as rdkit_to_topology

    tmp_item = to_rdkit_Mol(item, skip_digestion=True)

    return rdkit_to_topology(tmp_item, skip_digestion=True)
