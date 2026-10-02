"""Reading explicit CTAB records without chemical perception or optional toolkits.

This module implements the bounded native SDF contract. It deliberately rejects
query chemistry and stereo encodings until a faithful native interpretation is
available. The connection-table reader is independent of native-object assembly.
Reference: BIOVIA CTFile Formats 2020; RDKit's FileParsers were inspected, not
copied (uibcdf/molsysmt#215).
"""

import re
import shlex
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from molsysmt._private.smonitor import FormatError

_ELEMENTS = frozenset(
    "H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni "
    "Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I "
    "Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir "
    "Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md "
    "No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og".split()
)
# CTAB's mass-difference field uses the rounded reference isotope, not an
# arbitrary application mass. Other elements require absolute M ISO / MASS.
_REFERENCE_ISOTOPES = {
    "H": 1,
    "B": 11,
    "C": 12,
    "N": 14,
    "O": 16,
    "F": 19,
    "Si": 28,
    "P": 31,
    "S": 32,
    "Cl": 35,
    "Br": 79,
    "I": 127,
}


def _fail(reason):
    raise FormatError(reason=reason, caller="molsysmt._private.ctfile")


def _integer(token, context, *, blank=False):
    value = token.strip()
    if not value and blank:
        return 0
    if re.fullmatch(r"[+-]?[0-9]+", value) is None:
        _fail(f"Invalid integer {token!r} in {context}.")
    return int(value)


@dataclass
class AtomRecord:
    serial: int
    element: str
    coordinates: tuple
    formal_charge: int = 0
    isotope: int | None = None
    n_unpaired_electrons: int = 0


@dataclass
class BondRecord:
    serial: int
    atom1: int
    atom2: int
    order: int


@dataclass
class CTRecord:
    title: str
    version: str
    atoms: list = field(default_factory=list)
    bonds: list = field(default_factory=list)
    properties: list = field(default_factory=list)


def _atom(serial, element, coordinates, *, isotope=None):
    if element in {"D", "T"}:
        isotope = {"D": 2, "T": 3}[element]
        element = "H"
    if element not in _ELEMENTS:
        _fail(f"Unsupported atom symbol {element!r}; query atoms are not elements.")
    values = [value.strip() or "0" for value in coordinates]
    if any(
        re.fullmatch(
            r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", value
        )
        is None
        for value in values
    ):
        _fail(f"Invalid coordinates for atom {serial}.")
    coordinates = tuple(float(value) for value in values)
    if not np.isfinite(coordinates).all():
        _fail(f"Non-finite coordinates for atom {serial}.")
    return AtomRecord(serial, element, coordinates, isotope=isotope)


def _radical(value):
    if value not in {0, 2, 3}:
        _fail(f"Unsupported radical code {value}; singlet spin cannot be retained.")
    return {0: 0, 2: 1, 3: 2}[value]


def _validate(record):
    atom_serials = {atom.serial for atom in record.atoms}
    if len(atom_serials) != len(record.atoms) or any(i <= 0 for i in atom_serials):
        _fail("Atom serials must be unique positive integers.")
    bond_serials, pairs = set(), set()
    for atom in record.atoms:
        if (
            atom.element not in _ELEMENTS
            or len(atom.coordinates) != 3
            or not np.isfinite(atom.coordinates).all()
        ):
            _fail(f"Invalid element or coordinates for atom {atom.serial}.")
        if atom.n_unpaired_electrons not in {0, 1, 2}:
            _fail(f"Unsupported radical count for atom {atom.serial}.")
        if not -15 <= atom.formal_charge <= 15:
            _fail(
                f"Formal charge outside CTAB's supported range on atom {atom.serial}."
            )
        if atom.isotope is not None and not 1 <= atom.isotope <= 65535:
            _fail(f"Invalid isotope on atom {atom.serial}.")
    for bond in record.bonds:
        if bond.serial <= 0 or bond.serial in bond_serials:
            _fail("Bond serials must be unique positive integers.")
        bond_serials.add(bond.serial)
        if bond.atom1 not in atom_serials or bond.atom2 not in atom_serials:
            _fail(f"Bond {bond.serial} references an unknown atom.")
        pair = tuple(sorted((bond.atom1, bond.atom2)))
        if bond.atom1 == bond.atom2 or pair in pairs:
            _fail(f"Self or duplicate bond {bond.serial}.")
        pairs.add(pair)
        if bond.order not in {1, 2, 3, 4}:
            _fail(f"Unsupported bond type {bond.order}; no query order is inferred.")


