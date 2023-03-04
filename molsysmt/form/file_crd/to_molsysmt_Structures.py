from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='file:crd')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

        # EXT:
        #      (i10,2x,a)  natoms,'EXT'
        #      (2I10,2X,A8,2X,A8,3F20.10,2X,A8,2X,A8,F20.10)
        #      iatom,ires,resn,typr,x,y,z,segid,rid,wmain
        # standard:
        #      (i5) natoms
        #      (2I5,1X,A4,1X,A4,3F10.5,1X,A4,1X,A4,F10.5)
        #      iatom,ires,resn,typr,x,y,z,segid,orig_resid,wmain

    from molsysmt.native.structures import Structures

    tmp_item = Structures()

    x = []
    y = []
    z = []

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
                x.append(float(field[4]))
                y.append(float(field[5]))
                z.append(float(field[6]))

    if len(x)!=n_atoms:
        raise ValueError

    coordinates = puw.quantity(np.expand_dims(np.column_stack([x,y,z]), axis=0), unit='angstroms', standardized=True)

    tmp_item.append_structures(structure_id=[0], coordinates=coordinates)

    del(x,y,z,coordinates)

    return tmp_item

def _to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)
