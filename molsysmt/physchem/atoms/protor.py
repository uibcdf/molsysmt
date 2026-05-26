import numpy as np
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw

# Fallback radii in Angstroms
_PROTOR_FALLBACK_RADII = {
    'C': 1.88,
    'N': 1.64,
    'O': 1.42,
    'S': 1.77,
}

# Radii mapped by type in Angstroms
_PROTOR_RADII_BY_TYPE = {
    'C3H0': 1.61,
    'C3H1': 1.76,
    'C4H1': 1.88,
    'C4H2': 1.88,
    'C4H3': 1.88,
    'N3H0': 1.64,
    'N3H1': 1.64,
    'N3H2': 1.64,
    'N4H3': 1.64,
    'O1H0': 1.42,
    'O2H1': 1.46,
    'S2H0': 1.77,
    'S2H1': 1.77,
}

# Backbone atom types map
_PROTOR_PROTEIN_BACKBONE_TYPES = {
    'N': 'N3H1',
    'CA': 'C4H1',
    'C': 'C3H0',
    'O': 'O1H0',
    'OXT': 'O2H1',
}

# Residue name aliases (for variant protonation states)
_PROTOR_RESIDUE_NAME_ALIASES = {
    'HSD': 'HID',
    'HSE': 'HIE',
    'HSP': 'HIP',
}

# Standard and variant residue specific heavy atom ProtOr types
_PROTOR_PROTEIN_HEAVY_ATOM_TYPES = {
    'ALA': {'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0', 'CB': 'C4H3'},
    'ARG': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C4H2', 'CD': 'C4H2', 'NE': 'N3H1', 'CZ': 'C3H0', 'NH1': 'N3H2', 'NH2': 'N3H2',
    },
    'ASN': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'OD1': 'O1H0', 'ND2': 'N3H2',
    },
    'ASP': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'OD1': 'O1H0', 'OD2': 'O1H0',
    },
    'ASH': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'OD1': 'O1H0', 'OD2': 'O2H1',
    },
    'CYS': {'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0', 'CB': 'C4H2', 'SG': 'S2H1'},
    'CYX': {'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0', 'CB': 'C4H2', 'SG': 'S2H0'},
    'GLN': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C4H2', 'CD': 'C3H0', 'OE1': 'O1H0', 'NE2': 'N3H2',
    },
    'GLU': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C4H2', 'CD': 'C3H0', 'OE1': 'O1H0', 'OE2': 'O1H0',
    },
    'GLH': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C4H2', 'CD': 'C3H0', 'OE1': 'O1H0', 'OE2': 'O2H1',
    },
    'GLY': {'N': 'N3H1', 'CA': 'C4H2', 'C': 'C3H0', 'O': 'O1H0'},
    'HIS': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'ND1': 'N3H0', 'CD2': 'C3H1', 'CE1': 'C3H1', 'NE2': 'N3H0',
    },
    'HID': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'ND1': 'N3H1', 'CD2': 'C3H1', 'CE1': 'C3H1', 'NE2': 'N3H0',
    },
    'HIE': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'ND1': 'N3H0', 'CD2': 'C3H1', 'CE1': 'C3H1', 'NE2': 'N3H1',
    },
    'HIP': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'ND1': 'N3H1', 'CD2': 'C3H1', 'CE1': 'C3H1', 'NE2': 'N3H1',
    },
    'ILE': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H1', 'CG1': 'C4H2', 'CG2': 'C4H3', 'CD1': 'C4H3',
    },
    'LEU': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C4H1', 'CD1': 'C4H3', 'CD2': 'C4H3',
    },
    'LYS': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C4H2', 'CD': 'C4H2', 'CE': 'C4H2', 'NZ': 'N4H3',
    },
    'LYN': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C4H2', 'CD': 'C4H2', 'CE': 'C4H2', 'NZ': 'N3H2',
    },
    'MET': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C4H2', 'SD': 'S2H0', 'CE': 'C4H3',
    },
    'PHE': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'CD1': 'C3H1', 'CD2': 'C3H1', 'CE1': 'C3H1', 'CE2': 'C3H1', 'CZ': 'C3H1',
    },
    'PRO': {'N': 'N3H0', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0', 'CB': 'C4H2', 'CG': 'C4H2', 'CD': 'C4H2'},
    'SER': {'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0', 'CB': 'C4H2', 'OG': 'O2H1'},
    'THR': {'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0', 'CB': 'C4H1', 'OG1': 'O2H1', 'CG2': 'C4H3'},
    'TRP': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'CD1': 'C3H1', 'CD2': 'C3H0', 'NE1': 'N3H1', 'CE2': 'C3H0',
        'CE3': 'C3H1', 'CZ2': 'C3H1', 'CZ3': 'C3H1', 'CH2': 'C3H1',
    },
    'TYR': {
        'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0',
        'CB': 'C4H2', 'CG': 'C3H0', 'CD1': 'C3H1', 'CD2': 'C3H1', 'CE1': 'C3H1', 'CE2': 'C3H1', 'CZ': 'C3H0', 'OH': 'O2H1',
    },
    'VAL': {'N': 'N3H1', 'CA': 'C4H1', 'C': 'C3H0', 'O': 'O1H0', 'CB': 'C4H1', 'CG1': 'C4H3', 'CG2': 'C4H3'},
}


