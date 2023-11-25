from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt.element.atom import get_atom_type_from_atom_name
from molsysmt.element.group.get_group_type import _get_group_type_from_group_name
import numpy as np

@digest(form='file:crd')
def to_molsysmt_TopologyOld(item, atom_indices='all', structure_indices='all'):

        # EXT:
        #      (i10,2x,a)  natoms,'EXT'
        #      (2I10,2X,A8,2X,A8,3F20.10,2X,A8,2X,A8,F20.10)
        #      iatom,ires,resn,typr,x,y,z,segid,rid,wmain
        # standard:
        #      (i5) natoms
        #      (2I5,1X,A4,1X,A4,3F10.5,1X,A4,1X,A4,F10.5)
        #      iatom,ires,resn,typr,x,y,z,segid,orig_resid,wmain

    from molsysmt.native.topology_old import TopologyOld

    tmp_item = TopologyOld()

    atom_index = []
    atom_id = []
    atom_name = []
    atom_type = []
    group_index = []
    group_id = []
    group_name = []
    group_type = []
    chain_index = []
    chain_id = []
    bfactor = []

    extended = False

    with open(item) as fff:
        for line in fff:
            if line.strip().startswith('*') or line.strip() == "":
                continue
            field = line.split()
            if len(field)==1:
                n_atoms = int(field[0])
            elif len(field)==2:
                n_atoms = int(field[0])
                extended = True
            else:
                atom_id.append(int(field[0]))
                group_id.append(int(field[1]))
                group_name.append(field[2])
                atom_name.append(field[3])
                chain_id.append(field[7])
                bfactor.append(float(field[9]))

    if len(atom_id)!=n_atoms:
        raise ValueError

    for ii in atom_name:
        atom_type.append(get_atom_type_from_atom_name(ii))

    counter = 0
    prev = group_id[0]
    for ii in group_id:
        if ii != prev:
            prev = ii
            counter += 1
        group_index.append(counter)

    for ii in group_name:
        group_type.append(_get_group_type_from_group_name(ii))

    counter = 0
    prev = chain_id[0]
    for ii in chain_id:
        if ii != prev:
            prev = ii
            counter += 1
        chain_index.append(counter)

    atom_index = np.arange(0, n_atoms, dtype=int)
    atom_id = np.array(atom_id, dtype=int)
    atom_name = np.array(atom_name, dtype=object)
    atom_type = np.array(atom_type, dtype=object)
    group_index = np.array(group_index, dtype=int)
    group_id = np.array(group_id, dtype=int)
    group_name = np.array(group_name, dtype=object)
    group_type = np.array(group_type, dtype=object)
    chain_index = np.array(chain_index, dtype=int)
    chain_id = np.array(chain_id, dtype=object)
    bfactor = puw.quantity(np.array(bfactor), unit='angstroms**2', standardized=True)

    tmp_item.atoms_dataframe["atom_index"] = atom_index
    tmp_item.atoms_dataframe["atom_name"] = atom_name
    tmp_item.atoms_dataframe["atom_id"] = atom_id
    tmp_item.atoms_dataframe["atom_type"] = atom_type
    tmp_item.atoms_dataframe["b_factor"] = puw.get_value(bfactor)
    tmp_item.atoms_dataframe["group_index"] = group_index
    tmp_item.atoms_dataframe["group_name"] = group_name
    tmp_item.atoms_dataframe["group_id"] = group_id
    tmp_item.atoms_dataframe["group_type"] = group_type
    tmp_item.atoms_dataframe["chain_index"] = chain_index
    tmp_item.atoms_dataframe["chain_id"] = chain_id

    ## nan to None

    tmp_item._nan_to_None()

    del(atom_index, atom_id, atom_name, atom_type,
        group_index, group_id, group_name, group_type,
        chain_index, chain_id, bfactor)

    return tmp_item

