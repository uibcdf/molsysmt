"""
Unit and regression test for the get_contacts module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

# Distance between atoms in space and time

def test_principal_component_analysis_from_molsysmt_MolSys_1():

    molecular_system = msm.systems['pentalanine']['traj_pentalanine.h5']
    molecular_system = msm.convert(molecular_system, to_form='molsysmt.MolSys')

    eigenvectors, eigenvalues = msm.structure.principal_component_analysis(
        molecular_system, selection='atom_name=="CA"'
    )
    eigenvalues = puw.get_value(eigenvalues, to_unit='nm**2')

    # Canonical PCA reference implementation with full covariance.
    coordinates = msm.get(
        molecular_system,
        element='atom',
        selection='atom_name=="CA"',
        coordinates=True,
    )
    coordinates = puw.get_value(coordinates).astype(np.float64)
    n_structures, n_atoms = coordinates.shape[0:2]

    flat = coordinates.transpose(0, 2, 1).reshape(n_structures, 3 * n_atoms)
    centered = flat - flat.mean(axis=0, keepdims=True)
    cov = centered.T @ centered / n_structures

    ref_eigenvalues, ref_eigenvectors = np.linalg.eigh(cov)
    ref_eigenvalues = ref_eigenvalues[::-1]
    ref_eigenvectors = ref_eigenvectors.T[::-1]

    assert np.allclose(eigenvalues, ref_eigenvalues), (
        f"Test failed with {eigenvalues} and {ref_eigenvalues}"
    )

    # Eigenvectors are defined up to a sign; compare by absolute value.
    assert np.allclose(np.abs(eigenvectors[0]), np.abs(ref_eigenvectors[0])), (
        f"Test failed with {eigenvectors[0]} and {ref_eigenvectors[0]}"
    )
