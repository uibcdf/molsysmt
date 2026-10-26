"""Project and validate explicit PDBQT output fields without molecular edits."""

import numpy as np
import pandas as pd

from molsysmt import pyunitwizard as puw
from molsysmt._private.pdbqt import fail
from molsysmt._private.variables import is_all

FIELDS = frozenset(
    {
        "atom_serials",
        "atom_names",
        "group_names",
        "group_ids",
        "chain_ids",
        "occupancy",
        "b_factor",
    }
)


def field(value, width, name, *, integer=False):
    if pd.isna(value):
        return " " * width
    text = str(value)
    if integer:
        try:
            number = int(text)
        except ValueError:
            fail(f"PDBQT {name} must be an integer string.")
        if str(number) != text:
            fail(f"PDBQT {name} must have a canonical integer representation.")
    if len(text) > width or any(ord(char) < 33 or ord(char) > 126 for char in text):
        fail(f"PDBQT {name} cannot fit its {width}-column field.")
    return text.rjust(width)


def keys(presentation):
    if presentation is None:
        return {}
    if not isinstance(presentation, dict) or any(
        not isinstance(k, str) for k in presentation
    ):
        fail("output_presentation must be a dictionary with string field names.")
    unknown = set(presentation) - FIELDS
    if unknown:
        fail(f"Unsupported PDBQT presentation fields: {sorted(unknown)}.")
    return presentation


def select(presentation, n_source_atoms, atom_indices):
    """Project source-axis vectors through native extraction's sorted atom selection."""
    presentation = keys(presentation)
    retained = (
        None
        if atom_indices is None or is_all(atom_indices)
        else np.unique(atom_indices)
    )
    selected = {}
    for name, value in presentation.items():
        quantity = not isinstance(value, str) and puw.is_quantity(value)
        values = puw.get_value(value) if quantity else value
        try:
            array = np.asarray(values, dtype=None if quantity else object)
        except (ValueError, TypeError):
            fail(f"PDBQT {name} must be a scalar or a source-atom vector.")
        if array.ndim == 0:
            selected[name] = value
        elif array.ndim == 1 and len(array) == n_source_atoms:
            chosen = array.copy() if retained is None else array[retained]
            selected[name] = (
                puw.quantity(chosen, puw.get_unit(value)) if quantity else chosen
            )
        else:
            fail(f"PDBQT {name} vectors must match the original input atom axis.")
    return selected


def _array(value, n_atoms, name):
    array = np.asarray(value, dtype=object)
    if array.ndim == 0:
        scalar = array.item()
        array = np.empty(n_atoms, dtype=object)
        array.fill(scalar)
    if array.shape != (n_atoms,):
        fail(f"PDBQT {name} must align with the selected atom axis.")
    return array


def prepare(presentation, n_atoms, written_order):
    prepared = {}
    for name, value in keys(presentation).items():
        if (
            name not in {"occupancy", "b_factor"}
            and not isinstance(value, str)
            and puw.is_quantity(value)
        ):
            fail(f"PDBQT {name} labels cannot carry physical units.")
        if name == "atom_serials":
            if isinstance(value, str):
                if value == "preserve":
                    continue
                if value != "consecutive" or n_atoms > 99999:
                    fail(
                        "atom_serials must be 'preserve', 'consecutive' or explicit serials in [1, 99999]."
                    )
                serials = np.empty(n_atoms, dtype=np.int64)
                serials[written_order] = np.arange(1, n_atoms + 1)
            else:
                values = _array(value, n_atoms, name)
                if any(
                    isinstance(v, (bool, np.bool_))
                    or not isinstance(v, (str, int, np.integer))
                    for v in values
                ):
                    fail("Explicit PDBQT serials must be canonical integer labels.")
                try:
                    serials = np.asarray([int(v) for v in values], dtype=np.int64)
                except (ValueError, OverflowError):
                    fail("Explicit PDBQT serials must be canonical integer labels.")
                if any(str(s) != str(v) for s, v in zip(serials, values)):
                    fail("Explicit PDBQT serials must be canonical integer labels.")
            if (
                np.any(serials < 1)
                or np.any(serials > 99999)
                or len(np.unique(serials)) != n_atoms
            ):
                fail("PDBQT output serials must be unique and in [1, 99999].")
            prepared[name] = serials
        elif name in {"occupancy", "b_factor"}:
            if value is None:
                prepared[name] = np.full(n_atoms, np.nan)
                continue
            if name == "b_factor":
                if not puw.is_quantity(value) or not puw.are_compatible(
                    value, "angstrom**2"
                ):
                    fail(
                        "PDBQT b_factor presentation requires a squared-length quantity."
                    )
                value = puw.get_value(value, to_unit="angstrom**2")
            elif puw.is_quantity(value):
                if not puw.are_compatible(value, "dimensionless"):
                    fail("PDBQT occupancy must be dimensionless.")
                value = puw.get_value(value, to_unit="dimensionless")
            values = _array(value, n_atoms, name)
            if any(
                isinstance(v, (bool, np.bool_, complex, np.complexfloating))
                for v in values
            ):
                fail(f"PDBQT {name} presentation must contain finite real numbers.")
            try:
                values = np.asarray(values, dtype=float)
            except (ValueError, TypeError):
                fail(f"PDBQT {name} presentation must contain finite real numbers.")
            if not np.isfinite(values).all():
                fail(f"PDBQT {name} presentation must contain finite real numbers.")
            prepared[name] = values
        else:
            width = {"atom_names": 4, "group_names": 3, "group_ids": 4, "chain_ids": 1}[
                name
            ]
            values = _array(value, n_atoms, name)
            strings = [
                field(v, width, name, integer=name == "group_ids") for v in values
            ]
            if name == "atom_names" and any(not s.strip() for s in strings):
                fail("PDBQT writing requires atom names.")
            prepared[name] = strings
    return prepared


def caller_remarks(remarks):
    if remarks is None:
        return ()
    if not isinstance(remarks, (list, tuple, np.ndarray)):
        fail("remarks must be a sequence of complete REMARK lines.")
    lines, total = [], 0
    for line in remarks:
        if (
            not isinstance(line, str)
            or not line.startswith("REMARK ")
            or not line[7:].strip()
            or len(line) > 4096
            or any(ord(c) < 32 or ord(c) > 126 for c in line)
        ):
            fail(
                "Caller remarks must be printable ASCII REMARK lines of at most 4096 characters, without newlines."
            )
        if line[7:].lstrip().upper().startswith("MOLSYSMT_"):
            fail(
                "Caller remarks cannot use the reserved MOLSYSMT_ provenance namespace."
            )
        total += len(line) + 1
        if total > 65536:
            fail("Caller remarks exceed the 64 KiB output budget.")
        lines.append(line)
    return tuple(lines)
