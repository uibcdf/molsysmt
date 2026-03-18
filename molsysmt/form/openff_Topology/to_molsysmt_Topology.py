from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openff.Topology')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.openff_Molecule.to_molsysmt_Topology import to_molsysmt_Topology as mol_to_topology

    molecules = list(item.molecules)

    if len(molecules) == 1:
        tmp_item = mol_to_topology(molecules[0], skip_digestion=True)
    else:
        from molsysmt.basic.merge import merge
        topologies = [mol_to_topology(mol, skip_digestion=True) for mol in molecules]
        tmp_item = merge(topologies, skip_digestion=True)

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
