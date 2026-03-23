import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np


def test_structures_yaml_roundtrip(tmp_path):
    structures = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.Structures')
    output = tmp_path / 'structures.yaml'

    msm.convert(structures, to_form='file:structures_yaml', output_filename=str(output))

    assert output.exists()
    assert msm.get_form(str(output)) == 'file:structures_yaml'

    recovered = msm.convert(str(output), to_form='molsysmt.Structures')

    assert recovered.n_structures == structures.n_structures
    assert recovered.n_atoms == structures.n_atoms
    assert msm.get(str(output), element='system', n_structures=True) == 1
    assert msm.get(str(output), element='atom', b_factor=True) is not None


def test_structures_yaml_preserves_declared_builder_structure(builder_structures, tmp_path):
    output = tmp_path / 'builder_structures.yaml'

    msm.convert(builder_structures, to_form='file:structures_yaml', output_filename=str(output))

    recovered = msm.convert(str(output), to_form='molsysmt.Structures')

    assert recovered.n_structures == 1
    assert recovered.n_atoms == 4
    assert np.allclose(
        puw.get_value(recovered.coordinates, to_unit='nm'),
        puw.get_value(builder_structures.coordinates, to_unit='nm'),
    )
    assert np.allclose(
        puw.get_value(recovered.box, to_unit='nm'),
        puw.get_value(builder_structures.box, to_unit='nm'),
    )
    assert puw.get_value(recovered.time, to_unit='ps').tolist() == [0.0]
    assert list(recovered.structure_id) == [0]
