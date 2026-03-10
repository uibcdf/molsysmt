import numpy as np
import molsysmt as msm


def test_file_h5msm_preserves_b_factor_roundtrip(tmp_path, tctim_bcif_molsys):

    output_path = tmp_path / 'tctim_bfactor.h5msm'

    msm.convert(tctim_bcif_molsys, to_form='file:h5msm', output_filename=str(output_path))

    b_factor_from_file = msm.get(str(output_path), element='atom', b_factor=True)
    b_factor_from_molsys = msm.get(tctim_bcif_molsys, element='atom', b_factor=True)

    assert b_factor_from_file is not None
    assert msm.pyunitwizard.check(b_factor_from_file, unit='nm^2')
    assert b_factor_from_file.shape == b_factor_from_molsys.shape
    assert np.allclose(
        msm.pyunitwizard.get_value(b_factor_from_file),
        msm.pyunitwizard.get_value(b_factor_from_molsys),
    )
