from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt.element.atom.get_atom_type import _get_atom_type_from_atom_name
from molsysmt.element.group.get_group_type import _get_group_type_from_group_name
import numpy as np

@digest(form='file:crd')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

        # EXT:
        #      (i10,2x,a)  natoms,'EXT'
        #      (2I10,2X,A8,2X,A8,3F20.10,2X,A8,2X,A8,F20.10)
        #      iatom,ires,resn,typr,x,y,z,segid,rid,wmain
        # standard:
        #      (i5) natoms
        #      (2I5,1X,A4,1X,A4,3F10.5,1X,A4,1X,A4,F10.5)
        #      iatom,ires,resn,typr,x,y,z,segid,orig_resid,wmain

    from molsysmt.native.topology import Topology

    tmp_item = Topology()

    atom_id = []
    atom_name = []
    atom_type = []
    group_index = []
    group_id = []
    group_name = []
    group_type = []
    chain_index = []
    chain_name = []

    extended = False

    former_group_id = -1
    former_chain_name = ''

    aux_group_index = -1
    aux_chain_index = -1

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
                atom_name.append(field[3])

                aux_group_id = int(field[1])
                aux_chain_name = field[7]

                if former_group_id!=aux_group_id:
                    former_group_id=aux_group_id
                    group_id.append(aux_group_id)
                    group_name.append(field[2])
                    aux_group_index += 1

                if former_chain_name!=aux_chain_name:
                    former_chain_name=aux_chain_name
                    chain_name.append(aux_chain_name)
                    aux_chain_index += 1

                group_index.append(aux_group_index)
                chain_index.append(aux_chain_index)

    if len(atom_id)!=n_atoms:
        raise ValueError

    for ii in atom_name:
        atom_type.append(_get_atom_type_from_atom_name(ii))

    for ii in group_name:
        group_type.append(_get_group_type_from_group_name(ii))

    n_groups = len(group_name)
    n_chains = len(chain_name)

    tmp_item.reset_atoms(n_atoms=n_atoms)
    tmp_item.reset_groups(n_groups=n_groups)
    tmp_item.reset_chains(n_chains=n_chains)

    tmp_item.atoms.atom_id = np.array(atom_id, dtype=int)
    tmp_item.atoms.atom_name = np.array(atom_name, dtype=object)
    tmp_item.atoms.atom_type = np.array(atom_type, dtype=object)
    tmp_item.atoms.group_index = np.array(group_index, dtype=int)
    tmp_item.atoms.chain_index = np.array(chain_index, dtype=int)
    tmp_item.groups.group_id = np.array(group_id, dtype=int)
    tmp_item.groups.group_name = np.array(group_name, dtype=object)
    tmp_item.groups.group_type = np.array(group_type, dtype=object)
    tmp_item.chains.chain_id = np.arange(n_chains, dtype=int)
    tmp_item.chains.chain_name = np.array(chain_name, dtype=object)

    del(atom_id, atom_name, atom_type,
        group_index, group_id, group_name, group_type,
        chain_index, chain_name)

    return tmp_item

