
def getting(item, element='atom', indices=None, ids=None, **kwargs):

    result=[]
    args = [ii for ii in kwargs if kwargs[ii]]

    if element=='atom':

        for option in args:
            if option=='n_atoms':
                raise NotImplementedError
            elif option in ['atom_name', 'name']:
                raise NotImplementedError
            elif option in ['atom_index', 'index']:
                raise NotImplementedError
            elif option in ['atom_id', 'id']:
                raise NotImplementedError
            elif option in ['atom_type', 'type']:
                raise NotImplementedError
            elif option=='n_residues':
                raise NotImplementedError
            elif option=='residue_name':
                raise NotImplementedError
            elif option=='residue_index':
                raise NotImplementedError
            elif option=='residue_id':
                raise NotImplementedError
            elif option=='chain_index':
                raise NotImplementedError
            elif option=='chain_id':
                raise NotImplementedError
            elif option=='n_frames':
                raise NotImplementedError
            elif option=='n_chains':
                raise NotImplementedError
            elif option=='n_molecules':
                raise NotImplementedError
            elif option=='n_aminoacids':
                raise NotImplementedError
            elif option=='n_nucleotides':
                raise NotImplementedError
            elif option=='n_waters':
                raise NotImplementedError
            elif option=='n_ions':
                raise NotImplementedError
            elif option=='mass':
                raise NotImplementedError
            elif option=='net_mass':
                raise NotImplementedError
            elif option=='charge':
                raise NotImplementedError
            elif option=='net_charge':
                raise NotImplementedError
            elif option=='n_degrees_of_freedom':
                raise NotImplementedError
            elif option=='bonded_atoms':
                raise NotImplementedError
            elif option=='bonds':
                raise NotImplementedError
            elif option=='graph':
                raise NotImplementedError
            elif option=='molecules':
                raise NotImplementedError
            elif option=='molecule_type':
                raise NotImplementedError
            elif option=='coordinates':
                tmp_unit = item.positions.unit
                tmp_positions = [item.positions[ii]._value for ii in indices]
                result.append(tmp_positions*tmp_unit)
            else:
                raise NotImplementedError

    elif element=='residue':

        for option in args:
            if option=='n_atoms':
                raise NotImplementedError
            elif option=='atom_name':
                raise NotImplementedError
            elif option=='atom_type':
                raise NotImplementedError
            elif option=='n_residues':
                raise NotImplementedError
            elif option=='residue_name':
                raise NotImplementedError
            elif option=='residue_index':
                raise NotImplementedError
            elif option=='residue_id':
                raise NotImplementedError
            elif option=='chain_index':
                raise NotImplementedError
            elif option=='chain_id':
                raise NotImplementedError
            elif option=='n_frames':
                raise NotImplementedError
            elif option=='n_chains':
                raise NotImplementedError
            elif option=='n_molecules':
                raise NotImplementedError
            elif option=='n_aminoacids':
                raise NotImplementedError
            elif option=='n_nucleotides':
                raise NotImplementedError
            elif option=='n_waters':
                raise NotImplementedError
            elif option=='n_ions':
                raise NotImplementedError
            elif option=='masses':
                raise NotImplementedError
            elif option=='charge':
                raise NotImplementedError
            elif option=='bonded_atoms':
                raise NotImplementedError
            elif option=='bonds':
                raise NotImplementedError
            elif option=='graph':
                raise NotImplementedError
            elif option=='molecules':
                raise NotImplementedError
            elif option=='molecule_type':
                raise NotImplementedError
            elif option=='coordinates':
                raise NotImplementedError
            else:
                raise NotImplementedError

    elif element=='molecule':
        raise NotImplementedError

    elif element=='chain':

        for option in args:
            if option=='n_atoms':
                raise NotImplementedError
            elif option=='atom_name':
                raise NotImplementedError
            elif option=='atom_type':
                raise NotImplementedError
            elif option=='n_residues':
                raise NotImplementedError
            elif option=='residue_name':
                raise NotImplementedError
            elif option=='residue_index':
                raise NotImplementedError
            elif option=='residue_id':
                raise NotImplementedError
            elif option=='chain_index':
                raise NotImplementedError
            elif option=='chain_id':
                raise NotImplementedError
            elif option=='n_frames':
                raise NotImplementedError
            elif option=='n_chains':
                raise NotImplementedError
            elif option=='n_molecules':
                raise NotImplementedError
            elif option=='n_aminoacids':
                raise NotImplementedError
            elif option=='n_nucleotides':
                raise NotImplementedError
            elif option=='n_waters':
                raise NotImplementedError
            elif option=='n_ions':
                raise NotImplementedError
            elif option=='masses':
                raise NotImplementedError
            elif option=='charge':
                raise NotImplementedError
            elif option=='bonded_atoms':
                raise NotImplementedError
            elif option=='bonds':
                raise NotImplementedError
            elif option=='graph':
                raise NotImplementedError
            elif option=='molecules':
                raise NotImplementedError
            elif option=='molecule_type':
                raise NotImplementedError
            elif option=='coordinates':
                raise NotImplementedError
            else:
                raise NotImplementedError

    elif element=='trajectory':
        raise NotImplementedError

    elif element=='system':

        for option in args:
            if option=='n_atoms':
                raise NotImplementedError
            elif option=='charge':
                raise NotImplementedError
            elif option=='net_charge':
                raise NotImplementedError
            elif option=='n_degrees_of_freedom':
                raise NotImplementedError
            else:
                raise NotImplementedError

    else:
        raise NotImplementedError


    if len(result)==1:
        return result[0]
    else:
        return result

