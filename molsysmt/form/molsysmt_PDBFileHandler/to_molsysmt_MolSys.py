import os

import numpy as np
import pandas as pd

from molsysmt._private.argdigest import arg_digest


def _site_variants(model):
    output = {}
    for atom in model.atoms:
        output.setdefault(atom.site_key, []).append(atom)
    return output


def _canonical_atoms(content):
    if not content.models:
        return [], {}
    variants = _site_variants(content.models[0])
    return [items[0] for items in variants.values()], variants


def _topology_rows(content):
    canonical_atoms, variants = _canonical_atoms(content)
    group_rows = []
    chain_rows = []
    group_indices = {}
    chain_indices = {}

    for atom in canonical_atoms:
        chain_key = (atom.chain_segment, atom.chain_id)
        if chain_key not in chain_indices:
            chain_indices[chain_key] = len(chain_rows)
            chain_rows.append((atom.chain_id, atom.chain_id))
        group_key = (
            atom.chain_segment,
            atom.chain_id,
            atom.group_id,
            atom.insertion_code,
            atom.group_name,
        )
        if group_key not in group_indices:
            group_indices[group_key] = len(group_rows)
            group_rows.append((
                atom.group_id,
                atom.group_name,
                chain_indices[chain_key],
            ))

    atom_rows = []
    for atom in canonical_atoms:
        group_key = (
            atom.chain_segment,
            atom.chain_id,
            atom.group_id,
            atom.insertion_code,
            atom.group_name,
        )
        chain_key = (atom.chain_segment, atom.chain_id)
        atom_rows.append((
            str(atom.serial),
            atom.atom_name,
            atom.element_symbol,
            group_indices[group_key],
            chain_indices[chain_key],
        ))
    return atom_rows, group_rows, chain_rows, canonical_atoms, variants


def _get_group_types(group_rows, atom_rows):
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.element.group.small_molecule.group_names import (
        group_names as reserved_small_molecule_names,
    )

    atom_names_by_group_index = {}
    for _, atom_name, _, group_index, _ in atom_rows:
        atom_names_by_group_index.setdefault(int(group_index), set()).add(atom_name)

    group_types = []
    for group_index, (_, group_name, _) in enumerate(group_rows):
        group_type = get_group_type_from_group_name(group_name)
        if (
            group_type == "small molecule"
            and reserved_small_molecule_names is not None
            and group_name in reserved_small_molecule_names
            and {"N", "CA", "C", "O", "CB"}.issubset(
                atom_names_by_group_index.get(group_index, set())
            )
        ):
            group_type = "amino acid"
        group_types.append(group_type)
    return np.array(group_types, dtype=object)


def _resolve_link_endpoint(canonical_atoms, endpoint):
    chain_id, group_id, insertion_code, group_name, atom_name, _ = endpoint
    return [
        atom_index
        for atom_index, atom in enumerate(canonical_atoms)
        if (
            atom.chain_id == chain_id
            and atom.group_id == group_id
            and atom.insertion_code == insertion_code
            and atom.group_name == group_name
            and atom.atom_name == atom_name
        )
    ]


def _resolve_ssbond_endpoint(canonical_atoms, endpoint):
    chain_id, group_id, insertion_code = endpoint
    return [
        atom_index
        for atom_index, atom in enumerate(canonical_atoms)
        if (
            atom.chain_id == chain_id
            and atom.group_id == group_id
            and atom.insertion_code == insertion_code
            and atom.group_name == "CYS"
            and atom.atom_name == "SG"
        )
    ]