def _infer_protor_type_for_atom(residue_name, atom_name, atom_type, n_bonds):
    """
    Inferring the ProtOr-like atom type for a protein heavy atom.

    Parameters
    ----------
    residue_name : str
        The group/residue name.
    atom_name : str
        The atom name.
    atom_type : str
        The atom type/element name.
    n_bonds : int
        The number of heavy-atom bonds of the atom.

    Returns
    -------
    str or None
        The assigned ProtOr type, or None if fallback.
    """
    residue_name = str(residue_name).strip().upper()
    atom_name = str(atom_name).strip().upper()
    atom_type = str(atom_type).strip().upper()
    n_bonds = int(n_bonds)

    normalized_residue_name = _PROTOR_RESIDUE_NAME_ALIASES.get(residue_name, residue_name)
    residue_map = _PROTOR_PROTEIN_HEAVY_ATOM_TYPES.get(normalized_residue_name)

    if residue_map is not None and atom_name in residue_map:
        return residue_map[atom_name]

    if atom_name in _PROTOR_PROTEIN_BACKBONE_TYPES:
        if atom_name == 'N':
            return 'N3H0' if normalized_residue_name == 'PRO' else 'N3H1'
        if atom_name == 'CA':
            return 'C4H2' if normalized_residue_name == 'GLY' else 'C4H1'
        return _PROTOR_PROTEIN_BACKBONE_TYPES[atom_name]

    if atom_type == 'S':
        return 'S2H1' if n_bonds <= 1 else 'S2H0'

    return None


