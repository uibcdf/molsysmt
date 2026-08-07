from datetime import datetime

import numpy as np
import pandas as pd

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


def _raise_capacity_error(attribute, reason):
    from molsysmt._private.smonitor import NotCompatibleConversionError

    raise NotCompatibleConversionError(
        "molsysmt.MolSys",
        "string:pdb_text",
        {attribute},
        caller="molsysmt.form.molsysmt_MolSys.to_string_pdb_text",
        message=reason,
    )


def _model_ids(structure_ids, n_structures):
    if structure_ids is None:
        return [str(index) for index in range(1, n_structures + 1)]
    output = [str(value) for value in structure_ids]
    valid = (
        len(set(output)) == len(output)
        and all(value.isdigit() and 1 <= int(value) <= 9999 for value in output)
    )
    if not valid:
        return [str(index) for index in range(1, n_structures + 1)]
    return output


def _charge_field(value):
    if value is None or pd.isna(value) or int(value) == 0:
        return "  "
    value = int(value)
    if abs(value) > 9:
        _raise_capacity_error(
            "formal_charge",
            "PDB formal-charge magnitudes must fit one decimal digit.",
        )
    return f"{abs(value)}{'+' if value > 0 else '-'}"


def _validate_coordinates(coordinates):
    if not np.isfinite(coordinates).all():
        _raise_capacity_error(
            "coordinates", "PDB coordinates must be finite."
        )
    if np.any(coordinates < -999.999) or np.any(coordinates > 9999.999):
        _raise_capacity_error(
            "coordinates",
            "PDB coordinates exceed the fixed-width 8.3 fields.",
        )


def _bioassembly_lines(item):
    bioassemblies = item.structures.bioassembly
    if not bioassemblies:
        return []
    lines = []
    chain_ids = item.topology.chains["chain_id"].astype(str).tolist()
    for assembly_id, assembly in bioassemblies.items():
        lines.append(f"REMARK 350 BIOMOLECULE: {assembly_id}\n")
        chain_indices = assembly["chain_indices"]
        if not chain_indices or not isinstance(
            chain_indices[0], (list, tuple, np.ndarray)
        ):
            chain_indices = [chain_indices] * len(assembly["rotations"])
        raw_translations = assembly["translations"]
        if isinstance(raw_translations, (list, tuple)):
            translations = [
                puw.get_value(translation, to_unit="angstrom")
                for translation in raw_translations
            ]
        else:
            translations = np.atleast_2d(
                puw.get_value(raw_translations, to_unit="angstrom")
            )
        for operation_index, (operation_chains, rotation, translation) in enumerate(
            zip(chain_indices, assembly["rotations"], translations), start=1
        ):
            names = ", ".join(chain_ids[int(index)] for index in operation_chains)
            lines.append(
                f"REMARK 350 APPLY THE FOLLOWING TO CHAINS: {names}\n"
            )
            for row in range(3):
                values = rotation[row]
                lines.append(
                    f"REMARK 350   BIOMT{row + 1} {operation_index:>3}"
                    f"{values[0]:>10.6f}{values[1]:>10.6f}{values[2]:>10.6f}"
                    f"{translation[row]:>15.5f}\n"
                )
    return lines


