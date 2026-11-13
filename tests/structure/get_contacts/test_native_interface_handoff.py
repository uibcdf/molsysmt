"""Receive Cartesian contacts and declared nonidentity source maps for #734."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
@pytest.mark.parametrize("cell_list", [False, True])
def test_interface_cross_pairs_cutoff_distances_and_completed_zero(
    native_interface_molsys, length, time, cell_list
):
    source = native_interface_molsys
    before = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    with puw.context(standard_units=[length, time, "radians"]):
        policy = puw.configure.get_standard_units()
        arguments = dict(
            selection=[8, 2],
            selection_2=[30, 10],
            structure_indices=[2],
            pairs=False,
            pbc=False,
            use_gpu=False,
            parallel=False,
            num_threads=1,
        )
        contacts = msm.structure.get_contacts(
            source, threshold="1000 pm", cell_list=cell_list, **arguments
        )
        np.testing.assert_array_equal(contacts, [[[False, True], [True, False]]])
        distances = msm.structure.get_distances(source, **arguments)
        assert puw.check(distances, dimensionality={"[L]": 1})
        np.testing.assert_allclose(
            puw.get_value(distances, to_unit="nm"),
            [[[3.5, 1.0], [0.5, 2.0]]],
            rtol=0,
            atol=1e-12,
        )
        pairs = msm.structure.get_contacts(
            source,
            threshold="1 nm",
            cell_list=cell_list,
            output_type="pairs",
            output_indices="atom",
            **arguments,
        )
        assert pairs == [[[8, 10], [2, 30]]]
        predecessor = msm.structure.get_contacts(
            source,
            threshold=puw.quantity(np.nextafter(1.0, -np.inf), "nm"),
            cell_list=cell_list,
            output_type="pairs",
            output_indices="atom",
            **arguments,
        )
        assert predecessor == [[[2, 30]]]
        corresponding = msm.structure.get_contacts(
            source,
            selection=[8, 2],
            selection_2=[30, 10],
            structure_indices=[2],
            pairs=True,
            threshold="1 nm",
            pbc=False,
            use_gpu=False,
            cell_list=cell_list,
            parallel=False,
            num_threads=1,
        )
        np.testing.assert_array_equal(corresponding, [[False, False]])
        empty = msm.structure.get_contacts(
            source,
            **{**arguments, "structure_indices": [0]},
            threshold="1 nm",
            cell_list=cell_list,
            output_type="pairs",
            output_indices="atom",
        )
        assert empty == [[]]
        assert puw.configure.get_standard_units() == policy
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), before
    )


def test_extraction_permutation_and_footprints_keep_source_structure_and_state(
    native_interface_molsys,
):
    source = native_interface_molsys
    selected = [2, 8, 10, 30]
    reduced = msm.extract(source, selection=[8, 2, 30, 10], structure_indices=[2])
    assert msm.get(reduced, element="atom", atom_id=True) == [
        f"atom-{ii}" for ii in selected
    ]
    permuted = msm.permute_atoms(reduced, [1, 0, 3, 2], return_report=True)
    context = permuted["molecular_system"]
    inverse = np.full(31, -1, dtype=np.int64)
    inverse[selected] = np.arange(4)
    report = msm.compose_atom_maps(
        [
            dict(
                schema="molsysmt.atom_map@1",
                n_source_atoms=31,
                n_output_atoms=4,
                output_to_source_atom_indices=selected,
                source_to_output_atom_indices=inverse,
            ),
            permuted["report"],
        ]
    )
    np.testing.assert_array_equal(
        report["output_to_source_atom_indices"], [8, 2, 30, 10]
    )
    assert msm.get(context, structure_chemical_state_index=True) == [1]
    assert msm.get(
        context,
        element="atom",
        chemical_state="structure",
        structure_indices=[0],
        formal_charge=True,
    ) == [0, 1, -1, 0]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(context, element="atom", coordinates=True), to_unit="nm"),
        puw.get_value(source.structures.coordinates, to_unit="nm")[[2]][
            :, [8, 2, 30, 10]
        ],
    )
    pairs = np.asarray(
        msm.structure.get_contacts(
            context,
            selection=[0, 1],
            selection_2=[2, 3],
            structure_indices=[0],
            threshold="1 nm",
            pbc=False,
            pairs=False,
            output_type="pairs",
            output_indices="atom",
            use_gpu=False,
            cell_list=False,
            parallel=False,
            num_threads=1,
        )[0]
    )
    original_pairs = report["output_to_source_atom_indices"][pairs]
    np.testing.assert_array_equal(original_pairs, [[8, 10], [2, 30]])
    first = np.unique(original_pairs[:, 0])
    second = np.unique(original_pairs[:, 1])
    np.testing.assert_array_equal(first, [2, 8])
    np.testing.assert_array_equal(second, [10, 30])
    np.testing.assert_array_equal(
        report["source_to_output_atom_indices"][first], [1, 0]
    )
    np.testing.assert_array_equal(
        report["source_to_output_atom_indices"][second], [3, 2]
    )
