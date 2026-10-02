import numpy as np

import molsysmt as msm


def test_molsysmt_H5MSMFileHandler_preserves_b_factor_roundtrip(
    tmp_path, tctim_bcif_molsys
):

    output_path = tmp_path / "tctim_bfactor_handler.h5msm"

    # This handler owns the legacy 0.3/0.4 layout; public convert writes 0.5.
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm

    to_file_h5msm(tctim_bcif_molsys, output_filename=str(output_path))

    handler = msm.convert(str(output_path), to_form="molsysmt.H5MSMFileHandler")
    structures = msm.convert(handler, to_form="molsysmt.Structures")

    assert structures.b_factor is not None
    assert msm.pyunitwizard.check(structures.b_factor, unit="nm^2")

    expected = msm.get(tctim_bcif_molsys, element="atom", b_factor=True)

    assert structures.b_factor.shape == expected.shape
    assert np.allclose(
        msm.pyunitwizard.get_value(structures.b_factor),
        msm.pyunitwizard.get_value(expected),
    )
