"""
Unit and regression test for the iterator module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt import systems


def test_iterator_1():
    psf = systems["POPC membrane"]["popc_membrane.psf"]
    dcd = systems["POPC membrane"]["popc_membrane.dcd"]
    atoms_P = msm.select(psf, selection='atom_name == "P"')
    iterator = msm.Iterator(dcd, selection=atoms_P, coordinates=True)
    coordinates = []
    for aux_coordinates in iterator:
        coordinates.append(aux_coordinates[0])
    coordinates = puw.utils.sequences.concatenate(
        coordinates, value_type="numpy.ndarray"
    )
    assert coordinates.shape == (5, 294, 3)


def test_iterator_2():
    psf = systems["POPC membrane"]["popc_membrane.psf"]
    dcd = systems["POPC membrane"]["popc_membrane.dcd"]
    iterator = msm.Iterator([psf, dcd], selection='atom_name == "P"', coordinates=True)
    coordinates = []
    for aux_coordinates in iterator:
        coordinates.append(aux_coordinates[0])
    coordinates = puw.utils.sequences.concatenate(
        coordinates, value_type="numpy.ndarray"
    )
    assert coordinates.shape == (5, 294, 3)


def test_iterator_does_not_hide_backend_failures():
    structures = msm.convert(
        systems["pentalanine"]["traj_pentalanine.h5"],
        to_form="molsysmt.Structures",
        structure_indices=[0],
    )
    iterator = msm.Iterator(structures, coordinates=True)

    class BrokenIterator:
        def __next__(self):
            raise RuntimeError("backend failure")

    iterator._iterators = [BrokenIterator()]

    with pytest.raises(RuntimeError, match="backend failure"):
        next(iterator)


def test_iterator_yields_molecular_systems_for_a_coordinate_only_form():
    # Without explicit attributes the iterator yields a molecular system per chunk. A DCD
    # provides no 'structure_id' and no 'time', which used to leave the internal iterator
    # unassigned and raise UnboundLocalError before the first item.
    dcd = systems["POPC membrane"]["popc_membrane.dcd"]
    iterator = msm.Iterator(dcd, chunk=2)

    assert iterator.arguments == ["coordinates", "box"]

    sizes = []
    first_atom = []
    for molecular_system in iterator:
        sizes.append(msm.get(molecular_system, n_structures=True))
        coordinates = msm.get(molecular_system, element="atom", coordinates=True)
        first_atom.append(puw.get_value(coordinates[0, 0]).copy())

    # Five structures in chunks of two, the last one partial.
    assert sizes == [2, 2, 1]
    # The reusable system is genuinely updated: consecutive chunks are not the same data.
    assert not np.allclose(first_atom[0], first_atom[1])


def test_iterator_yields_molecular_systems_for_an_h5msm_trajectory():
    # 'structures/id' is stored as an empty dataset in this file, so reading it indexed an
    # empty dimension. The 'time' branch of the same reader already treated that as absent.
    h5msm = systems["pentalanine"]["traj_pentalanine.h5msm"]
    iterator = msm.Iterator(h5msm, chunk=1000)

    sizes = [
        msm.get(molecular_system, n_structures=True) for molecular_system in iterator
    ]
    assert sizes == [1000, 1000, 1000, 1000, 1000]


def test_iterator_preserves_structure_order_and_units():
    # Chunking must not reorder structures nor strip units: the chunks concatenated back
    # together have to reproduce the whole trajectory exactly.
    dcd = systems["POPC membrane"]["popc_membrane.dcd"]
    whole = msm.get(dcd, element="atom", coordinates=True)

    # The last chunk is partial, so the pieces are stacked by value after checking units.
    chunks = list(msm.Iterator(dcd, chunk=2, coordinates=True))
    assert [len(chunk) for chunk in chunks] == [2, 2, 1]
    assert all(puw.get_unit(chunk) == puw.get_unit(whole) for chunk in chunks)

    rebuilt = np.concatenate([puw.get_value(chunk) for chunk in chunks], axis=0)
    assert np.allclose(rebuilt, puw.get_value(whole))


def test_iterator_yielding_molecular_systems_honors_the_selection():
    dcd = systems["POPC membrane"]["popc_membrane.dcd"]
    iterator = msm.Iterator(dcd, selection="atom_index < 100", chunk=2)
    for molecular_system in iterator:
        assert msm.get(molecular_system, n_atoms=True) == 100


@pytest.mark.parametrize(
    "arguments",
    [
        {"coordinates": True, "time": True},
        {"time": True, "coordinates": True},
    ],
)
def test_iterator_rejects_an_unavailable_attribute_in_any_keyword_order(arguments):
    # A DCD has no 'time'. Depending on the keyword order this used to raise
    # UnboundLocalError or, worse, append the previous iterator twice and yield no item at
    # all without reporting anything.
    dcd = systems["POPC membrane"]["popc_membrane.dcd"]
    with pytest.raises(msm.NotWithThisFormError, match="time"):
        msm.Iterator(dcd, chunk=2, **arguments)


@pytest.mark.parametrize("reversed_order", [False, True])
def test_iterator_yields_molecular_systems_for_a_topology_plus_trajectory(
    reversed_order,
):
    # The H5MSM file holds a single reference structure and the DCD holds twenty. Only the
    # DCD spans the structure axis, so 'structure_id' and 'time' are not iterated and the
    # result must not depend on the order the items were listed in.
    h5msm = systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.h5msm"]
    dcd = systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.dcd"]
    composite = [dcd, h5msm] if reversed_order else [h5msm, dcd]

    iterator = msm.Iterator(composite, chunk=10)
    assert iterator.arguments == ["coordinates", "box"]

    sizes = [
        msm.get(molecular_system, n_structures=True) for molecular_system in iterator
    ]
    assert sizes == [10, 10]


def test_iterator_accepts_structural_attributes_sharing_one_structure_axis():
    composite = [
        systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.h5msm"],
        systems["chicken villin HP35"]["traj_chicken_villin_HP35_solvated.dcd"],
    ]
    iterator = msm.Iterator(composite, chunk=10, coordinates=True, box=True)
    sizes = [len(coordinates) for coordinates, _ in iterator]
    assert sizes == [10, 10]


# def test_iterator_3():
#    iterator = msm.Iterator(molsys, selection='atom_name == "P"', coordinates=True)
#    coordinates = []
#    for aux_coordinates in iterator:
#        coordinates.append(aux_coordinates[0])
#    coordinates = puw.utils.sequences.concatenate(coordinates, value_type='numpy.ndarray')
#    assert coordinates.shape == (5, 294, 3)


@pytest.mark.parametrize("output_form", ["molsysmt.MolSys", "molsysmt.Structures"])
@pytest.mark.parametrize("unit,scale", [("nm", 1), ("pm", 1000)])
def test_native_system_chunks_publish_the_complete_selected_axis(
    output_form, unit, scale
):
    from molsysmt.native import Structures

    values = np.arange(18, dtype=float).reshape(3, 2, 3)
    source = Structures(
        coordinates=puw.quantity(values * scale, unit),
        time=puw.quantity([2, 5, 11], "ps"),
        box=puw.quantity(np.repeat(np.eye(3)[None] * 4 * scale, 3, axis=0), unit),
        structure_id=["C", "A", "C"],
    )
    source_xyz, source_box = source._coordinates, source._box
    results, blocks = [], []
    for block in msm.Iterator(
        source, structure_indices=[2, 0, 2], chunk=2, output_form=output_form
    ):
        blocks.append(block)
        domain = block.structures if output_form == "molsysmt.MolSys" else block
        assert domain.n_structures in (1, 2)
        results.append(
            (
                puw.get_value(domain.coordinates, to_unit="nm").copy(),
                puw.get_value(domain.time, to_unit="ps").copy(),
                domain.structure_id.copy(),
                puw.get_value(domain.box, to_unit="nm").copy(),
            )
        )
    assert blocks[0] is not blocks[1]
    assert [len(result[0]) for result in results] == [2, 1]
    np.testing.assert_allclose(
        np.concatenate([r[0] for r in results]), values[[2, 0, 2]]
    )
    np.testing.assert_array_equal(np.concatenate([r[1] for r in results]), [11, 2, 11])
    np.testing.assert_array_equal(
        np.concatenate([r[2] for r in results]), ["C", "C", "C"]
    )
    np.testing.assert_allclose(
        np.concatenate([r[3] for r in results]),
        np.repeat(np.eye(3)[None] * 4, 3, axis=0),
    )
    assert source._coordinates is source_xyz and source._box is source_box
    assert source.n_structures == 3


def test_native_chunks_remap_state_links_coverage_and_other_observables():
    from molsysmt.native import MolSys, Structures

    source = MolSys(n_atoms=2)
    source.structures = Structures(
        coordinates=puw.quantity(np.arange(18).reshape(3, 2, 3), "nm"),
        occupancy=np.arange(6).reshape(3, 2) / 10,
        structure_id=["same", "middle", "same"],
    )
    source.chemical_states.append_state()
    msm.set(source, structure_chemical_state_index=[0, 1, 0])
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=2,
        n_structures=3,
        evaluated_structure_indices=[0, 2],
        method="synthetic.iterator-axis-correspondence",
    )
    source.interactions = {"empty": analysis}
    first, last = list(msm.Iterator(source, structure_indices=[2, 1, 0], chunk=2))
    assert first is not last and first.structures is not source.structures
    assert msm.get(first, structure_chemical_state_index=True) == [0, 1]
    assert msm.get(last, structure_chemical_state_index=True) == [0]
    assert first.interactions["empty"].n_structures == 2
    assert last.interactions["empty"].n_structures == 1
    np.testing.assert_array_equal(
        first.interactions["empty"].evaluated_structure_indices, [0]
    )
    np.testing.assert_array_equal(
        last.interactions["empty"].evaluated_structure_indices, [0]
    )
    np.testing.assert_array_equal(
        first.structures.occupancy, source.structures.occupancy[[2, 1]]
    )
    np.testing.assert_array_equal(
        last.structures.occupancy, source.structures.occupancy[[0]]
    )
    assert (
        source.interactions["empty"] is analysis and source.structures.n_structures == 3
    )
    assert msm.get(source, structure_chemical_state_index=True) == [0, 1, 0]