@arg_digest()
def get_protor_atom_type(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False):
    """
    Determining the ProtOr atom type for selected atoms.

    Assigns implicit-hydrogen-aware ProtOr atom types to protein heavy atoms
    based on residue identities, atom labels, and connectivity.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of atoms to include.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    (numpy.ndarray, numpy.ndarray)
        The first array contains the assigned ProtOr types (str or None).
        The second array contains the rule provenance/matching category (str).
        Shape of both: ``(n_atoms,)``.

    Notes
    -----
    Types are assigned to standard amino acids and their common variants, and 
    backbone defaults are applied. Elements that do not match are labeled as 
    ``'element_fallback'`` or ``'ignored'`` (e.g. for hydrogen).

    .. versionadded:: 1.0.0
    """
    from molsysmt.basic import get

    # Extract required attributes
    group_names, atom_names, atom_types, bonded_atoms = get(
        molecular_system,
        element='atom',
        selection=selection,
        group_name=True,
        atom_name=True,
        atom_type=True,
        bonded_atoms=True
    )

    # Convert results to arrays to facilitate vectorized or indexed access
    group_names = np.asarray(group_names, dtype=object)
    atom_names = np.asarray(atom_names, dtype=object)
    atom_types = np.asarray(atom_types, dtype=object)

    # Get atom types for ALL atoms in the system to check neighbor elements
    all_atom_types = np.asarray(
        get(molecular_system, element='atom', selection='all', atom_type=True),
        dtype=object
    )

    n_atoms = len(group_names)
    protor_types = np.empty(n_atoms, dtype=object)
    provenance = np.empty(n_atoms, dtype=object)

    for ii in range(n_atoms):
        element = str(atom_types[ii]).strip().upper()
        if element == 'H':
            protor_types[ii] = None
            provenance[ii] = 'ignored'
            continue

        # Count only bonds with heavy atoms (not 'H')
        neighbors = bonded_atoms[ii]
        n_heavy_bonds = sum(1 for neighbor_idx in neighbors if all_atom_types[neighbor_idx] != 'H')

        res_name = str(group_names[ii]).strip().upper()
        at_name = str(atom_names[ii]).strip().upper()

        ptype = _infer_protor_type_for_atom(res_name, at_name, element, n_heavy_bonds)

        if ptype is not None:
            protor_types[ii] = ptype
            if at_name in _PROTOR_PROTEIN_BACKBONE_TYPES:
                provenance[ii] = 'protein_backbone'
            else:
                provenance[ii] = 'protein_heavy'
        else:
            protor_types[ii] = None
            provenance[ii] = 'element_fallback'

    return protor_types, provenance


@arg_digest()
def get_protor_vdw_radius(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False):
    """
    Calculating the ProtOr atomic van der Waals radius for selected atoms.

    Computes the implicit-hydrogen-aware ProtOr radii in nanometers, applying
    specific protein heavy-atom definitions or standard element-level fallbacks.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of atoms to include.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    skip_digestion : bool, default False
        If ``True``, bypass argument validation (for internal use only).

    Returns
    -------
    quantity
        Atomic van der Waals radii as a PyUnitWizard quantity in nm.
        Shape: ``(n_atoms,)``.

    Notes
    -----
    Standard ProtOr radii are defined in Ångstroms and converted to nanometers (nm)
    for integration with MolSysMT's default unit framework. Non-protein atoms or
    unrecognized residues utilize standard element fallbacks or global default values.

    .. versionadded:: 1.0.0
    """
    from molsysmt.physchem.atoms.radius import vdw as standard_vdw

    protor_types, provenance = get_protor_atom_type(
        molecular_system,
        selection=selection,
        syntax=syntax,
        skip_digestion=True
    )

    from molsysmt.basic import get
    atom_types = get(molecular_system, element='atom', selection=selection, atom_type=True)
    atom_types = np.asarray(atom_types, dtype=object)

    radii = np.empty(len(protor_types), dtype=float)

    for ii, ptype in enumerate(protor_types):
        if ptype is not None:
            # Standard ProtOr radius is in Angstroms, convert to nanometers (divide by 10)
            radii[ii] = float(_PROTOR_RADII_BY_TYPE[ptype]) / 10.0
        else:
            element = str(atom_types[ii]).strip().capitalize()
            # If standard element fallback exists in ProtOr
            if element.upper() in _PROTOR_FALLBACK_RADII:
                radii[ii] = _PROTOR_FALLBACK_RADII[element.upper()] / 10.0
            else:
                # Retrieve default vdw radius in nm
                val = standard_vdw.get(element)
                if val is None:
                    # Global default heavy-atom fallback is 0.18 nm (1.8 Angstroms)
                    radii[ii] = 0.12 if element == 'H' else 0.18
                else:
                    radii[ii] = float(val)

    return puw.quantity(radii, 'nm')
