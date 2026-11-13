import re
from pathlib import Path

import pytest

import molsysmt as msm
from molsysmt import systems


@pytest.fixture(autouse=True)
def restore_pyunitwizard_config():
    yield
    import pyunitwizard as puw

    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(
        [
            "nm",
            "ps",
            "K",
            "mole",
            "dalton",
            "e",
            "kJ/mol",
            "kJ/(mol*nm)",
            "kJ/(mol*nm**2)",
            "radians",
        ]
    )


# ---------------------------------------------------------------------------
# Auto-apply tier marks to tests under tests/form/<form_dir>/
# Tier is derived from molsysmt._private.form_tier.FORM_TIERS (single source
# of truth). Every adapter must be registered explicitly.
# ---------------------------------------------------------------------------


def _build_form_dir_tier_map():
    """Return {form_directory_name: tier_int} for all known form adapters."""
    import molsysmt.form as _msm_form_pkg
    from molsysmt._private.form_tier import FORM_TIERS

    form_base = Path(_msm_form_pkg.__file__).parent
    pattern = re.compile(r"^form_name\s*=\s*['\"]([^'\"]+)['\"]", re.MULTILINE)

    mapping = {}
    for form_dir in sorted(form_base.iterdir()):
        if not form_dir.is_dir() or form_dir.name.startswith("_"):
            continue
        init_file = form_dir / "__init__.py"
        if not init_file.exists():
            continue
        text = init_file.read_text()
        m = pattern.search(text)
        if m:
            form_name = m.group(1)
            tier = FORM_TIERS[form_name]
            mapping[form_dir.name] = tier
    return mapping


_FORM_DIR_TIER: dict | None = None


def pytest_collection_modifyitems(config, items):
    global _FORM_DIR_TIER
    if _FORM_DIR_TIER is None:
        _FORM_DIR_TIER = _build_form_dir_tier_map()

    for item in items:
        parts = Path(str(item.fspath)).parts
        if "form" not in parts:
            continue
        form_idx = list(parts).index("form")
        if form_idx + 1 >= len(parts):
            continue
        form_dir_name = parts[form_idx + 1]
        tier = _FORM_DIR_TIER.get(form_dir_name)
        if tier is None:
            continue
        item.add_marker(getattr(pytest.mark, f"tier{tier}"))

    # Auto-deselect peptide_parity tests unless the user explicitly requests
    # them via -m "peptide_parity".  This keeps the default test run fast and
    # avoids a mandatory tleap dependency.  To run: pytest -m "peptide_parity".
    mark_expr = getattr(config.option, "markexpr", "") or ""
    if "peptide_parity" not in mark_expr:
        deselected = [
            item for item in items if item.get_closest_marker("peptide_parity")
        ]
        if deselected:
            config.hook.pytest_deselected(items=deselected)
            items[:] = [
                item for item in items if not item.get_closest_marker("peptide_parity")
            ]


# Base loaders (session scope) to avoid repeated IO/parsing


