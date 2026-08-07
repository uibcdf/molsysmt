from molsysmt._private.argdigest import arg_digest
from smonitor import signal
import numpy as np

@signal(tags=['api', 'topology'])
@arg_digest()
def get_dihedral_quartets(molecular_system, with_blocks=False, selection='all',
                               syntax='MolSysMT', **kwargs):
    """
    Finding atom quartets that define standard dihedral angles.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    with_blocks : bool, default False
        If True, also return covalent blocks after severing the central bond.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atom selection to restrict the search.
    syntax : str, default 'MolSysMT'
        Selection syntax for string selections.
    **kwargs
        Flags indicating which dihedrals to compute (e.g., `phi=True`, `psi=True`, `chi1=True`, ...).

    Returns
    -------
    list
        Quartets of atom indices for the requested dihedrals (list of lists).
    list, optional
        If `with_blocks=True`, the covalent blocks obtained after removing the central bond
        of each quartet: one entry per quartet, each a list of sets of atom indices. The
        two sets of a quartet are the groups of atoms that move apart when that dihedral
        angle is rotated. This is ragged on purpose and is not a NumPy array.

    Notes
    -----
    - Uses `get_covalent_paths` to assemble quartets for each requested dihedral type.

    .. versionadded:: 1.0.0
    """

    # phi, psi, omega, chi1, chi2, chi3, chi4, chi5

    from molsysmt.basic import get
    from . import get_covalent_blocks, get_covalent_paths

    dihedral_angles = []
    for key in kwargs.keys():
        if kwargs[key]:
            dihedral_angles.append(key)

    all_quartets = []
    all_blocks = []

    for dihedral_angle in dihedral_angles:

        if dihedral_angle=='phi':
            path=['atom_name=="C"', 'atom_name=="N"', 'atom_name=="CA"', 'atom_name=="C"']
        elif dihedral_angle=='psi':
            path=['atom_name=="N"', 'atom_name=="CA"', 'atom_name=="C"', 'atom_name=="N"']
        elif dihedral_angle=='omega':
            path=['atom_name==["CA","CH3"]', 'atom_name=="C"', 'atom_name=="N"', 'atom_name==["CA","CH3"]']
        elif dihedral_angle=='chi1':
            path=['atom_name=="N"','atom_name=="CA"','atom_name=="CB"', 'atom_name==["CG","CG1","OG","OG1","SG"]'] # flexible but PRO
        elif dihedral_angle=='chi2':
            path=['atom_name=="CA"','atom_name=="CB"', 'atom_name==["CG","CG1"]', 'atom_name==["CD","CD1","SD","OD1","ND1"]'] # flexible but PRO
        elif dihedral_angle=='chi3':
            path=['atom_name=="CB"', 'atom_name=="CG"', 'atom_name==["CD","SD"]','atom_name==["NE","OE1","CE"]']
        elif dihedral_angle=='chi4':
            path=['atom_name=="CG"', 'atom_name=="CD"', 'atom_name==["NE","CE"]', 'atom_name==["CZ","NZ"]']
        elif dihedral_angle=='chi5':
            path=['atom_name=="CD"', 'atom_name=="NE"', 'atom_name=="CZ"', 'atom_name=="NH1"']

        quartets = get_covalent_paths(molecular_system, path=path, selection=selection, syntax=syntax)

        all_quartets.append(quartets)

        if with_blocks:

            n_quartets = quartets.shape[0]

            blocks = []

            for quartet_index in range(n_quartets):

                quartet = quartets[quartet_index]
                component_index = get(molecular_system, element='atom', selection=quartet[1], component_index=True)[0]
                component_atom_indices = get(molecular_system, element='component', selection=component_index,
                                             atom_index=True)[0]
                tmp_blocks = get_covalent_blocks(molecular_system, remove_bonds=[quartet[1],
                    quartet[2]], output_type='sets')
                blocks_in_component = []
                for block in tmp_blocks:
                    if block.issubset(component_atom_indices):
                        blocks_in_component.append(block)
                blocks.append(blocks_in_component)
            
            # Each quartet yields blocks of different sizes, so this is a ragged
            # structure by nature. NumPy refuses to build an array from it, and the
            # consumers index it by quartet and by block, which a list already does.
            all_blocks.append(blocks)

    
    if len(dihedral_angles)==1:
        all_quartets = all_quartets[0]
        if with_blocks:
            all_blocks = all_blocks[0]
    elif len(dihedral_angles)==0:
        all_quartets = None
        all_blocks = None

    all_quartets = [ii.tolist() for ii in all_quartets]
    if with_blocks:
        return all_quartets, all_blocks
    else:
        return all_quartets
