import os
import numpy as np
from molsysmt._private.arg_digestion import arg_digest


def _parse_serial(s):
    """Parse a PDB serial-number field (5 chars).
    Handles decimal, uppercase-hex overflow (OpenMM/VMD), and hybrid-36 (Chimera).
    """
    s = s.strip()
    if not s:
        return 0
    try:
        return int(s)
    except ValueError:
        pass
    try:
        shifted = int(s, 16)
        return shifted - 10 * (16 ** 4) + 100000
    except ValueError:
        pass
    try:
        return int(s[0], 36) * 10000 + int(s[1:])
    except (ValueError, IndexError):
        pass
    return 0


def _read_pdb_lines(item):
    if hasattr(item.file, "seek"):
        item.file.seek(0)
    lines = item.file.readlines()
    if hasattr(item.file, "seek"):
        item.file.seek(0)
    return lines


def _parse_topology_from_lines(lines):
    atom_rows = []
    group_rows = []
    chain_rows = []
    bonded_atom_pairs = []

    serial_to_atom_index = {}
    group_key_to_index = {}
    chain_segment_to_index = {}
    bonded_pairs_seen = set()

    current_chain_segment = -1
    pending_new_chain = True
    previous_group_key = None

    inside_model = False
    first_model_finished = False

    for line in lines:
        record = line[0:6].strip()

        if record == "MODEL":
            if inside_model:
                continue
            inside_model = True
            if atom_rows:
                break
            continue

        if record == "ENDMDL":
            if inside_model:
                first_model_finished = True
                break
            continue

        if record == "TER":
            if atom_rows:
                pending_new_chain = True
            continue

        if record in ["ATOM", "HETATM"]:
            if first_model_finished:
                break

            if pending_new_chain:
                current_chain_segment += 1
                pending_new_chain = False

                chain_id = line[21].strip()
                if chain_id == "":
                    chain_id = " "
                chain_rows.append((chain_id, chain_id))
                chain_segment_to_index[current_chain_segment] = len(chain_rows) - 1

            atom_serial = str(_parse_serial(line[6:11]))
            atom_name = line[12:16].strip()
            group_name = line[17:20].strip()
            chain_id = line[21].strip()
            if chain_id == "":
                chain_id = " "
            group_id = line[22:26].strip()
            insertion_code = line[26]
            element_symbol = line[76:78].strip() or None

            group_key = (current_chain_segment, chain_id, group_id, insertion_code, group_name)
            if group_key != previous_group_key:
                group_rows.append((group_id, group_name, chain_segment_to_index[current_chain_segment]))
                group_key_to_index[group_key] = len(group_rows) - 1
                previous_group_key = group_key

            atom_index = len(atom_rows)
            serial_to_atom_index[int(atom_serial)] = atom_index
            atom_rows.append(
                (
                    atom_serial,
                    atom_name,
                    element_symbol,
                    group_key_to_index[group_key],
                    chain_segment_to_index[current_chain_segment],
                )
            )
            continue

        if record == "CONECT":
            try:
                atom_serial = _parse_serial(line[6:11])
            except Exception:
                continue

            if atom_serial not in serial_to_atom_index:
                continue

            for start in [11, 16, 21, 26]:
                bonded_serial = line[start:start + 5].strip()
                if bonded_serial == "":
                    continue
                try:
                    bonded_serial = _parse_serial(bonded_serial)
                except Exception:
                    continue
                if bonded_serial not in serial_to_atom_index:
                    continue

                pair = tuple(sorted((serial_to_atom_index[atom_serial], serial_to_atom_index[bonded_serial])))
                if pair[0] == pair[1] or pair in bonded_pairs_seen:
                    continue
                bonded_pairs_seen.add(pair)
                bonded_atom_pairs.append(pair)

    return atom_rows, group_rows, chain_rows, bonded_atom_pairs