def _get_explicit_bonds(content, canonical_atoms, variants):
    serial_to_indices = {}
    for atom_index, items in enumerate(variants.values()):
        for item in items:
            serial_to_indices.setdefault(item.serial, set()).add(atom_index)

    pairs = set()
    repeated_pairs = set()
    unresolved = False
    for record in content.conect:
        for target in record.target_serials:
            sources = serial_to_indices.get(record.source_serial, set())
            targets = serial_to_indices.get(target, set())
            if len(sources) != 1 or len(targets) != 1:
                unresolved = True
                continue
            pair = tuple(sorted((next(iter(sources)), next(iter(targets)))))
            if pair[0] == pair[1]:
                continue
            if pair in pairs:
                repeated_pairs.add(pair)
            pairs.add(pair)

    for record in content.links:
        endpoint1 = _resolve_link_endpoint(canonical_atoms, record.endpoint1)
        endpoint2 = _resolve_link_endpoint(canonical_atoms, record.endpoint2)
        if len(endpoint1) != 1 or len(endpoint2) != 1:
            unresolved = True
            continue
        pair = tuple(sorted((endpoint1[0], endpoint2[0])))
        if pair[0] != pair[1]:
            pairs.add(pair)

    for record in content.ssbonds:
        endpoint1 = _resolve_ssbond_endpoint(canonical_atoms, record.endpoint1)
        endpoint2 = _resolve_ssbond_endpoint(canonical_atoms, record.endpoint2)
        if len(endpoint1) != 1 or len(endpoint2) != 1:
            unresolved = True
            continue
        pair = tuple(sorted((endpoint1[0], endpoint2[0])))
        if pair[0] != pair[1]:
            pairs.add(pair)

    return sorted(pairs), unresolved, bool(repeated_pairs)


def _get_bonded_atom_pairs_from_openmm_pdb(item):
    from io import StringIO
    from openmm.app import PDBFile

    item.file.seek(0)
    text = item.file.read()
    item.file.seek(0)
    pdb = PDBFile(StringIO(text))
    _, variants = _canonical_atoms(item.content)
    serial_to_site_index = {}
    for site_index, records in enumerate(variants.values()):
        for record in records:
            serial_to_site_index.setdefault(str(record.serial), site_index)

    openmm_to_site_index = {}
    openmm_atoms = list(pdb.topology.atoms())
    for atom in openmm_atoms:
        atom_id = getattr(atom, "id", None)
        if atom_id is not None and str(atom_id) in serial_to_site_index:
            openmm_to_site_index[atom.index] = serial_to_site_index[str(atom_id)]
        elif len(openmm_atoms) == len(variants):
            openmm_to_site_index[atom.index] = atom.index

    output = []
    for bond in pdb.topology.bonds():
        if (
            bond.atom1.index in openmm_to_site_index
            and bond.atom2.index in openmm_to_site_index
        ):
            output.append((
                openmm_to_site_index[bond.atom1.index],
                openmm_to_site_index[bond.atom2.index],
            ))
    return output


def _build_topology_from_content(item, get_missing_bonds=True):
    from molsysmt.native import Topology

    content = item.content
    (
        atom_rows,
        group_rows,
        chain_rows,
        canonical_atoms,
        variants,
    ) = _topology_rows(content)

    topology = Topology()
    topology.reset_atoms(n_atoms=len(atom_rows))
    topology.reset_groups(n_groups=len(group_rows))
    topology.reset_chains(n_chains=len(chain_rows))

    if atom_rows:
        topology.atoms["atom_id"] = np.array(
            [row[0] for row in atom_rows], dtype=object
        )
        topology.atoms["atom_name"] = np.array(
            [row[1] for row in atom_rows], dtype=object
        )
        from molsysmt.element.atom import get_atom_type_from_atom_name

        topology.atoms["atom_type"] = np.array([
            row[2] or get_atom_type_from_atom_name(row[1]) for row in atom_rows
        ], dtype=object)
        topology.atoms["group_index"] = np.array(
            [row[3] for row in atom_rows], dtype=int
        )
        topology.atoms["chain_index"] = np.array(
            [row[4] for row in atom_rows], dtype=int
        )
    topology.rebuild_atoms(redefine_ids=False, redefine_types=False)

    if group_rows:
        topology.groups["group_id"] = np.array(
            [row[0] for row in group_rows], dtype=object
        )
        topology.groups["group_name"] = np.array(
            [row[1] for row in group_rows], dtype=object
        )
        topology.groups["group_type"] = _get_group_types(group_rows, atom_rows)
    if chain_rows:
        topology.chains["chain_id"] = np.array(
            [row[0] for row in chain_rows], dtype=object
        )
        topology.chains["chain_name"] = np.array(
            [row[1] for row in chain_rows], dtype=object
        )

    formal_charges = [atom.formal_charge for atom in canonical_atoms]
    if any(value is not None for value in formal_charges):
        topology._set_chemical_state_atom_attribute(
            "formal_charge", pd.array(formal_charges, dtype="Int16")
        )

    explicit_pairs, _, _ = _get_explicit_bonds(
        content, canonical_atoms, variants
    )
    bond_evidence = {pair: "explicit" for pair in explicit_pairs}
    if get_missing_bonds:
        try:
            inferred_pairs = _get_bonded_atom_pairs_from_openmm_pdb(item)
        except Exception:
            inferred_pairs = []
        for pair in inferred_pairs:
            normalized = tuple(sorted((int(pair[0]), int(pair[1]))))
            if (
                normalized[0] != normalized[1]
                and normalized[1] < len(canonical_atoms)
            ):
                bond_evidence.setdefault(normalized, "inferred")

    if bond_evidence:
        pairs = sorted(bond_evidence)
        topology._append_chemical_state_bonds(
            pairs,
            types=["covalent"] * len(pairs),
            evidence=[bond_evidence[pair] for pair in pairs],
        )
        topology.rebuild_molecules(force=True)
        topology.rebuild_chains(
            redefine_indices=False,
            redefine_ids=False,
            redefine_names=False,
            redefine_types=True,
        )
        topology.rebuild_entities(force=True)

    return topology


