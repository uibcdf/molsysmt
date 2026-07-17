"""Analytic scientific truth tests for rigid structural alignment."""

import numpy as np

import molsysmt as msm
from molsysmt.native import Structures


def test_least_rmsd_fit_recovers_reference_after_rigid_transform(float64_kernel_atol):
    """Recover an asymmetric reference exactly after rotation and translation."""

    reference = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.2, 1.3, 0.0], [0.1, 0.2, 0.9]]
    )
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    transformed = reference @ rotation.T + np.array([2.0, -3.0, 0.5])
    system = Structures(
        coordinates=np.stack([reference, transformed]) * msm.pyunitwizard.unit("nm")
    )

    fitted = msm.structure.least_rmsd_fit(
        system,
        selection="all",
        selection_fit="all",
        reference_structure_index=0,
        in_place=False,
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(fitted.coordinates, to_unit="nm")

    np.testing.assert_allclose(
        observed,
        np.stack([reference, reference]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_least_rmsd_align_recovers_homologous_rigid_transform(float64_kernel_atol):
    """Recover all coordinates after sequence-aware alignment of one peptide."""

    reference = msm.convert(
        msm.systems["Met-enkephalin"]["met_enkephalin.h5msm"],
        to_form="molsysmt.MolSys",
    )
    rotation = np.array(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    )
    transformed = msm.structure.rotate(reference, rotation=rotation, in_place=False)
    transformed = msm.structure.translate(
        transformed,
        translation=np.array([2.0, -3.0, 0.5]) * msm.pyunitwizard.unit("nm"),
        in_place=False,
    )

    aligned = msm.structure.least_rmsd_align(
        transformed,
        selection='atom_name=="CA"',
        reference_molecular_system=reference,
        reference_selection='atom_name=="CA"',
        in_place=False,
        use_gpu=False,
    )
    observed = msm.pyunitwizard.get_value(
        msm.get(aligned, coordinates=True), to_unit="nm"
    )
    expected = msm.pyunitwizard.get_value(
        msm.get(reference, coordinates=True), to_unit="nm"
    )

    np.testing.assert_allclose(
        observed, expected, rtol=0.0, atol=float64_kernel_atol
    )