def _build_structures_from_lines(lines, entry):
    from molsysmt.native import Structures
    from molsysmt import pyunitwizard as puw
    from molsysmt import lib as msmlib

    models = []
    current_model = []
    inside_model = False
    saw_explicit_model = False

    for line in lines:
        record = line[0:6].strip()
        if record == "MODEL":
            if current_model:
                models.append(current_model)
                current_model = []
            inside_model = True
            saw_explicit_model = True
            continue
        if record == "ENDMDL":
            models.append(current_model)
            current_model = []
            inside_model = False
            continue
        if record in ["ATOM", "HETATM"]:
            try:
                bfac = float(line[60:66])
            except (ValueError, IndexError):
                bfac = 0.0
            current_model.append(
                [float(line[30:38]), float(line[38:46]), float(line[46:54]), bfac]
            )

    if current_model:
        models.append(current_model)

    if not models:
        return Structures()

    if not saw_explicit_model:
        models = [models[0]]

    n_structures = len(models)

    models_array = np.array(models, dtype=float)
    coordinates = models_array[:, :, :3] * puw.unit("angstroms")
    coordinates = puw.convert(coordinates, to_unit="nanometers")

    b_factor_raw = models_array[:, :, 3]  # shape (n_structures, n_atoms)
    if np.any(b_factor_raw != 0.0):
        b_factor = b_factor_raw * puw.unit("angstroms**2")
        b_factor = puw.convert(b_factor, to_unit="nanometers**2")
    else:
        b_factor = None

    if saw_explicit_model:
        structure_id = np.arange(1, n_structures + 1, dtype=int).astype(str)
    else:
        structure_id = np.array(["1"], dtype=object)

    box = None
    cryst1 = entry.crystallographic_and_coordinate_transformation.cryst1
    if cryst1 is not None:
        lengths = np.array([cryst1.a, cryst1.b, cryst1.c], dtype=float) * puw.unit("angstroms")
        angles = np.array([cryst1.alpha, cryst1.beta, cryst1.gamma], dtype=float) * puw.unit("degrees")
        single_box_value = msmlib.pbc.get_box_from_lengths_and_angles_single_structure(
            np.array(puw.get_value(lengths), dtype=np.float64),
            np.array(puw.get_value(angles, to_unit="radians"), dtype=np.float64),
        )
        box_value = np.repeat(single_box_value[np.newaxis, :, :], n_structures, axis=0)
        box = box_value * puw.unit("angstroms")
        box = puw.convert(box, to_unit="nanometers")

    structures = Structures()
    structures.append(coordinates=coordinates, structure_id=structure_id, box=box,
                      b_factor=b_factor, skip_digestion=True)

    return structures


def _get_group_types(group_rows, atom_rows):
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.element.group.small_molecule.group_names import group_names as reserved_small_molecule_names

    atom_names_by_group_index = {}
    for _, atom_name, _, group_index, _ in atom_rows:
        atom_names_by_group_index.setdefault(int(group_index), set()).add(atom_name)

    group_types = []
    for group_index, (_, group_name, _) in enumerate(group_rows):
        group_type = get_group_type_from_group_name(group_name)
        if (
            group_type == 'small molecule'
            and reserved_small_molecule_names is not None
            and group_name in reserved_small_molecule_names
        ):
            atom_names = atom_names_by_group_index.get(group_index, set())
            if {'N', 'CA', 'C', 'O', 'CB'}.issubset(atom_names):
                group_type = 'amino acid'
        group_types.append(group_type)

    return np.array(group_types, dtype=object)


def _get_bonded_atom_pairs_from_openmm_pdb(item):
    from io import StringIO
    from openmm.app import PDBFile

    if hasattr(item.file, "name") and isinstance(item.file.name, str) and os.path.isfile(item.file.name):
        pdb = PDBFile(item.file.name)
    else:
        pdb = PDBFile(StringIO("".join(_read_pdb_lines(item))))

    return [(bond.atom1.index, bond.atom2.index) for bond in pdb.topology.bonds()]