def _build_bioassemblies(content, chain_rows):
    from molsysmt import pyunitwizard as puw

    chain_indices_by_id = {}
    for chain_index, (chain_id, _) in enumerate(chain_rows):
        chain_indices_by_id.setdefault(chain_id, []).append(chain_index)

    output = {}
    for assembly_id, operations in content.bioassemblies.items():
        chain_sets = []
        rotations = []
        translations = []
        for operation in operations:
            indices = []
            for chain_id in operation["chain_ids"]:
                indices.extend(chain_indices_by_id.get(chain_id, []))
            if not indices:
                continue
            chain_sets.append(indices)
            rotations.append(operation["rotation"])
            translations.append(operation["translation"])
        if not rotations:
            continue
        chain_indices = (
            chain_sets[0]
            if all(indices == chain_sets[0] for indices in chain_sets)
            else chain_sets
        )
        output[assembly_id] = {
            "chain_indices": chain_indices,
            "rotations": np.asarray(rotations, dtype=float),
            "translations": puw.quantity(
                np.asarray(translations, dtype=float), "angstrom"
            ),
        }
    return output or None


def _build_structures_from_content(item):
    from molsysmt import pyunitwizard as puw
    from molsysmt.native import Structures
    from molsysmt._private import rust_backend as _kernels

    content = item.content
    atom_rows, _, chain_rows, canonical_atoms, _ = _topology_rows(content)
    if not content.models:
        return Structures()

    canonical_keys = [atom.site_key for atom in canonical_atoms]
    coordinates = []
    occupancies = []
    b_factors = []
    alternate_locations = []
    for model in content.models:
        variants = _site_variants(model)
        if set(variants) != set(canonical_keys):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="PDB models do not share one canonical atom-site axis.",
                caller="molsysmt.PDBFileHandler",
            )
        primary = [variants[key][0] for key in canonical_keys]
        coordinates.append([atom.coordinates for atom in primary])
        occupancies.append([
            np.nan if atom.occupancy is None else atom.occupancy for atom in primary
        ])
        b_factors.append([
            np.nan if atom.b_factor is None else atom.b_factor for atom in primary
        ])
        model_alternates = {}
        for atom_index, key in enumerate(canonical_keys):
            items = variants[key]
            if len(items) < 2 and not items[0].alternate_location:
                continue
            model_alternates[atom_index] = {
                "location_id": np.array(
                    [atom.alternate_location for atom in items], dtype=object
                ),
                "atom_id": np.array(
                    [str(atom.serial) for atom in items], dtype=object
                ),
                "occupancy": np.array(
                    [
                        np.nan if atom.occupancy is None else atom.occupancy
                        for atom in items
                    ],
                    dtype=float,
                ),
                "coordinates": puw.quantity(
                    np.array([atom.coordinates for atom in items], dtype=float),
                    "angstrom",
                ),
                "b_factor": puw.quantity(
                    np.array(
                        [
                            np.nan if atom.b_factor is None else atom.b_factor
                            for atom in items
                        ],
                        dtype=float,
                    ),
                    "angstrom**2",
                ),
            }
            model_alternates[atom_index]["coordinates"] = puw.convert(
                model_alternates[atom_index]["coordinates"], to_unit="nm"
            )
            model_alternates[atom_index]["b_factor"] = puw.convert(
                model_alternates[atom_index]["b_factor"], to_unit="nm**2"
            )
        alternate_locations.append(model_alternates)

    coordinates = puw.quantity(np.asarray(coordinates, dtype=float), "angstrom")
    occupancy = np.asarray(occupancies, dtype=float)
    b_factor = puw.quantity(np.asarray(b_factors, dtype=float), "angstrom**2")
    if np.isnan(occupancy).all():
        occupancy = None
    if np.isnan(puw.get_value(b_factor)).all():
        b_factor = None
    if not any(alternate_locations):
        alternate_locations = None

    box = None
    if content.cryst1 is not None:
        a, b, c, alpha, beta, gamma = content.cryst1
        single_box = _kernels.get_box_from_lengths_and_angles_single_structure(
            np.array([a, b, c], dtype=np.float64),
            np.array(
                puw.get_value(
                    puw.quantity([alpha, beta, gamma], "degrees"),
                    to_unit="radians",
                ),
                dtype=np.float64,
            ),
        )
        box = puw.quantity(
            np.repeat(single_box[np.newaxis, :, :], len(content.models), axis=0),
            "angstrom",
        )

    structures = Structures()
    structures.append(
        coordinates=coordinates,
        structure_id=np.array(
            [model.structure_id for model in content.models], dtype=object
        ),
        box=box,
        occupancy=occupancy,
        b_factor=b_factor,
        alternate_location=alternate_locations,
        skip_digestion=True,
    )
    structures.bioassembly = _build_bioassemblies(content, chain_rows)
    return structures


