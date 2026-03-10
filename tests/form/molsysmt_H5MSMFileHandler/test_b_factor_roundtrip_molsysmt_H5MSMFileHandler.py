import numpy as np
import molsysmt as msm


def test_molsysmt_H5MSMFileHandler_preserves_b_factor_roundtrip(tmp_path, tctim_bcif_molsys):

    output_path = tmp_path / 'tctim_bfactor_handler.h5msm'

    msm.convert(tctim_bcif_molsys, to_form='file:h5msm', output_filename=str(output_path))

    handler = msm.convert(str(output_path), to_form='molsysmt.H5MSMFileHandler')
    structures = msm.convert(handler, to_form='molsysmt.Structures')

    assert structures.b_factor is not None
    assert msm.pyunitwizard.check(structures.b_factor, unit='nm^2')

    expected = msm.get(tctim_bcif_molsys, element='atom', b_factor=True)

    assert structures.b_factor.shape == expected.shape
    assert np.allclose(
        msm.pyunitwizard.get_value(structures.b_factor),
        msm.pyunitwizard.get_value(expected),
    )
