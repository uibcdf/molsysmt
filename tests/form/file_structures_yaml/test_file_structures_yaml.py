import molsysmt as msm


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