def _apply_compnd_names(item, molsys):
    compnd = getattr(getattr(item.entry, "title", None), "compnd", None)
    if not compnd:
        return
    chain_to_name = {}
    for record in compnd:
        name = record.molecule.lstrip(": ").strip() if record.molecule else None
        if name:
            for chain_id in record.chain:
                chain_to_name[chain_id] = name
    if not chain_to_name:
        return

    atoms = molsys.topology.atoms
    groups = molsys.topology.groups
    chain_ids = molsys.topology.chains["chain_id"].to_numpy()
    molecule_names = molsys.topology.molecules["molecule_name"].to_numpy(dtype=object)
    molecule_types = molsys.topology.molecules["molecule_type"].to_numpy(dtype=object)
    for molecule_index in range(len(molecule_names)):
        if molecule_types[molecule_index] not in {"protein", "peptide"}:
            continue
        group_indices = groups.index[
            groups["molecule_index"] == molecule_index
        ].to_numpy()
        atom_indices = atoms.index[atoms["group_index"].isin(group_indices)].to_numpy()
        if len(atom_indices):
            chain_id = chain_ids[int(atoms.iloc[atom_indices[0]]["chain_index"])]
            if chain_id in chain_to_name:
                molecule_names[molecule_index] = chain_to_name[chain_id]
    molsys.topology.molecules["molecule_name"] = molecule_names
    molsys.topology.rebuild_entities(force=True)


def _build_molsys_from_pdb_handler(item, get_missing_bonds=True):
    from molsysmt.native import MolSys

    output = MolSys()
    output.topology = _build_topology_from_content(
        item, get_missing_bonds=get_missing_bonds
    )
    output.structures = _build_structures_from_content(item)
    _apply_compnd_names(item, output)
    return output


@arg_digest(form="molsysmt.PDBFileHandler")
def to_molsysmt_MolSys(
    item,
    atom_indices="all",
    structure_indices="all",
    get_missing_bonds=True,
    skip_digestion=False,
):
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_PDBFileHandler(str(item), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    output = _build_molsys_from_pdb_handler(
        item, get_missing_bonds=get_missing_bonds
    )
    output = output.extract(
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )
    if opened_here:
        item.close()
    return output
