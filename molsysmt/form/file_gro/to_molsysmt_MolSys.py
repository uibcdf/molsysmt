from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='file:gro')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys

    with open(item,'r') as fff:
        
        header = fff.readline()
        n_atoms = int(fff.readline())
    
        atom_id_array = np.ndarray(shape=[n_atoms], dtype=int)
        atom_name_array = np.ndarray(shape=[n_atoms], dtype=object)
        group_index_array = np.ndarray(shape=[n_atoms], dtype=object)
        group_id_array = []
        group_name_array = []
    
        coordinates = np.ndarray(shape=[n_atoms,3], dtype=float)
        velocities = None
    
        check_velocities = True
        with_velocities = False
        group_index = -1
        former_group_id = -1
        
        for ii in range(n_atoms):
            line = fff.readline()
    
            group_id = int(line[:5])
            if former_group_id!=group_id:
                group_id_array.append(group_id)
                group_name_array.append(line[5:10].strip())
                group_index+=1
                former_group_id=group_id
    
            atom_id_array[ii]=int(line[15:20])
            atom_name_array[ii]=line[10:15].strip()
            group_index_array[ii]=group_index
    
            coordinates[ii,:]=[float(line[20:28]), float(line[28:36]), float(line[36:44])]
    
            if check_velocities:
                if len(line)>68:
                    velocities = np.ndarray(shape=[n_atoms,3], dtype=float)
                    with_velocities = True
                    check_velocities = False
    
            if with_velocities:
                velocities[ii,:]=[float(line[44:52]), float(line[52:60]), float(line[60:68])]
    
        box_values = fff.readline().split()
        box = np.zeros([3,3], dtype=float)
    
        box[0,0] = float(box_values[0])
        box[1,1] = float(box_values[1])
        box[2,2] = float(box_values[2])
        
        if len(box_values)==9:
            box[0,1] = float(box_values[3])
            box[0,2] = float(box_values[4])
            box[1,0] = float(box_values[5])
            box[1,2] = float(box_values[6])
            box[2,0] = float(box_values[7])
            box[2,1] = float(box_values[8])
 
    group_id_array = np.array(group_id_array, dtype=int)
    group_name_array = np.array(group_name_array, dtype=object)
    n_groups = group_id_array.shape[0]

    tmp_item = MolSys()

    tmp_item.topology.reset_atoms(n_atoms=n_atoms)
    tmp_item.topology.reset_groups(n_groups=n_groups)
    tmp_item.topology.reset_chains(n_chains=1)

    tmp_item.topology.atoms.atom_id = atom_id_array
    tmp_item.topology.atoms.atom_name = atom_name_array
    tmp_item.topology.atoms.group_index = group_index_array
    tmp_item.topology.atoms.chain_index = np.zeros(shape=[n_atoms], dtype=int)

    tmp_item.topology.rebuild_atoms(redefine_ids=False, redefine_types=True)

    tmp_item.topology.groups.group_id = group_id_array
    tmp_item.topology.groups.group_name = group_name_array

    tmp_item.topology.rebuild_groups(redefine_ids=False, redefine_types=True)

    tmp_item.topology.chains.iloc[0,0] = 0
    tmp_item.topology.chains.iloc[0,1] = 'A'

    coordinates=puw.quantity(coordinates,'nm')
    box=puw.quantity(box,'nm')
    if with_velocities:
        velocities=puw.quantity(velocities,'nm/ps')
        
    tmp_item.structures.append(coordinates=coordinates, box=box, velocities=velocities)

    #tmp_item.topology.rebuild_chains(redefine_ids=False, redefine_types=True)

    return tmp_item

