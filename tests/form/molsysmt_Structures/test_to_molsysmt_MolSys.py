"""Keep a public structural embedding independent and free of invented chemistry."""

import numpy as np

import molsysmt as msm
from molsysmt.native import Structures


def source():
    return Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(27).reshape(3, 3, 3), "angstrom"
        ),
        time=msm.pyunitwizard.quantity([0, 2, 4], "ps"),
    )


def test_public_embedding_retains_absent_domains_and_independent_geometry_handles():
    original = source()
    result = msm.convert(original, to_form="molsysmt.MolSys")
    assert result.topology is None and result.chemical_states is None
    assert result.structures is not original
    assert np.shares_memory(
        result.structures._coordinates._blocks[0], original._coordinates._blocks[0]
    )
    assert result.structures._molsys_owner_ref() is result
    msm.set(
        result,
        selection=[0],
        structure_indices=[0],
        coordinates=msm.pyunitwizard.quantity([[[9.0, 9.0, 9.0]]], "nm"),
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(original.coordinates, to_unit="angstrom"),
        np.arange(27).reshape(3, 3, 3),
    )


def test_public_embedding_selects_structure_and_atom_axes_with_units():
    result = msm.convert(
        source(), selection=[2, 0], structure_indices=[2, 0], to_form="molsysmt.MolSys"
    )
    assert result.topology is None
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="angstrom"),
        np.arange(27).reshape(3, 3, 3)[[2, 0]][:, [2, 0]],
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.time, to_unit="ps"), [4, 0]
    )


def test_public_permutation_uses_the_general_embedding_route():
    original = source()
    result = msm.permute_atoms(original, [2, 0, 1])
    assert result.topology is None and result.chemical_states is None
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="angstrom"),
        np.arange(27).reshape(3, 3, 3)[:, [2, 0, 1]],
    )


def test_conversion_profile_covers_actual_rich_structural_payload():
    from tests.basic.test_permute_atoms import rich_system

    original = rich_system().structures.copy(deep=False)
    original.temperature = msm.pyunitwizard.quantity([280.0, 290.0, 300.0], "K")
    original.potential_energy = msm.pyunitwizard.quantity([1.0, 2.0, 3.0], "kJ/mol")
    original.kinetic_energy = msm.pyunitwizard.quantity([4.0, 5.0, 6.0], "kJ/mol")
    original.structure_id = np.array(["s0", "s1", "s2"])
    for atoms, structures in [("all", "all"), ([5, 1], [2, 0])]:
        report = msm.get_conversion_report(
            original,
            to_form="molsysmt.MolSys",
            selection=atoms,
            structure_indices=structures,
        )
        assert (
            report.is_exhaustive
            and report.outcome == "equivalent"
            and not report.issues
        )
        output = msm.convert(
            original,
            to_form="molsysmt.MolSys",
            selection=atoms,
            structure_indices=structures,
        ).structures
        rows = np.arange(3) if structures == "all" else np.array(structures)
        columns = np.arange(6) if atoms == "all" else np.array(atoms)
        for field, unit in [
            ("coordinates", "nm"),
            ("velocities", "nm/ps"),
            ("b_factor", "nm**2"),
        ]:
            expected = msm.pyunitwizard.get_value(
                getattr(original, field), to_unit=unit
            )[rows][:, columns]
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(getattr(output, field), to_unit=unit),
                expected,
            )
        for field, unit in [
            ("time", "ps"),
            ("box", "nm"),
            ("temperature", "K"),
            ("potential_energy", "kJ/mol"),
            ("kinetic_energy", "kJ/mol"),
        ]:
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(getattr(output, field), to_unit=unit),
                msm.pyunitwizard.get_value(getattr(original, field), to_unit=unit)[
                    rows
                ],
            )
        np.testing.assert_array_equal(
            output.occupancy, original.occupancy[rows][:, columns]
        )
        np.testing.assert_array_equal(output.structure_id, original.structure_id[rows])
        np.testing.assert_array_equal(
            output.bioassembly["1"]["chain_indices"], [[1, 0]]
        )
        expected_keys = [[4], [], [1]] if atoms == "all" else [[1], []]
        assert [list(sites) for sites in output.alternate_location] == expected_keys
