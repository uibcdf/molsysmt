
def singular(argument):

    if argument.endswith('s'):
        if argument=="atoms":
            return "atom"
        elif argument=="residues":
            return "residue"
        elif argument=="chains":
            return "chain"
        elif argument=="molecules":
            return "molecule"
        elif argument=="atom_names":
            return "atom_name"
        elif argument=="atom_names":
            return "atom_name"
        elif argument=="atom_indices":
            return "atom_index"
        elif argument=="atom_ids":
            return "atom_id"
        elif argument=="residue_names":
            return "residue_name"
        elif argument=="residue_types":
            return "residue_type"
        elif argument=="molecule_types":
            return "molecule_type"

    return argument
