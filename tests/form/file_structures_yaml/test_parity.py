"""
Parity tests for file:structures_yaml form.

Oracle: builder_pdb_molsys (4 atoms, 1 structure).
Parity means that get() on a file:structures_yaml returns identical values
to get() on the source Structures for all documented structural attributes.
"""

import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture()
def yaml_file(builder_pdb_molsys, tmp_path):
    path = str(tmp_path / 'parity.yaml')
    msm.convert(builder_pdb_molsys.structures, to_form='file:structures_yaml', output_filename=path)
    return path


@pytest.fixture()
def source_structures(builder_pdb_molsys):
    return builder_pdb_molsys.structures


# ---------------------------------------------------------------------------
# Parity: file:structures_yaml get() == Structures get() on the same system
# ---------------------------------------------------------------------------

def test_parity_n_atoms(yaml_file, source_structures):
    assert msm.get(yaml_file, element='system', n_atoms=True) == source_structures.n_atoms


def test_parity_n_structures(yaml_file, source_structures):
    assert msm.get(yaml_file, element='system', n_structures=True) == source_structures.n_structures


def test_parity_coordinates(yaml_file, source_structures):
    yaml_coords = puw.get_value(
        msm.get(yaml_file, element='atom', coordinates=True), to_unit='nm'
    )
    src_coords = puw.get_value(source_structures.coordinates, to_unit='nm')
    assert np.allclose(yaml_coords, src_coords)