def _v2000(lines):
    counts = lines[3]
    if len(counts) < 39 or counts[33:39].strip() != "V2000":
        _fail("Missing or malformed V2000 counts line.")
    n_atoms = _integer(counts[:3], "atom count", blank=True)
    n_bonds = _integer(counts[3:6], "bond count", blank=True)
    if n_atoms < 0 or n_bonds < 0 or len(lines) < 5 + n_atoms + n_bonds:
        _fail("Negative counts or truncated V2000 connection table.")
    # Atom lists, chiral flag, Stext, and obsolete entries need their own model.
    for start in (6, 9, 12, 15, 18, 21, 24, 27):
        if _integer(counts[start : start + 3], "counts flags", blank=True):
            _fail(
                "Unsupported nonzero V2000 counts flag (including stereo/query data)."
            )
    record = CTRecord(lines[0], "V2000")
    mass_differences = []
    for i, line in enumerate(lines[4 : 4 + n_atoms], 1):
        if len(line) < 39:
            _fail(f"Truncated atom line for atom {i}.")
        atom = _atom(i, line[31:34].strip(), (line[:10], line[10:20], line[20:30]))
        difference = _integer(line[34:36], "mass difference", blank=True)
        if not -3 <= difference <= 4:
            _fail("V2000 mass differences must be between -3 and +4; use M ISO.")
        if difference:
            mass_differences.append((atom, difference))
        charge = _integer(line[36:39], "atom charge", blank=True)
        if charge not in range(8):
            _fail(f"Unsupported atom charge code {charge}.")
        atom.formal_charge = 4 - charge if charge and charge != 4 else 0
        atom.n_unpaired_electrons = int(charge == 4)
        for start in range(39, max(len(line), 69), 3):
            if _integer(line[start : start + 3], "atom flags", blank=True):
                _fail(
                    f"Unsupported atom flag on atom {i} (stereo, query, valence or map)."
                )
        record.atoms.append(atom)
    for i, line in enumerate(lines[4 + n_atoms : 4 + n_atoms + n_bonds], 1):
        if len(line) < 9:
            _fail(f"Truncated bond line for bond {i}.")
        values = [
            _integer(line[start : start + 3], "bond", blank=True)
            for start in range(0, max(len(line), 21), 3)
        ]
        if any(values[3:]):
            _fail(
                f"Unsupported bond flag on bond {i} (stereo, query or reaction data)."
            )
        record.bonds.append(BondRecord(i, *values[:3]))
    cursor = 4 + n_atoms + n_bonds
    reset_charge_radical = False
    reset_isotope = False
    while cursor < len(lines) and lines[cursor] != "M  END":
        line = lines[cursor]
        tag = line[:6]
        if tag not in {"M  CHG", "M  ISO", "M  RAD"}:
            _fail(f"Unsupported CTAB property line {line!r}.")
        count = _integer(line[6:9], "property count")
        if not 1 <= count <= 8 or len(line.rstrip()) > 9 + 8 * count:
            _fail("Invalid CTAB property count or trailing data.")
        if tag in {"M  CHG", "M  RAD"} and not reset_charge_radical:
            for atom in record.atoms:
                atom.formal_charge = 0
                atom.n_unpaired_electrons = 0
            reset_charge_radical = True
        if tag == "M  ISO" and not reset_isotope:
            for atom in record.atoms:
                atom.isotope = None
            reset_isotope = True
        for offset in range(count):
            start = 9 + 8 * offset
            serial = _integer(line[start : start + 4], "property atom")
            value = _integer(line[start + 4 : start + 8], "property value")
            if not 1 <= serial <= n_atoms:
                _fail("CTAB property references an unknown atom.")
            atom = record.atoms[serial - 1]
            if tag == "M  CHG":
                atom.formal_charge = value
            elif tag == "M  ISO":
                atom.isotope = value or None
            else:
                atom.n_unpaired_electrons = _radical(value)
        cursor += 1
    if cursor == len(lines):
        _fail("Missing M  END connection-table terminator.")
    if not reset_isotope:
        for atom, difference in mass_differences:
            if atom.isotope is not None or atom.element not in _REFERENCE_ISOTOPES:
                _fail(
                    "Unsupported mass-difference element; use an absolute M ISO isotope."
                )
            atom.isotope = _REFERENCE_ISOTOPES[atom.element] + difference
    return record, cursor + 1


