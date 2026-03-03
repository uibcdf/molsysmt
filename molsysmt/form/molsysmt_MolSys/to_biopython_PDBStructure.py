from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_biopython_PDBStructure(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.basic import get
    from Bio.PDB.Structure import Structure
    from Bio.PDB.Model import Model
    from Bio.PDB.Chain import Chain
    from Bio.PDB.Residue import Residue
    from Bio.PDB.Atom import Atom
    import pyunitwizard as puw

    atom_names, atom_ids, elements = get(item, element='atom', selection=atom_indices, 
                                         name=True, id=True, type=True)
    res_names, res_ids = get(item, element='group', selection=atom_indices, name=True, id=True)
    chain_ids = get(item, element='chain', selection=atom_indices, id=True)
    
    coordinates = get(item, element='atom', selection=atom_indices, 
                      structure_indices=structure_indices, coordinates=True)
    
    if coordinates is not None:
        coords_val = puw.get_value(coordinates, to_unit='angstroms')
    else:
        import numpy as np
        coords_val = np.zeros((1, len(atom_names), 3))

    structure = Structure("MolSysMT")
    
    # We will build only the first model for now
    model = Model(0)
    structure.add(model)

    current_chain_id = None
    current_res_id = None
    
    for i in range(len(atom_names)):
        
        cid = str(chain_ids[i])
        if cid != current_chain_id:
            chain = Chain(cid)
            model.add(chain)
            current_chain_id = cid
            
        rid = int(res_ids[i])
        if rid != current_res_id:
            # BioPython res_id is a tuple (hetero, resseq, insertion_code)
            residue = Residue(('', rid, ' '), res_names[i], '')
            chain.add(residue)
            current_res_id = rid
            
        atom = Atom(atom_names[i], coords_val[0, i, :], 0.0, 1.0, ' ', 
                    atom_names[i], int(atom_ids[i]), element=elements[i])
        residue.add(atom)

    return structure