@pytest.fixture(scope="session")
def _base_hp35_solvated_molsys():
    molsys = msm.convert(
        systems["chicken villin HP35"]["chicken_villin_HP35_solvated.h5msm"],
        to_form="molsysmt.MolSys",
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_hp35_molsys():
    molsys = msm.convert(
        systems["chicken villin HP35"]["chicken_villin_HP35.h5msm"],
        to_form="molsysmt.MolSys",
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_hp35_bcif_molsys():
    molsys = msm.convert(
        systems["chicken villin HP35"]["1vii.bcif.gz"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_met_enkephalin_pdb_molsys():
    molsys = msm.convert(
        systems["Met-enkephalin"]["met_enkephalin.pdb"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_met_enkephalin_h5msm_molsys():
    molsys = msm.convert(
        systems["Met-enkephalin"]["met_enkephalin.h5msm"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_traj_pentalanine_h5_molsys():
    molsys = msm.convert(
        systems["pentalanine"]["traj_pentalanine.h5"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_barnase_barstar_molsys():
    molsys = msm.convert(msm.systems["Barnase-Barstar"]["barnase_barstar.h5msm"])
    assert molsys is not None
    return molsys


# Small systems for structure/geometry tests


@pytest.fixture(scope="session")
def _base_alanine_molsys():
    molsys = msm.convert(
        systems["alanine dipeptide"]["alanine_dipeptide.h5msm"],
        to_form="molsysmt.MolSys",
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_proline_molsys():
    molsys = msm.convert(
        systems["proline dipeptide"]["proline_dipeptide.h5msm"],
        to_form="molsysmt.MolSys",
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_valine_molsys():
    molsys = msm.convert(
        systems["valine dipeptide"]["valine_dipeptide.h5msm"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_lysine_molsys():
    molsys = msm.convert(
        systems["lysine dipeptide"]["lysine_dipeptide.h5msm"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


# Alternate formats for HP35


@pytest.fixture(scope="session")
def _base_hp35_pdb_molsys():
    molsys = msm.convert(
        systems["chicken villin HP35"]["1vii.pdb"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


# T4 lysozyme variants


@pytest.fixture(scope="session")
def _base_t4_h5msm_molsys():
    molsys = msm.convert(
        systems["T4 lysozyme L99A"]["181l.h5msm"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_t4_pdb_molsys():
    molsys = msm.convert(
        systems["T4 lysozyme L99A"]["181l.pdb"], to_form="molsysmt.MolSys"
    )
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_t4_pdb_text():
    pdb_text = msm.convert(
        systems["T4 lysozyme L99A"]["181l.pdb"], to_form="string:pdb_text"
    )
    assert pdb_text is not None
    return pdb_text


@pytest.fixture(scope="session")
def _base_t4_written_pdb_text(_base_t4_pdb_molsys):
    pdb_text = msm.convert(_base_t4_pdb_molsys, to_form="string:pdb_text")
    assert pdb_text is not None
    return pdb_text


@pytest.fixture(scope="session")
def _base_md_1u19_pdb_molsys():
    molsys = msm.convert(systems["nglview"]["md_1u19.pdb"], to_form="molsysmt.MolSys")
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_md_1u19_pdb_text():
    pdb_text = msm.convert(systems["nglview"]["md_1u19.pdb"], to_form="string:pdb_text")
    assert pdb_text is not None
    return pdb_text


@pytest.fixture(scope="session")
def _base_builder_pdb_molsys():
    import numpy as np

    from molsysmt import pyunitwizard as puw

    builder = msm.MolSysBuilder()
    atom_indices = [builder.add_atom(atom_name=name) for name in ["N", "CA", "C", "O"]]
    group_index_0 = builder.add_group(atom_indices[:3], group_id="10", group_name="ALA")
    group_index_1 = builder.add_group(atom_indices[3:], group_id="11", group_name="HOH")
    builder.add_bond(atom_indices[0], atom_indices[1])
    builder.add_bond(atom_indices[1], atom_indices[2])
    builder.add_chain([group_index_0, group_index_1], chain_id="A", chain_name="A")
    molecule_index_0 = builder.add_molecule(
        [group_index_0],
        molecule_id="20",
        molecule_name="protein 0",
        molecule_type="protein",
    )
    molecule_index_1 = builder.add_molecule(
        [group_index_1], molecule_id="21", molecule_name="water", molecule_type="water"
    )
    builder.add_entity(
        [molecule_index_0],
        entity_id="30",
        entity_name="protein 0",
        entity_type="protein",
    )
    builder.add_entity(
        [molecule_index_1], entity_id="31", entity_name="water", entity_type="water"
    )
    builder.set_coordinates(
        puw.quantity(
            np.array(
                [
                    [0.0, 0.0, 0.0],
                    [0.1, 0.0, 0.0],
                    [0.2, 0.0, 0.0],
                    [0.3, 0.0, 0.0],
                ]
            ),
            "nm",
        )
    )
    builder.set_box(puw.quantity(np.eye(3)[np.newaxis, :, :], "nm"))
    builder.set_time(puw.quantity(np.array([0.0]), "ps"))
    builder.set_structure_id([0])
    molsys = builder.build()
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_builder_pdb_text(_base_builder_pdb_molsys):
    pdb_text = msm.convert(_base_builder_pdb_molsys, to_form="string:pdb_text")
    assert pdb_text is not None
    return pdb_text


@pytest.fixture()
def builder_pdb_molsys(_base_builder_pdb_molsys):
    return _base_builder_pdb_molsys.copy()


@pytest.fixture()
def builder_pdb_text(_base_builder_pdb_text):
    return _base_builder_pdb_text


@pytest.fixture()
def builder_pdb_handler(builder_pdb_text):
    return msm.convert(builder_pdb_text, to_form="molsysmt.PDBFileHandler")


@pytest.fixture(scope="session")
def _base_builder_h5msm_file(_base_builder_pdb_molsys, tmp_path_factory):
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import (
        to_file_h5msm as write_legacy_h5msm,
    )

    output_path = (
        tmp_path_factory.mktemp("builder_h5msm_assets") / "builder_fixture.h5msm"
    )
    write_legacy_h5msm(
        _base_builder_pdb_molsys,
        output_filename=str(output_path),
        skip_digestion=True,
    )
    assert output_path.is_file()
    return str(output_path)


@pytest.fixture()
def builder_h5msm_file(_base_builder_h5msm_file):
    return _base_builder_h5msm_file


@pytest.fixture()
def builder_h5msm_handler(builder_h5msm_file):
    return msm.convert(builder_h5msm_file, to_form="molsysmt.H5MSMFileHandler")


@pytest.fixture()
def builder_openmm_topology(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys, to_form="openmm.Topology")


@pytest.fixture()
def builder_structures(builder_pdb_molsys):
    return builder_pdb_molsys.structures.copy()


# Multi-frame trajectory builder system
# Same topology as builder_pdb_molsys (N, CA, C, O / ALA+HOH / chain A) but
# with 3 distinct frames.  Used as the oracle for trajectory-form parity tests
# (file:xtc ↔ file:h5msm, mdtraj.Trajectory, etc.).


@pytest.fixture(scope="session")
def _base_builder_trajectory_molsys():
    import numpy as np

    from molsysmt import pyunitwizard as puw

    builder = msm.MolSysBuilder()
    atom_indices = [builder.add_atom(atom_name=name) for name in ["N", "CA", "C", "O"]]
    group_index_0 = builder.add_group(atom_indices[:3], group_id="10", group_name="ALA")
    group_index_1 = builder.add_group(atom_indices[3:], group_id="11", group_name="HOH")
    builder.add_bond(atom_indices[0], atom_indices[1])
    builder.add_bond(atom_indices[1], atom_indices[2])
    builder.add_chain([group_index_0, group_index_1], chain_id="A", chain_name="A")
    molecule_index_0 = builder.add_molecule(
        [group_index_0],
        molecule_id="20",
        molecule_name="protein 0",
        molecule_type="protein",
    )
    molecule_index_1 = builder.add_molecule(
        [group_index_1], molecule_id="21", molecule_name="water", molecule_type="water"
    )
    builder.add_entity(
        [molecule_index_0],
        entity_id="30",
        entity_name="protein 0",
        entity_type="protein",
    )
    builder.add_entity(
        [molecule_index_1], entity_id="31", entity_name="water", entity_type="water"
    )

    coords = np.array(
        [
            [[0.0, 0.0, 0.0], [0.1, 0.0, 0.0], [0.2, 0.0, 0.0], [0.3, 0.0, 0.0]],
            [[0.0, 0.1, 0.0], [0.1, 0.1, 0.0], [0.2, 0.1, 0.0], [0.3, 0.1, 0.0]],
            [[0.0, 0.2, 0.0], [0.1, 0.2, 0.0], [0.2, 0.2, 0.0], [0.3, 0.2, 0.0]],
        ],
        dtype=float,
    )  # shape (3, 4, 3), nm
    builder.set_coordinates(puw.quantity(coords, "nm"))
    builder.set_box(puw.quantity(np.tile(np.eye(3), (3, 1, 1)), "nm"))
    builder.set_time(puw.quantity(np.array([0.0, 1.0, 2.0]), "ps"))
    builder.set_structure_id([0, 1, 2])

    molsys = builder.build()
    assert molsys is not None
    return molsys


@pytest.fixture()
def builder_trajectory_molsys(_base_builder_trajectory_molsys):
    return _base_builder_trajectory_molsys.copy()


@pytest.fixture(scope="session")
def _base_builder_trajectory_h5msm_file(
    _base_builder_trajectory_molsys, tmp_path_factory
):
    output_path = (
        tmp_path_factory.mktemp("builder_traj_h5msm_assets")
        / "builder_trajectory.h5msm"
    )
    msm.convert(
        _base_builder_trajectory_molsys,
        to_form="file:h5msm",
        output_filename=str(output_path),
    )
    assert output_path.is_file()
    return str(output_path)


@pytest.fixture()
def builder_trajectory_h5msm_file(_base_builder_trajectory_h5msm_file):
    return _base_builder_trajectory_h5msm_file


@pytest.fixture(scope="session")
def _base_builder_trajectory_xtc_file(
    _base_builder_trajectory_molsys, tmp_path_factory
):
    # XTC can only be written via mdtraj; MolSys → mdtraj.Trajectory → .xtc
    output_path = (
        tmp_path_factory.mktemp("builder_traj_xtc_assets") / "builder_trajectory.xtc"
    )
    traj = msm.convert(_base_builder_trajectory_molsys, to_form="mdtraj.Trajectory")
    traj.save_xtc(str(output_path))
    assert output_path.is_file()
    return str(output_path)


@pytest.fixture()
def builder_trajectory_xtc_file(_base_builder_trajectory_xtc_file):
    return _base_builder_trajectory_xtc_file


@pytest.fixture()
def builder_mdtraj_trajectory(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys, to_form="mdtraj.Trajectory")


@pytest.fixture()
def builder_mdtraj_topology(builder_pdb_molsys):
    return msm.convert(builder_pdb_molsys, to_form="mdtraj.Topology")


# TcTIM systems


@pytest.fixture(scope="session")
def _base_tctim_h5msm_molsys():
    molsys = msm.convert(systems["TcTIM"]["1tcd.h5msm"], to_form="molsysmt.MolSys")
    assert molsys is not None
    return molsys


@pytest.fixture(scope="session")
def _base_tctim_bcif_molsys():
    molsys = msm.convert(systems["TcTIM"]["1tcd.bcif.gz"], to_form="molsysmt.MolSys")
    assert molsys is not None
    return molsys


# POPC systems


@pytest.fixture(scope="session")
def _base_popc_psf():
    path = systems["POPC"]["popc.psf"]
    assert path is not None
    return path


@pytest.fixture(scope="session")
def _base_popc_membrane_molsys():
    molsys = msm.convert(
        systems["POPC membrane"]["popc_membrane.dcd"], to_form="molsysmt.Structures"
    )
    assert molsys is not None
    return molsys


# Function-scoped copies to keep tests isolated


@pytest.fixture()
def hp35_solvated_molsys(_base_hp35_solvated_molsys):
    return _base_hp35_solvated_molsys.copy()


@pytest.fixture()
def hp35_molsys(_base_hp35_molsys):
    return _base_hp35_molsys.copy()


@pytest.fixture()
def hp35_bcif_molsys(_base_hp35_bcif_molsys):
    return _base_hp35_bcif_molsys.copy()


@pytest.fixture()
def hp35_bcif_file():
    return systems["chicken villin HP35"]["1vii.bcif"]


@pytest.fixture()
def hp35_bcif_gz_file():
    return systems["chicken villin HP35"]["1vii.bcif.gz"]


@pytest.fixture(scope="session")
def _base_hp35_cif_file(tmp_path_factory):
    from mmcif.io import IoAdapter

    tmp_dir = tmp_path_factory.mktemp("hp35_cif_assets")
    cif_path = tmp_dir / "1vii.cif"
    if not cif_path.exists():
        container = msm.convert(
            systems["chicken villin HP35"]["1vii.bcif.gz"],
            to_form="mmcif.PdbxContainers.DataContainer",
        )
        io = IoAdapter()
        io.writeFile(str(cif_path), [container])

    return str(cif_path)


@pytest.fixture()
def hp35_cif_file(_base_hp35_cif_file):
    return _base_hp35_cif_file


@pytest.fixture(scope="session")
def _base_hp35_cif_gz_file(tmp_path_factory, _base_hp35_cif_file):
    import gzip
    import shutil

    tmp_dir = tmp_path_factory.mktemp("hp35_cif_gz_assets")
    cif_gz_path = tmp_dir / "1vii.cif.gz"
    if not cif_gz_path.exists():
        with (
            open(_base_hp35_cif_file, "rb") as source,
            gzip.open(cif_gz_path, "wb") as destination,
        ):
            shutil.copyfileobj(source, destination)

    return str(cif_gz_path)


@pytest.fixture()
def hp35_cif_gz_file(_base_hp35_cif_gz_file):
    return _base_hp35_cif_gz_file


@pytest.fixture()
def met_enkephalin_pdb_molsys(_base_met_enkephalin_pdb_molsys):
    return _base_met_enkephalin_pdb_molsys.copy()


@pytest.fixture()
def met_enkephalin_h5msm_molsys(_base_met_enkephalin_h5msm_molsys):
    return _base_met_enkephalin_h5msm_molsys.copy()


@pytest.fixture()
def barnase_barstar_molsys(_base_barnase_barstar_molsys):
    return _base_barnase_barstar_molsys.copy()


@pytest.fixture()
def alanine_molsys(_base_alanine_molsys):
    return _base_alanine_molsys.copy()


@pytest.fixture()
def proline_molsys(_base_proline_molsys):
    return _base_proline_molsys.copy()


@pytest.fixture()
def valine_molsys(_base_valine_molsys):
    return _base_valine_molsys.copy()


@pytest.fixture()
def lysine_molsys(_base_lysine_molsys):
    return _base_lysine_molsys.copy()


@pytest.fixture()
def hp35_pdb_molsys(_base_hp35_pdb_molsys):
    return _base_hp35_pdb_molsys.copy()


@pytest.fixture()
def t4_h5msm_molsys(_base_t4_h5msm_molsys):
    return _base_t4_h5msm_molsys.copy()


@pytest.fixture()
def t4_pdb_molsys(_base_t4_pdb_molsys):
    return _base_t4_pdb_molsys.copy()


@pytest.fixture()
def t4_pdb_file():
    return systems["T4 lysozyme L99A"]["181l.pdb"]


@pytest.fixture()
def t4_pdb_text(_base_t4_pdb_text):
    return _base_t4_pdb_text


@pytest.fixture()
def t4_written_pdb_text(_base_t4_written_pdb_text):
    return _base_t4_written_pdb_text


@pytest.fixture()
def t4_pdb_handler(t4_pdb_text):
    handler = msm.convert(t4_pdb_text, to_form="molsysmt.PDBFileHandler")
    yield handler
    handler.close()


@pytest.fixture()
def md_1u19_pdb_molsys(_base_md_1u19_pdb_molsys):
    return _base_md_1u19_pdb_molsys.copy()


@pytest.fixture()
def md_1u19_pdb_file():
    return systems["nglview"]["md_1u19.pdb"]


@pytest.fixture()
def md_1u19_pdb_text(_base_md_1u19_pdb_text):
    return _base_md_1u19_pdb_text


@pytest.fixture()
def tctim_h5msm_molsys(_base_tctim_h5msm_molsys):
    return _base_tctim_h5msm_molsys.copy()


@pytest.fixture()
def tctim_bcif_molsys(_base_tctim_bcif_molsys):
    return _base_tctim_bcif_molsys.copy()


@pytest.fixture()
def popc_psf(_base_popc_psf):
    return _base_popc_psf


@pytest.fixture()
def popc_membrane_structures(_base_popc_membrane_molsys):
    return _base_popc_membrane_molsys.copy()


@pytest.fixture()
def traj_pentalanine_h5_molsys(_base_traj_pentalanine_h5_molsys):
    return _base_traj_pentalanine_h5_molsys.copy()


@pytest.fixture()
def native_interface_molsys():
    """Supply a small declared two-state source with nonidentity interface maps."""
    import numpy as np

    from molsysmt.native import MolSys, Structures

    source = MolSys(n_atoms=31, n_groups=31, n_chains=1, n_molecules=1, n_entities=1)
    source.topology.atoms["atom_type"] = ["C"] * 31
    source.topology.atoms["atom_id"] = [f"atom-{ii}" for ii in range(31)]
    source.topology.atoms["atom_name"] = [f"C{ii}" for ii in range(31)]
    source.topology.atoms["group_index"] = np.arange(31)
    source.topology.atoms["chain_index"] = [0] * 31
    source.topology.groups["group_name"] = ["LIG"] * 31
    source.topology.groups["molecule_index"] = [0] * 31
    source.topology.molecules["entity_index"] = [0]
    source.topology.chains["chain_id"] = ["A"]

    xyz = np.zeros((3, 31, 3))
    xyz[:, :, 0] = 100 + np.arange(31)
    xyz[:, [8, 2, 30, 10], 0] = [0, 3, 3.5, 1]
    xyz[0, [30, 10], 0] += 8
    xyz[1, [30, 10], 0] += 4
    # This third body must not enter the A-union-B surface environment.
    xyz[:, 0] = [0, 0.05, 0]
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(xyz, "nm"),
        time=msm.pyunitwizard.quantity([0, 1, 2], "ps"),
    )
    second = source.chemical_states.append_state()
    for state_index in [0, second]:
        source.chemical_states.add_bonds([[2, 8], [10, 30]], chemical_state=state_index)
        charges = [0] * 31
        if state_index == second:
            charges[2], charges[30] = 1, -1
        msm.set(
            source, element="atom", chemical_state=state_index, formal_charge=charges
        )
    msm.set(source, element="system", structure_chemical_state_index=[0, 0, second])
    return source


@pytest.fixture()
def openmm_pdb_ensemble(builder_openmm_topology):
    """Supply three distinguishable PDB models with a common declared box."""
    from io import StringIO

    import numpy as np
    from openmm import Vec3, unit
    from openmm.app import PDBFile

    topology = builder_openmm_topology
    topology.setPeriodicBoxVectors(
        (Vec3(4, 0, 0), Vec3(0, 5, 0), Vec3(0, 0, 6)) * unit.nanometer
    )
    positions = np.array(
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9], [1.0, 1.1, 1.2]]
    )
    text = StringIO()
    PDBFile.writeHeader(topology, text)
    for index in range(3):
        PDBFile.writeModel(
            topology,
            (positions + index) * unit.nanometer,
            text,
            modelIndex=index + 1,
            keepIds=True,
        )
    PDBFile.writeFooter(topology, text)
    text.seek(0)
    return PDBFile(text)


@pytest.fixture()
def openmm_position_snapshot():
    """Supply positions captured from a tiny Reference context, without simulation."""
    import openmm
    from openmm import unit

    system = openmm.System()
    system.addParticle(12 * unit.dalton)
    system.addParticle(12 * unit.dalton)
    integrator = openmm.VerletIntegrator(0.001 * unit.picosecond)
    context = openmm.Context(
        system, integrator, openmm.Platform.getPlatformByName("Reference")
    )
    context.setPositions([[0, 0, 0], [1, 2, 3]] * unit.nanometer)
    snapshot = context.getState(getPositions=True)
    del context
    del integrator
    return snapshot


@pytest.fixture()
def openmm_reference_context():
    """Supply a mutable two-particle Reference context without dynamics."""
    import openmm
    from openmm import unit

    system = openmm.System()
    for _ in range(2):
        system.addParticle(12 * unit.dalton)
    integrator = openmm.VerletIntegrator(0.001 * unit.picosecond)
    context = openmm.Context(
        system, integrator, openmm.Platform.getPlatformByName("Reference")
    )
    context.setPositions([[0, 0, 0], [1, 2, 3]] * unit.nanometer)
    yield context
    del context
    del integrator


@pytest.fixture()
def mdtraj_selection_ensemble(builder_pdb_molsys):
    """Supply a tiny ensemble with distinguishable positions, times and boxes."""
    import mdtraj as md
    import numpy as np

    topology = msm.convert(builder_pdb_molsys, to_form="mdtraj.Topology")
    xyz = np.arange(60, dtype=np.float32).reshape(5, 4, 3) / 10
    item = md.Trajectory(xyz, topology, time=np.array([1.0, 4.0, 9.0, 16.0, 25.0]))
    item.unitcell_vectors = np.array([np.diag([2 + i, 3 + i, 4 + i]) for i in range(5)])
    return item


@pytest.fixture()
def mdtraj_hdf5_small_files(tmp_path, mdtraj_selection_ensemble):
    """Supply minimal and complete provider-written HDF5 records."""
    import mdtraj as md
    import numpy as np

    source = mdtraj_selection_ensemble
    paths = {}
    for mode in ["minimal", "complete"]:
        path = tmp_path / (mode + ".h5")
        with md.formats.HDF5TrajectoryFile(str(path), "w") as writer:
            arguments = dict(coordinates=source.xyz)
            if mode == "complete":
                arguments.update(
                    time=np.array([1, 4, 9, 16, 25], dtype=np.float32),
                    cell_lengths=source.unitcell_lengths,
                    cell_angles=source.unitcell_angles,
                    velocities=source.xyz / 2,
                    temperature=np.array([270, 280, 290, 300, 310], dtype=np.float32),
                    kineticEnergy=np.array([1, 2, 3, 4, 5], dtype=np.float32),
                    potentialEnergy=np.array(
                        [-10, -20, -30, -40, -50], dtype=np.float32
                    ),
                )
            writer.write(**arguments)
            writer.topology = source.topology
        paths[mode] = path
    return paths
