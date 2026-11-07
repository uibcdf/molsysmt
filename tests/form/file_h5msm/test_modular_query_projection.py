"""Check actual structural dataset windows behind modular public queries."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures

puw = msm.pyunitwizard
FRAMES = [16, 1, 16]
ATOMS = [9, 2, 9]


@pytest.fixture(params=["structures-only", "full-system"])
def source(request, tmp_path):
    coordinates = np.arange(17 * 11 * 3, dtype=float).reshape(17, 11, 3) / 1000
    structures = Structures(
        coordinates=puw.quantity(coordinates, "nm"),
        time=puw.quantity(np.arange(17, dtype=float), "ps"),
        box=puw.quantity(np.tile(np.eye(3) * 3, (17, 1, 1)), "nm"),
        structure_id=[str(100 + index) for index in range(17)],
    )
    filename = tmp_path / "projection.h5msm"
    if request.param == "structures-only":
        native = structures
        msm.h5msm.write_layers(filename, structures=structures)
    else:
        builder = msm.MolSysBuilder()
        atoms = [builder.add_atom(atom_name=f"C{i}", atom_type="C") for i in range(11)]
        builder.add_group(atoms, group_name="LIG")
        builder.set_coordinates(puw.quantity(coordinates, "nm"))
        native = builder.build()
        native.structures = structures
        msm.h5msm.write(native, filename)
    return str(filename), native


def _watch(monkeypatch, allowed, frames=(), atoms=()):
    """Observe all ordinary HDF5 payload routes, including implicit full arrays."""
    getitem = h5py.Dataset.__getitem__
    direct = h5py.Dataset.read_direct
    asarray = h5py.Dataset.__array__
    calls = []

    def check(dataset, key):
        assert not dataset.name.startswith("/interactions/"), (
            f"Unrequested interaction observation read: {dataset.name} {key!r}"
        )
        if not dataset.name.startswith("/structures/"):
            return
        name = dataset.name.rsplit("/", 1)[-1]
        assert name in allowed, (
            f"Unrequested structural payload read: {dataset.name} {key!r}"
        )
        key = key if isinstance(key, tuple) else (key,)
        rows = np.arange(dataset.shape[0])[key[0]]
        assert set(np.asarray(rows).reshape(-1)) <= set(frames), (
            f"Unrequested structure rows read from {dataset.name}: {key!r}"
        )
        if name == "coordinates":
            columns = np.arange(dataset.shape[1])[
                key[1] if len(key) > 1 else slice(None)
            ]
            assert set(np.asarray(columns).reshape(-1)) <= set(atoms), (
                f"Unrequested atom rows read from {dataset.name}: {key!r}"
            )
        calls.append((name, key))

    def read(dataset, key):
        check(dataset, key)
        return getitem(dataset, key)

    def read_direct(dataset, destination, source_sel=None, dest_sel=None):
        check(dataset, slice(None) if source_sel is None else source_sel)
        return direct(dataset, destination, source_sel=source_sel, dest_sel=dest_sel)

    def array(dataset, *args, **kwargs):
        check(dataset, slice(None))
        return asarray(dataset, *args, **kwargs)

    monkeypatch.setattr(h5py.Dataset, "__getitem__", read)
    monkeypatch.setattr(h5py.Dataset, "read_direct", read_direct)
    monkeypatch.setattr(h5py.Dataset, "__array__", array)
    return calls


@pytest.mark.parametrize(
    "query", ["n_atoms", "n_structures", "structure_index", "select", "has_coordinates"]
)
def test_axis_and_numeric_selection_queries_read_no_structural_payload(
    source, monkeypatch, query
):
    filename, native = source
    calls = _watch(monkeypatch, allowed=set())
    if query == "select":
        actual = msm.select(filename, selection=ATOMS, structure_indices=FRAMES)
        expected = ATOMS
    elif query == "has_coordinates":
        actual = msm.has_attribute(filename, attribute="coordinates")
        expected = True
    else:
        kwargs = {query: True}
        if query == "structure_index":
            kwargs["structure_indices"] = FRAMES
        actual = msm.get(filename, **kwargs)
        expected = msm.get(native, **kwargs)
    np.testing.assert_equal(actual, expected)
    assert not calls


@pytest.mark.parametrize("attribute", ["coordinates", "box", "time"])
def test_structural_query_reads_only_the_requested_field_and_windows(
    source, monkeypatch, attribute
):
    filename, native = source
    kwargs = {attribute: True, "structure_indices": FRAMES}
    if attribute == "coordinates":
        kwargs.update(element="atom", selection=ATOMS)
    expected = msm.get(native, **kwargs)
    calls = _watch(monkeypatch, allowed={attribute}, frames=FRAMES, atoms=ATOMS)
    actual = msm.get(filename, **kwargs)
    assert calls
    np.testing.assert_array_equal(
        puw.get_value(actual, to_unit=puw.get_unit(expected)), puw.get_value(expected)
    )


def test_empty_coordinate_selection_reads_no_structure_rows(source, monkeypatch):
    filename, native = source
    expected = msm.get(
        native, element="atom", selection=ATOMS, structure_indices=[], coordinates=True
    )
    calls = _watch(monkeypatch, allowed=set())
    actual = msm.get(
        filename,
        element="atom",
        selection=ATOMS,
        structure_indices=[],
        coordinates=True,
    )
    if expected is None:
        assert actual is None
    else:
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    assert not calls


@pytest.fixture
def chemical_source(tmp_path):
    system = MolSys(n_atoms=11)
    system.topology.atoms["atom_name"] = [f"C{i}" for i in range(11)]
    system.topology.atoms["atom_type"] = ["C"] * 11
    system.chemical_states.append_state()
    for state in (0, 1):
        msm.set(
            system, element="atom", chemical_state=state, formal_charge=[state] * 11
        )
        system.chemical_states.add_bonds([[state, state + 1]], chemical_state=state)
    system.structures = Structures(
        coordinates=puw.quantity(
            np.arange(17 * 11 * 3).reshape(17, 11, 3) / 1000, "nm"
        ),
        box=puw.quantity(np.tile(np.eye(3) * 3, (17, 1, 1)), "nm"),
        time=puw.quantity(np.arange(17), "ps"),
        velocities=puw.quantity(np.ones((17, 11, 3)), "nm/ps"),
        b_factor=puw.quantity(np.ones((17, 11)) / 100, "nm**2"),
        occupancy=np.ones((17, 11)),
        temperature=puw.quantity(np.arange(17) + 300, "K"),
        potential_energy=puw.quantity(np.arange(17), "kJ/mol"),
        kinetic_energy=puw.quantity(np.arange(17) + 2, "kJ/mol"),
    )
    system._set_structure_chemical_state_indices([index % 2 for index in range(17)])
    system.interactions = {
        "unused": msm.Interactions.from_records(
            [
                {
                    "structure_index": 16,
                    "interaction_type": "test",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [1]},
                    ],
                }
            ],
            n_atoms=11,
            n_structures=17,
            method="unrequested-test",
            evaluated_structure_indices=[0, 16],
        )
    }
    filename = str(tmp_path / "chemical.h5msm")
    msm.h5msm.write(system, filename)
    return filename, system


@pytest.mark.parametrize("state", ["reference", None, 0, 1, "structure"])
def test_static_and_state_queries_do_not_read_structural_payload(
    chemical_source, monkeypatch, state
):
    filename, native = chemical_source
    kwargs = dict(
        element="atom",
        selection=ATOMS,
        structure_indices=[16, 0, 16],
        chemical_state=state,
        atom_name=True,
        formal_charge=True,
        n_bonds=True,
        output_type="dictionary",
    )
    expected = msm.get(native, **kwargs)
    calls = _watch(monkeypatch, allowed=set())
    actual = msm.get(filename, **kwargs)
    np.testing.assert_equal(actual, expected)
    assert not calls


@pytest.mark.parametrize("state", [0, 1, "structure"])
def test_chemical_predicate_uses_scoped_state_without_structural_reads(
    chemical_source, monkeypatch, state
):
    filename, native = chemical_source
    kwargs = dict(
        selection="formal_charge==1", chemical_state=state, structure_indices=[0, 16]
    )
    expected = msm.select(native, **kwargs)
    calls = _watch(monkeypatch, allowed=set())
    assert msm.select(filename, **kwargs) == expected
    assert not calls
    assert msm.get(filename, element="atom", formal_charge=True) == [0] * 11


@pytest.mark.parametrize(
    "attribute",
    [
        "velocities",
        "b_factor",
        "occupancy",
        "temperature",
        "potential_energy",
        "kinetic_energy",
        "total_energy",
        "box_lengths",
        "box_angles",
        "box_volume",
        "structure_id",
    ],
)
def test_additional_stored_and_derived_fields_are_projected(
    chemical_source, monkeypatch, attribute
):
    filename, native = chemical_source
    kwargs = dict(structure_indices=FRAMES, **{attribute: True})
    if attribute in {"velocities", "b_factor", "occupancy"}:
        kwargs.update(element="atom", selection=ATOMS)
    expected = msm.get(native, **kwargs)
    fields = (
        {"potential_energy", "kinetic_energy"}
        if attribute == "total_energy"
        else {"box"}
        if attribute.startswith("box_")
        else {attribute}
    )
    calls = _watch(monkeypatch, allowed=fields, frames=FRAMES, atoms=ATOMS)
    actual = msm.get(filename, **kwargs)
    if puw.is_quantity(expected):
        np.testing.assert_array_equal(
            puw.get_value(actual, to_unit=puw.get_unit(expected)),
            puw.get_value(expected),
        )
    else:
        np.testing.assert_equal(actual, expected)
    assert bool(calls) == (expected is not None)


@pytest.mark.parametrize("state", ["reference", 1, "structure"])
def test_mixed_query_projects_geometry_and_preserves_state(
    chemical_source, monkeypatch, state
):
    filename, native = chemical_source
    kwargs = dict(
        element="atom",
        selection=ATOMS,
        structure_indices=[16, 0, 16],
        chemical_state=state,
        coordinates=True,
        atom_name=True,
        formal_charge=True,
        output_type="dictionary",
    )
    expected = msm.get(native, **kwargs)
    calls = _watch(monkeypatch, allowed={"coordinates"}, frames=[0, 16], atoms=ATOMS)
    actual = msm.get(filename, **kwargs)
    for attribute in expected:
        if attribute == "coordinates":
            np.testing.assert_array_equal(
                puw.get_value(actual[attribute]), puw.get_value(expected[attribute])
            )
        else:
            np.testing.assert_equal(actual[attribute], expected[attribute])
    assert calls


def test_combined_native_topology_and_file_geometry_preserve_axis(
    chemical_source, monkeypatch
):
    filename, native = chemical_source
    kwargs = dict(
        element="atom",
        selection=ATOMS,
        structure_indices=FRAMES,
        coordinates=True,
        atom_name=True,
        output_type="dictionary",
    )
    expected = msm.get(native, **kwargs)
    calls = _watch(monkeypatch, allowed={"coordinates"}, frames=FRAMES, atoms=ATOMS)
    actual = msm.get([native.topology, filename], **kwargs)
    assert actual["atom_name"] == expected["atom_name"]
    np.testing.assert_array_equal(
        puw.get_value(actual["coordinates"]), puw.get_value(expected["coordinates"])
    )
    assert calls


@pytest.mark.parametrize(
    "state, structures",
    [("structure", [0, 1]), ("structure", []), (8, [0])],
)
def test_invalid_or_ambiguous_state_rejected_without_structural_reads(
    chemical_source, monkeypatch, state, structures
):
    filename, native = chemical_source
    kwargs = dict(
        element="atom",
        formal_charge=True,
        chemical_state=state,
        structure_indices=structures,
    )
    from molsysmt._private.smonitor import StructuralInconsistencyError

    with pytest.raises(StructuralInconsistencyError) as baseline:
        msm.get(native, **kwargs)
    calls = _watch(monkeypatch, allowed=set())
    with pytest.raises(type(baseline.value)):
        msm.get(filename, **kwargs)
    assert not calls


@pytest.mark.parametrize(
    "argument, indices",
    [
        ("selection", [-1]),
        ("selection", [11]),
        ("selection", [True, 1]),
        ("structure_indices", [17]),
        ("structure_indices", [-1]),
        ("structure_indices", [1.5]),
    ],
)
def test_invalid_projection_fails_before_payload(
    source, monkeypatch, argument, indices
):
    filename, _ = source
    from molsysmt._private.smonitor import ArgumentError

    calls = _watch(monkeypatch, allowed=set())
    with pytest.raises(ArgumentError):
        msm.get(filename, element="atom", coordinates=True, **{argument: indices})
    assert not calls


@pytest.mark.parametrize("argument", ["selection", "mask"])
def test_spatial_selection_reads_only_requested_structures(
    source, monkeypatch, argument
):
    filename, native = source
    kwargs = dict(
        element="atom",
        structure_indices=[16],
        atom_index=True,
        **{argument: "atom_index != 0 within 0.03 nm of atom_index == 0"},
    )
    expected = msm.get(native, **kwargs)
    calls = _watch(monkeypatch, allowed={"coordinates"}, frames=[16], atoms=range(11))
    assert msm.get(filename, **kwargs) == expected
    assert calls


@pytest.mark.parametrize("order", ["file-last", "native-last"])
def test_composite_predicate_retains_provider_precedence_without_geometry(
    chemical_source, monkeypatch, order
):
    filename, native = chemical_source
    topology = native.topology.copy()
    topology.atoms["atom_name"] = [f"N{i}" for i in range(11)]
    inputs = [topology, filename] if order == "file-last" else [filename, topology]
    calls = _watch(monkeypatch, allowed=set())
    assert msm.select(inputs, selection='atom_name=="C2"') == (
        [2] if order == "file-last" else []
    )
    assert not calls


@pytest.mark.parametrize("unit", ["pm", "angstrom"])
def test_requested_output_units_survive_projection(source, monkeypatch, unit):
    filename, native = source
    calls = _watch(monkeypatch, allowed={"coordinates"}, frames=FRAMES, atoms=ATOMS)
    with puw.context(standard_units=[unit, "fs"]):
        actual = msm.get(
            filename,
            element="atom",
            selection=ATOMS,
            structure_indices=FRAMES,
            coordinates=True,
        )
        expected = msm.get(
            native,
            element="atom",
            selection=ATOMS,
            structure_indices=FRAMES,
            coordinates=True,
        )
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    assert calls


@pytest.mark.parametrize("damage", ["schema", "unit", "shape", "dtype", "unlinked"])
def test_malformed_queried_schema_fails_before_structural_payload(
    chemical_source, monkeypatch, damage
):
    filename, _ = chemical_source
    with h5py.File(filename, "r+") as file:
        if damage == "schema":
            file["structures"].attrs["schema_version"] = 99
        elif damage == "unit":
            file["structures/coordinates"].attrs["unit"] = "angstrom"
        elif damage in {"shape", "dtype"}:
            del file["structures/coordinates"]
            dataset = file["structures"].create_dataset(
                "coordinates",
                shape=(17, 10 if damage == "shape" else 11, 3),
                dtype="S1" if damage == "dtype" else "f8",
            )
            dataset.attrs["unit"] = "nm"
        else:
            del file["associations"]
    calls = _watch(monkeypatch, allowed=set())
    with pytest.raises(ValueError):
        msm.get(
            filename,
            element="atom",
            selection=ATOMS,
            structure_indices=FRAMES,
            coordinates=True,
        )
    assert not calls


def test_bulk_query_reuses_decoded_static_domains(chemical_source, monkeypatch):
    from molsysmt.form import _h5msm05_topology, _h5msm_chemical_states

    filename, _ = chemical_source
    counts = {"topology": 0, "chemical_states": 0}

    def observe(module, name, key):
        original = getattr(module, name)

        def read(*args, **kwargs):
            counts[key] += 1
            return original(*args, **kwargs)

        monkeypatch.setattr(module, name, read)

    observe(_h5msm05_topology, "read_independent_topology", "topology")
    observe(
        _h5msm_chemical_states, "read_independent_chemical_states", "chemical_states"
    )
    _watch(monkeypatch, allowed=set())
    actual = msm.get(
        filename,
        element="atom",
        selection=ATOMS,
        atom_name=True,
        atom_type=True,
        formal_charge=True,
        component_index=True,
        output_type="dictionary",
    )
    assert actual["atom_name"] == ["C9", "C2", "C9"]
    assert counts == {"topology": 1, "chemical_states": 1}


@pytest.mark.parametrize("fail", [False, True])
def test_query_closes_handles_on_success_and_failure_and_preserves_file(
    source, monkeypatch, fail
):
    import hashlib
    from pathlib import Path

    filename, _ = source
    before = hashlib.sha256(Path(filename).read_bytes()).hexdigest()
    opened = []
    original = h5py.File.__init__

    def opening(file, *args, **kwargs):
        original(file, *args, **kwargs)
        opened.append(file)

    monkeypatch.setattr(h5py.File, "__init__", opening)
    if fail:
        from molsysmt._private.smonitor import ArgumentError

        with pytest.raises(ArgumentError):
            msm.get(filename, element="atom", selection=[11], coordinates=True)
    else:
        msm.get(
            filename,
            element="atom",
            selection=ATOMS,
            structure_indices=FRAMES,
            coordinates=True,
        )
    assert opened and all(not file.id.valid for file in opened)
    assert hashlib.sha256(Path(filename).read_bytes()).hexdigest() == before


def test_later_queries_observe_external_changes_without_stale_cache(source):
    filename, _ = source

    def query():
        return puw.get_value(
            msm.get(
                filename,
                element="atom",
                selection=[9],
                structure_indices=[16],
                coordinates=True,
            ),
            to_unit="nm",
        )

    first = query()
    with h5py.File(filename, "r+") as file:
        file["structures/coordinates"][16, 9] = [10, 20, 30]
    second = query()
    assert not np.array_equal(first, second)
    np.testing.assert_array_equal(second, [[[10, 20, 30]]])


def test_axis_queries_do_not_read_structure_to_state_map(chemical_source, monkeypatch):
    filename, _ = chemical_source
    original = h5py.Dataset.__getitem__

    def read(dataset, key):
        assert not dataset.name.startswith("/associations/"), (
            "Axis counts need no state map payload"
        )
        return original(dataset, key)

    monkeypatch.setattr(h5py.Dataset, "__getitem__", read)
    _watch(monkeypatch, allowed=set())
    assert msm.get(filename, n_atoms=True, n_structures=True) == [11, 17]


def test_interactions_only_counts_need_no_occurrence_arrays(tmp_path, monkeypatch):
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=11,
        n_structures=17,
        method="axis-test",
        evaluated_structure_indices=[0, 16],
    )
    filename = str(tmp_path / "interactions.h5msm")
    msm.h5msm.write_layers(filename, interactions={"test": analysis})

    def read(dataset, key):
        pytest.fail(f"Metadata-only query read {dataset.name} {key}")

    monkeypatch.setattr(h5py.Dataset, "__getitem__", read)
    assert msm.get(filename, n_atoms=True, n_structures=True) == [11, 17]
