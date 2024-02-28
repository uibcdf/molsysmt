from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = ""

    tp=item.topology
    st=item.structures

    for ii in range(item.topology.atoms.shape[0]):
        line = f"{'ATOM':<6}{[i]:>5} {tp.atoms[i]:<4}" \
               f"{' ':1}{residue_names[i]:>3} {' ':1}{chain_ids[i]:>1}" \
               f"{residue_numbers[i]:>4}{' ':1}   {x_coords[i]:>8.3f}" \
               f"{y_coords[i]:>8.3f}{z_coords[i]:>8.3f}{occupancies[i]:>6.2f}" \
               f"{temp_factors[i]:>6.2f}          {element_symbols[i]:>2}"
        file.write(line + '\n')
        line = f"ATOM  {atom_numbers[i]:5d} {atom_names[i]:^4}{residue_names[i]:>3} {chain_ids[i]}{residue_numbers[i]:4d}    {x_coords[i]:8.3f}{y_coords[i]:8.3f}{z_coords[i]:8.3f}{occupancies[i]:6.2f}{temp_factors[i]:6.2f}           {atom_names[i][0]}"
        # Escribe la línea en el archivo
        file.write(line + '\n')

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from ..openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = openmm_Topology_to_string_pdb_text(tmp_item, coordinates=coordinates, skip_digestion=True)

    return tmp_item

