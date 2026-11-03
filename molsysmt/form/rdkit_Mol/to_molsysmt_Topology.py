"""Converting an RDKit molecule into normalized native chemical-state storage."""

import pandas as pd

from molsysmt._private.argdigest import arg_digest

_RDKIT_BOND_STEREOCHEMISTRY = {
    "STEREOE": "E",
    "STEREOZ": "Z",
    "STEREOCIS": "cis",
    "STEREOTRANS": "trans",
}


def _rdkit_atom_stereochemistry(atom):
    if atom.HasProp("_CIPCode"):
        value = atom.GetProp("_CIPCode")
        if value in {"R", "S", "r", "s"}:
            return value
    return "unspecified"


def _rdkit_bond_metadata(bond):
    """Return independent canonical values supplied by one RDKit bond."""

    bond_type_name = str(bond.GetBondType()).upper()
    numeric_order = float(bond.GetBondTypeAsDouble())
    is_aromatic = bool(bond.GetIsAromatic())
    is_dative = bond_type_name.startswith("DATIVE")

    if is_aromatic or not numeric_order.is_integer():
        bond_order = pd.NA
        fractional_order = numeric_order
    else:
        bond_order = int(numeric_order)
        fractional_order = pd.NA

    stereochemistry = _RDKIT_BOND_STEREOCHEMISTRY.get(str(bond.GetStereo()))
    stereo_atoms = list(bond.GetStereoAtoms())
    if stereochemistry is None or len(stereo_atoms) != 2:
        stereochemistry = pd.NA
        stereo_atoms = [pd.NA, pd.NA]

    donor = bond.GetBeginAtomIdx() if is_dative else pd.NA
    acceptor = bond.GetEndAtomIdx() if is_dative else pd.NA
    return {
        "bond_id": str(bond.GetIdx()),
        "bond_order": bond_order,
        "fractional_bond_order": fractional_order,
        "bond_type": "dative" if is_dative else "covalent",
        "is_aromatic": is_aromatic,
        "is_conjugated": bool(bond.GetIsConjugated()),
        "stereochemistry": stereochemistry,
        "stereo_atom1_index": stereo_atoms[0],
        "stereo_atom2_index": stereo_atoms[1],
        "donor_atom_index": donor,
        "acceptor_atom_index": acceptor,
        "evidence": "explicit",
    }


@arg_digest(form="rdkit.Mol")
def to_molsysmt_Topology(item, atom_indices="all", skip_digestion=False):
    """
    Converting from rdkit.Mol to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    from ._read_native import read_native

    return read_native(item, atom_indices=atom_indices, skip_digestion=True).topology
