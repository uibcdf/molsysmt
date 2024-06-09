from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt import pyunitwizard as puw
import numpy as np
import sys

if sys.version_info[1]==10:
    from importlib.resources import files
    def path(package, file):
        return files(package).joinpath(file)
elif sys.version_info[1] in (8,9):
    from pathlib import PurePath
    parent = PurePath(__file__).parent
    def path(package, file):
        data_dir = package.split('.')[-1]
        return parent.joinpath('../data/'+data_dir+'/'+file).__str__()

@digest()
def make_water_box(box, form='molsysmt.MolSys'):

    from molsysmt.native import MolSys
    from molsysmt.basic import convert
    from molsysmt.form.file_gro import to_molsysmt_Structures

    box = puw.get_value(box[0], to_unit='nm')
    inv_box = np.linalg.inv(box)

    aux_item = to_molsysmt_Structures(path('molsysmt.data.gro','spc216.gro'))
    tile = puw.get_value(aux_item.coordinates[0], to_unit='nm')
    length_tile = 1.86206 # nm
    tile += length_tile/2.0
    del(aux_item)

    Os_indices = np.arange(0,216)*3

    n_tiles_x = np.ceil(box[0,0]/length_tile).astype(int)
    n_tiles_y = np.ceil(box[1,1]/length_tile).astype(int)
    n_tiles_z = np.ceil(box[2,2]/length_tile).astype(int)

    new_coors=[]

    for ii in range(n_tiles_x):
        for jj in range(n_tiles_y):
            for kk in range(n_tiles_z):

                aux_tile = tile.copy()
                aux_tile[:,0] += ii*length_tile
                aux_tile[:,1] += jj*length_tile
                aux_tile[:,2] += kk*length_tile

                coors_Os = aux_tile[Os_indices]
                aux = inv_box@coors_Os.transpose()
                mask = np.all(aux<1.0, axis=0)
                new_coors.append(aux_tile[np.repeat(mask,3),:])

    new_coors = np.concatenate(new_coors)

    del(tile, aux_tile, inv_box)

    n_atoms = new_coors.shape[0]
    n_waters = int(n_atoms/3)

    output = MolSys(n_atoms=n_atoms, n_groups=n_waters, n_components=n_waters, n_molecules=n_waters,
                    n_entities=1, n_chains=1, n_bonds=2*n_waters, skip_digestion=True) 

    output.structures.box = puw.quantity(box[np.newaxis,:,:], 'nm')
    output.structures.coordinates = puw.quantity(new_coors[np.newaxis,:,:], 'nm')
    output.structures.box = puw.standardize(output.structures.box)
    output.structures.coordinates = puw.standardize(output.structures.coordinates)
    output.structures.n_atoms = n_atoms
    output.structures.n_structures =1

    del(new_coors, box)

    output.topology.atoms['atom_id'] = np.arange(n_atoms)
    output.topology.atoms['atom_name'] = np.tile(['OW','HW1','HW2'], n_waters)
    output.topology.atoms['atom_type'] = np.tile(['O','H','H'], n_waters)
    output.topology.atoms['group_index'] = np.repeat(np.arange(n_waters), 3)
    output.topology.atoms['chain_index'] = 0
    output.topology.groups['group_id'] = np.arange(n_waters)
    output.topology.groups['group_name'] = 'WAT'
    output.topology.groups['group_type'] = 'water'
    output.topology.groups['component_index'] = np.arange(n_waters)
    output.topology.components['component_id'] = np.arange(n_waters)
    output.topology.components['component_name'] = 'water'
    output.topology.components['component_type'] = 'water'
    output.topology.components['molecule_index'] = np.arange(n_waters)
    output.topology.molecules['molecule_name'] = 'water'
    output.topology.molecules['molecule_id'] = np.arange(n_waters)
    output.topology.molecules['molecule_type'] = 'water'
    output.topology.molecules['entity_index'] = 0
    output.topology.entities['entity_name'] = 'water'
    output.topology.entities['entity_id'] = 0
    output.topology.entities['entity_type'] = 'water'
    output.topology.chains['chain_name'] = 'A'
    output.topology.chains['chain_id'] = 0
    output.topology.chains['chain_type'] = 'water'

    aux = np.zeros(n_waters*2, dtype='int')
    mask = np.arange(0,n_waters*2,2)
    aux[mask] = np.arange(1,n_atoms,3)
    mask = np.arange(1,n_waters*2,2)
    aux[mask] = np.arange(2,n_atoms,3)

    output.topology.bonds['atom1_index']=np.repeat(np.arange(n_waters)*3,2)
    output.topology.bonds['atom2_index']=aux
    output.topology.bonds._remove_empty_columns()

    del(aux, mask)

    return output

