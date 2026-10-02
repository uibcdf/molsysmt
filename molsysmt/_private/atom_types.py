"""Sharing explicit chemical atom types between queries and native readers."""

import numpy as np

# Genuine chemical elements only. Dummy particles and force-field labels have
# distinct semantics, even when other MolSysMT tables assign them a mass.
CHEMICAL_ATOM_TYPES = frozenset(
    "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni "
    "Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I "
    "Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir "
    "Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md "
    "No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split()
)


def normalize_atom_type(atom_type, isotope=None):
    """Return one canonical element and nullable mass number without guessing."""

    if not isinstance(atom_type, str):
        raise ValueError("An atom_type must be a chemical element symbol string.")
    if isotope is not None:
        if (
            not isinstance(isotope, (int, np.integer))
            or isinstance(isotope, (bool, np.bool_))
            or not 1 <= int(isotope) <= 65535
        ):
            raise ValueError(
                "An isotope must be a positive integer mass number up to 65535."
            )
        isotope = int(isotope)
    if atom_type in {"D", "T"}:
        implied = 2 if atom_type == "D" else 3
        if isotope is not None and isotope != implied:
            raise ValueError(
                f"Atom type {atom_type!r} conflicts with isotope {isotope}."
            )
        return "H", implied
    if atom_type not in CHEMICAL_ATOM_TYPES:
        raise ValueError(f"Unsupported chemical atom_type {atom_type!r}.")
    return atom_type, isotope