def _v3000(lines):
    logical = []
    cursor = 4
    while cursor < len(lines) and lines[cursor] != "M  END":
        payload = ""
        while True:
            if cursor >= len(lines) or not lines[cursor].startswith("M  V30 "):
                _fail("Malformed or truncated V3000 continuation.")
            segment = lines[cursor][7:]
            cursor += 1
            continued = segment.endswith("-")
            payload += segment[:-1] if continued else segment
            if not continued:
                break
        try:
            logical.append(shlex.split(payload, posix=True))
        except ValueError:
            _fail("Malformed quoted V3000 token.")
    if cursor == len(lines):
        _fail("Missing M  END connection-table terminator.")
    if len(logical) < 4 or logical[0] != ["BEGIN", "CTAB"]:
        _fail("Missing V3000 BEGIN CTAB.")
    counts = logical[1]
    if len(counts) != 6 or counts[0] != "COUNTS":
        _fail("Malformed V3000 COUNTS.")
    n_atoms, n_bonds, *flags = [_integer(i, "V3000 counts") for i in counts[1:]]
    if n_atoms < 0 or n_bonds < 0 or any(flags):
        _fail("Unsupported V3000 counts (query, groups or stereo).")
    record = CTRecord(lines[0], "V3000")
    position = 2
    for name, count in (("ATOM", n_atoms), ("BOND", n_bonds)):
        # Empty sections may be omitted by conforming writers.
        if position >= len(logical):
            _fail("Truncated V3000 sections.")
        if count == 0 and logical[position] != ["BEGIN", name]:
            continue
        if logical[position] != ["BEGIN", name]:
            _fail(f"Missing V3000 BEGIN {name}.")
        position += 1
        for _ in range(count):
            if position >= len(logical):
                _fail(f"Truncated V3000 {name} block.")
            tokens = logical[position]
            position += 1
            if name == "ATOM":
                if len(tokens) < 6:
                    _fail("Truncated V3000 atom.")
                atom = _atom(_integer(tokens[0], "atom serial"), tokens[1], tokens[2:5])
                if _integer(tokens[5], "atom map"):
                    _fail("V3000 reaction atom maps cannot be retained yet.")
                seen = set()
                for token in tokens[6:]:
                    key, separator, value = token.partition("=")
                    if (
                        not separator
                        or key not in {"CHG", "MASS", "RAD"}
                        or key in seen
                    ):
                        _fail(f"Unsupported or repeated V3000 atom property {token!r}.")
                    seen.add(key)
                    value = _integer(value, key)
                    if key == "CHG":
                        atom.formal_charge = value
                    elif key == "MASS":
                        atom.isotope = value or None
                    else:
                        atom.n_unpaired_electrons = _radical(value)
                record.atoms.append(atom)
            else:
                if len(tokens) != 4:
                    _fail(
                        "Unsupported V3000 bond properties (including stereo/query data)."
                    )
                serial, order, atom1, atom2 = [
                    _integer(i, "V3000 bond") for i in tokens
                ]
                record.bonds.append(BondRecord(serial, atom1, atom2, order))
        if position >= len(logical) or logical[position] != ["END", name]:
            _fail(f"Missing V3000 END {name} or mismatched count.")
        position += 1
    if logical[position:] != [["END", "CTAB"]]:
        _fail("Unsupported V3000 sections or mismatched CTAB terminator.")
    return record, cursor + 1


