from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
@dep_digest('MDAnalysis')
def to_MDAnalysis_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.parse()

    if atom_indices != 'all':
        from molsysmt.form.MDAnalysis_Topology.extract import extract as extract_MDAnalysis_Topology
        tmp_item = extract_MDAnalysis_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