def _build_molsys_from_pdb_handler(item, get_missing_bonds=True):
    from molsysmt.native import MolSys

    lines = _read_pdb_lines(item)
    atom_rows, group_rows, chain_rows, bonded_atom_pairs = _parse_topology_from_lines(lines)

    tmp_item = MolSys()
    tmp_item.topology.reset_atoms(n_atoms=len(atom_rows))
    tmp_item.topology.reset_groups(n_groups=len(group_rows))
    tmp_item.topology.reset_chains(n_chains=len(chain_rows))

    if atom_rows:
        tmp_item.topology.atoms["atom_id"] = np.array([row[0] for row in atom_rows], dtype=object)
        tmp_item.topology.atoms["atom_name"] = np.array([row[1] for row in atom_rows], dtype=object)
        from molsysmt.element.atom import get_atom_type_from_atom_name
        atom_types = []
        for row in atom_rows:
            t = row[2]
            if t is None:
                t = get_atom_type_from_atom_name(row[1])
            atom_types.append(t)
        tmp_item.topology.atoms["atom_type"] = np.array(atom_types, dtype=object)
        tmp_item.topology.atoms["group_index"] = np.array([row[3] for row in atom_rows], dtype=int)
        tmp_item.topology.atoms["chain_index"] = np.array([row[4] for row in atom_rows], dtype=int)

    tmp_item.topology.rebuild_atoms(redefine_ids=False, redefine_types=False)

    if group_rows:
        tmp_item.topology.groups["group_id"] = np.array([row[0] for row in group_rows], dtype=object)
        tmp_item.topology.groups["group_name"] = np.array([row[1] for row in group_rows], dtype=object)
        tmp_item.topology.groups["chain_index"] = np.array([row[2] for row in group_rows], dtype=int)
        tmp_item.topology.groups["group_type"] = _get_group_types(group_rows, atom_rows)

    if chain_rows:
        tmp_item.topology.chains["chain_id"] = np.array([row[0] for row in chain_rows], dtype=object)
        tmp_item.topology.chains["chain_name"] = np.array([row[1] for row in chain_rows], dtype=object)

    tmp_item.structures = _build_structures_from_lines(lines, item.entry)

    if get_missing_bonds:
        try:
            inferred_bonded_atom_pairs = _get_bonded_atom_pairs_from_openmm_pdb(item)
        except Exception:
            inferred_bonded_atom_pairs = []

        if inferred_bonded_atom_pairs:
            bonded_atom_pairs = sorted(set(tuple(sorted(pair)) for pair in bonded_atom_pairs).union(
                tuple(sorted(pair)) for pair in inferred_bonded_atom_pairs
            ))

    if bonded_atom_pairs:
        tmp_item.topology.add_bonds(bonded_atom_pairs, skip_digestion=True)
        tmp_item.topology.rebuild_molecules(force=True)
        tmp_item.topology.rebuild_chains(redefine_indices=False, redefine_ids=False, redefine_names=False, redefine_types=True)
        tmp_item.topology.rebuild_entities(force=True)

    # ── Apply COMPND molecule names ──────────────────────────────────────────
    # Build chain_id → molecule_name map from COMPND records.
    compnd = getattr(getattr(item.entry, 'title', None), 'compnd', None)
    if compnd:
        chain_to_name = {}
        for rec in compnd:
            name = rec.molecule.lstrip(': ').strip() if rec.molecule else None
            if name:
                for ch in rec.chain:
                    chain_to_name[ch] = name

        if chain_to_name:
            # Map molecule_index → chain_id via groups['molecule_index'] and chains['chain_id']
            grp_mol   = tmp_item.topology.groups['molecule_index'].to_numpy()
            grp_chain = tmp_item.topology.groups['chain_index'].to_numpy()
            chain_ids_arr = tmp_item.topology.chains['chain_id'].to_numpy()
            mol_names = tmp_item.topology.molecules['molecule_name'].to_numpy(dtype=object)
            mol_types = tmp_item.topology.molecules['molecule_type'].to_numpy(dtype=object)
            # Build molecule → first chain_id (take the chain of the first group in the molecule)
            mol_to_chain_id = {}
            for grp_idx in range(len(grp_mol)):
                mol_idx = grp_mol[grp_idx]
                if mol_idx not in mol_to_chain_id:
                    mol_to_chain_id[mol_idx] = chain_ids_arr[grp_chain[grp_idx]]
            for mol_idx in range(len(mol_names)):
                if mol_types[mol_idx] not in ('protein', 'peptide'):
                    continue
                chain_id = mol_to_chain_id.get(mol_idx)
                if chain_id in chain_to_name:
                    mol_names[mol_idx] = chain_to_name[chain_id]
            tmp_item.topology.molecules['molecule_name'] = mol_names
            # Re-infer entity names so they reflect the updated molecule names
            tmp_item.topology.rebuild_entities(force=True)

    return tmp_item


@arg_digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=True, skip_digestion=False):

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_PDBFileHandler(str(item), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    tmp_item = _build_molsys_from_pdb_handler(item, get_missing_bonds=get_missing_bonds)
    tmp_item = tmp_item.extract(atom_indices=atom_indices, structure_indices=structure_indices,
                                copy_if_all=False, skip_digestion=True)

    if opened_here:
        item.close()

    return tmp_item