def read_sdf(filename):
    """Read exactly one record, retaining SD properties separately from chemistry."""
    # Read one record at a time; a multi-record database is never materialized.
    lines = []
    terminated = False
    with Path(filename).open(encoding="utf-8-sig", newline=None) as stream:
        for line in stream:
            line = line.rstrip("\n")
            if line == "$$$$":
                terminated = True
                break
            lines.append(line)
        if terminated and any(line.strip() for line in stream):
            _fail(
                "Multiple SDF records require a record-selection contract; none is discarded."
            )
    if not terminated:
        _fail("Missing $$$$ SDF record terminator.")
    if len(lines) < 5:
        _fail("Truncated SDF header or connection table.")
    if lines[3].rstrip().endswith("V2000"):
        record, cursor = _v2000(lines)
    elif lines[3].rstrip().endswith("V3000"):
        record, cursor = _v3000(lines)
    else:
        _fail("Only explicitly versioned V2000 and V3000 CTAB records are supported.")
    _validate(record)
    while cursor < len(lines):
        if not lines[cursor].strip():
            cursor += 1
            continue
        match = re.fullmatch(r">\s*(?:[^<]*)<([^<>]+)>.*", lines[cursor])
        if match is None:
            _fail(f"Malformed SD property header {lines[cursor]!r}.")
        cursor += 1
        value = []
        while cursor < len(lines) and lines[cursor].strip():
            value.append(lines[cursor])
            cursor += 1
        record.properties.append((match[1], "\n".join(value)))
    return record


def write_sdf(record):
    """Render a validated explicit record before opening any destination file."""
    _validate(record)
    if "\n" in record.title or "\r" in record.title:
        _fail("An SDF molecule title must occupy one line.")
    if record.properties:
        _fail("Native SD-property serialization is outside the supported contract.")
    lines = [record.title, "  MolSysMT          3D", ""]
    if record.version == "V2000":
        if len(record.atoms) > 999 or len(record.bonds) > 999:
            _fail("V2000 counts exceed 999; choose ctfile_version='V3000'.")
        lines.append(
            f"{len(record.atoms):3d}{len(record.bonds):3d}  0  0  0  0  0  0  0  0999 V2000"
        )
        mapping = {atom.serial: i for i, atom in enumerate(record.atoms, 1)}
        for atom in record.atoms:
            coordinates = [f"{value:10.4f}" for value in atom.coordinates]
            if any(len(value) != 10 for value in coordinates):
                _fail("Coordinate exceeds V2000 field width; choose V3000.")
            lines.append(
                "".join(coordinates) + f" {atom.element:<3s}" + " 0" + "  0" * 11
            )
        for bond in record.bonds:
            lines.append(
                f"{mapping[bond.atom1]:3d}{mapping[bond.atom2]:3d}{bond.order:3d}  0  0  0  0"
            )
        for tag, getter in (
            ("CHG", lambda atom: atom.formal_charge),
            ("ISO", lambda atom: atom.isotope or 0),
            ("RAD", lambda atom: {0: 0, 1: 2, 2: 3}[atom.n_unpaired_electrons]),
        ):
            entries = [
                (mapping[atom.serial], getter(atom))
                for atom in record.atoms
                if getter(atom)
            ]
            for start in range(0, len(entries), 8):
                chunk = entries[start : start + 8]
                lines.append(
                    f"M  {tag}{len(chunk):3d}"
                    + "".join(f"{i:4d}{value:4d}" for i, value in chunk)
                )
    elif record.version == "V3000":
        lines.extend(
            [
                "  0  0  0     0  0            999 V3000",
                "M  V30 BEGIN CTAB",
                f"M  V30 COUNTS {len(record.atoms)} {len(record.bonds)} 0 0 0",
                "M  V30 BEGIN ATOM",
            ]
        )
        for atom in record.atoms:
            xyz = " ".join(f"{value:.12g}" for value in atom.coordinates)
            attributes = []
            if atom.formal_charge:
                attributes.append(f"CHG={atom.formal_charge}")
            if atom.isotope:
                attributes.append(f"MASS={atom.isotope}")
            if atom.n_unpaired_electrons:
                attributes.append(f"RAD={ {1: 2, 2: 3}[atom.n_unpaired_electrons] }")
            lines.append(
                f"M  V30 {atom.serial} {atom.element} {xyz} 0"
                + (" " + " ".join(attributes) if attributes else "")
            )
        lines.extend(["M  V30 END ATOM", "M  V30 BEGIN BOND"])
        for bond in record.bonds:
            lines.append(f"M  V30 {bond.serial} {bond.order} {bond.atom1} {bond.atom2}")
        lines.extend(["M  V30 END BOND", "M  V30 END CTAB"])
    else:
        _fail("ctfile_version must be 'V2000' or 'V3000'.")
    wrapped = []
    for line in lines:
        while line.startswith("M  V30 ") and len(line) > 80:
            wrapped.append(line[:79] + "-")
            line = "M  V30 " + line[79:]
        wrapped.append(line)
    return "\n".join([*wrapped, "M  END", "$$$$", ""])