@arg_digest(form="molsysmt.MolSys")
def to_string_pdb_text(
    item,
    atom_indices="all",
    structure_indices="all",
    pdb_chain_id="chain_name",
    skip_digestion=False,
):
    """Converting a native molecular system to PDB text."""

    if not (is_all(atom_indices) and is_all(structure_indices)):
        item = item.extract(
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            copy_if_all=True,
            skip_digestion=True,
        )
        atom_indices = "all"
        structure_indices = "all"

    if is_all(atom_indices):
        source_atom_indices = np.arange(item.topology.n_atoms, dtype=int)
    else:
        source_atom_indices = np.sort(np.asarray(atom_indices, dtype=int))
    if is_all(structure_indices):
        selected_structures = np.arange(
            item.structures.n_structures, dtype=int
        )
    else:
        selected_structures = np.asarray(structure_indices, dtype=int)

    atoms = item.topology.atoms.iloc[source_atom_indices]
    groups = item.topology.groups
    chains = item.topology.chains
    chain_column = "chain_name" if pdb_chain_id == "chain_name" else "chain_id"

    structure_ids = (
        None
        if item.structures.structure_id is None
        else item.structures.structure_id[selected_structures]
    )
    model_ids = _model_ids(structure_ids, len(selected_structures))
    multiple_models = len(selected_structures) > 1

    variants_per_atom = []
    for source_atom_index in source_atom_indices:
        counts = []
        if item.structures.alternate_location is not None:
            for structure_index in selected_structures:
                alternates = item.structures.alternate_location[
                    int(structure_index)
                ].get(int(source_atom_index))
                counts.append(
                    1 if alternates is None else len(alternates["location_id"])
                )
        variants_per_atom.append(max(counts, default=1))
    n_records = sum(variants_per_atom)
    if n_records > 99999:
        _raise_capacity_error(
            "atom_id", "PDB atom serials exceed the five-column capacity."
        )
    first_serial = {}
    next_serial = 1
    for atom_index, count in zip(source_atom_indices, variants_per_atom):
        first_serial[int(atom_index)] = next_serial
        next_serial += count

    formal_charge = item.topology._get_chemical_state_atom_attribute(
        "formal_charge"
    )
    lines = []
    now = datetime.now()
    lines.append(
        f"HEADER    {'MOLECULAR SYSTEM':<40}"
        f"{now.strftime('%d-%b-%y').upper():>9}   {'':<4}\n"
    )
    lines.append(
        "REMARK   1 Created by MolSysMT version 1.0 on "
        f"{now.strftime('%d-%b-%Y').upper()} at {now.strftime('%H:%M:%S')}\n"
    )
    lines.extend(_bioassembly_lines(item))

    if item.structures.box is not None and len(selected_structures):
        from molsysmt.pbc import get_lengths_and_angles_from_box

        lengths, angles = get_lengths_and_angles_from_box(
            item.structures.box[int(selected_structures[0])]
        )
        a, b, c = puw.get_value(lengths[0], to_unit="angstrom")
        alpha, beta, gamma = puw.get_value(angles[0], to_unit="degrees")
        lines.append(
            f"CRYST1{a:>9.3f}{b:>9.3f}{c:>9.3f}"
            f"{alpha:>7.2f}{beta:>7.2f}{gamma:>7.2f}\n"
        )

    for local_structure_index, structure_index in enumerate(selected_structures):
        structure_index = int(structure_index)
        if multiple_models:
            lines.append(f"MODEL     {model_ids[local_structure_index]:>4}\n")
        previous_chain_index = None
        serial = 1
        for source_atom_index, atom in zip(
            source_atom_indices, atoms.itertuples()
        ):
            source_atom_index = int(source_atom_index)
            if (
                previous_chain_index is not None
                and atom.chain_index != previous_chain_index
            ):
                lines.append("TER\n")
            previous_chain_index = atom.chain_index

            alternate = None
            if item.structures.alternate_location is not None:
                alternate = item.structures.alternate_location[
                    structure_index
                ].get(source_atom_index)
            if alternate is None:
                coordinates = puw.get_value(
                    item.structures.coordinates[
                        structure_index, source_atom_index
                    ],
                    to_unit="angstrom",
                )[np.newaxis, :]
                location_ids = [""]
                occupancies = [
                    0.0
                    if item.structures.occupancy is None
                    else item.structures.occupancy[
                        structure_index, source_atom_index
                    ]
                ]
                b_factors = [
                    0.0
                    if item.structures.b_factor is None
                    else puw.get_value(
                        item.structures.b_factor[
                            structure_index, source_atom_index
                        ],
                        to_unit="angstrom**2",
                    )
                ]
            else:
                coordinates = puw.get_value(
                    alternate["coordinates"], to_unit="angstrom"
                )
                location_ids = alternate["location_id"]
                occupancies = alternate["occupancy"]
                b_factors = puw.get_value(
                    alternate["b_factor"], to_unit="angstrom**2"
                )
            _validate_coordinates(coordinates)

            group = groups.iloc[int(atom.group_index)]
            raw_chain_id = chains.iloc[int(atom.chain_index)][chain_column]
            chain_id = "A" if pd.isna(raw_chain_id) else str(raw_chain_id)
            element_symbol = "" if pd.isna(atom.atom_type) else str(atom.atom_type)
            charge = (
                None
                if formal_charge is None
                else formal_charge.iloc[source_atom_index]
            )
            for variant_index, coordinates_value in enumerate(coordinates):
                x, y, z = coordinates_value
                location = str(location_ids[variant_index])[:1]
                lines.append(
                    f"{'ATOM':<6}{serial:>5} "
                    f"{str(atom.atom_name)[:4]:<4}{location:1}"
                    f"{str(group['group_name'])[:3]:>3} "
                    f"{chain_id[:1]:1}{str(group['group_id'])[:4]:>4}    "
                    f"{x:>8.3f}{y:>8.3f}{z:>8.3f}"
                    f"{float(occupancies[variant_index]):>6.2f}"
                    f"{float(b_factors[variant_index]):>6.2f}"
                    f"{'':10}{element_symbol[:2]:>2}"
                    f"{_charge_field(charge):>2}\n"
                )
                serial += 1
        if multiple_models:
            lines.append("ENDMDL\n")

    bonds = item.topology._get_chemical_state_bonds()
    selected_set = set(int(index) for index in source_atom_indices)
    written = set()
    for bond in bonds.itertuples():
        atom1 = int(bond.atom1_index)
        atom2 = int(bond.atom2_index)
        if atom1 not in selected_set or atom2 not in selected_set:
            continue
        pair = tuple(sorted((first_serial[atom1], first_serial[atom2])))
        if pair in written:
            continue
        written.add(pair)
        lines.append(f"CONECT{pair[0]:>5}{pair[1]:>5}\n")
    lines.append("END\n")
    return "".join(lines)
