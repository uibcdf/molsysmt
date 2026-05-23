import pytest
import numpy as np
from molsysmt import pyunitwizard as puw
import molsysmt as msm
from molsysmt.configure import context


def test_contacts_cell_list_vacuum():
    """Verify that cell-list spatial contacts in vacuum match all-pairs references exactly."""
    np.random.seed(42)
    coords_val = np.random.rand(1, 100, 3) * 5.0  # 100 atoms in 5.0 nm box
    coords = puw.quantity(coords_val, 'nm')

    # Create dummy molecular system (using molsysmt.Structures)
    system = msm.convert(coords, to_form='molsysmt.Structures')

    threshold = '1.2 nm'

    # Baseline: all-pairs
    with context(cell_list=False):
        contacts_all_pairs = msm.structure.get_contacts(system, threshold=threshold, pbc=False)

    # Candidate: O(N) cell list
    with context(cell_list=True):
        contacts_cell_list = msm.structure.get_contacts(system, threshold=threshold, pbc=False)

    np.testing.assert_array_equal(contacts_cell_list, contacts_all_pairs)


def test_contacts_cell_list_orthogonal_pbc():
    """Verify that cell-list spatial contacts in orthogonal PBC match references exactly."""
    np.random.seed(42)
    coords_val = np.random.rand(1, 150, 3) * 4.0  # 150 atoms in 4.0 nm box
    coords = puw.quantity(coords_val, 'nm')

    # Create system with orthogonal box
    system = msm.convert(coords, to_form='molsysmt.Structures')
    box_val = np.array([[[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]]])
    msm.basic.set(system, box=puw.quantity(box_val, 'nm'))

    threshold = '1.0 nm'

    # Baseline: all-pairs with PBC
    with context(cell_list=False):
        contacts_all_pairs = msm.structure.get_contacts(system, threshold=threshold, pbc=True)

    # Candidate: O(N) cell list with PBC
    with context(cell_list=True):
        contacts_cell_list = msm.structure.get_contacts(system, threshold=threshold, pbc=True)

    np.testing.assert_array_equal(contacts_cell_list, contacts_all_pairs)


def test_contacts_cell_list_triclinic_pbc():
    """Verify that cell-list spatial contacts in triclinic PBC match references exactly."""
    np.random.seed(42)
    coords_val = np.random.rand(1, 120, 3) * 3.5
    coords = puw.quantity(coords_val, 'nm')

    system = msm.convert(coords, to_form='molsysmt.Structures')
    # Triclinic box: non-orthogonal vectors
    box_val = np.array([[[3.5, 0.0, 0.0], [1.0, 3.5, 0.0], [0.5, 1.0, 3.5]]])
    msm.basic.set(system, box=puw.quantity(box_val, 'nm'))

    threshold = '1.1 nm'

    # Baseline: all-pairs with PBC
    with context(cell_list=False):
        contacts_all_pairs = msm.structure.get_contacts(system, threshold=threshold, pbc=True)

    # Candidate: O(N) cell list with PBC
    with context(cell_list=True):
        contacts_cell_list = msm.structure.get_contacts(system, threshold=threshold, pbc=True)

    np.testing.assert_array_equal(contacts_cell_list, contacts_all_pairs)
