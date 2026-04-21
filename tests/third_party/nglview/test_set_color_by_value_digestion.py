import numpy as np
import molsysmt as msm


def test_set_color_by_value_accepts_numpy_scalar_limits():

    molecular_system = msm.convert(
        msm.systems['T4 lysozyme L99A']['181l.h5msm'],
        selection='molecule_type=="protein"',
    )

    b_factors = msm.get(molecular_system, element='atom', b_factor=True)

    view = msm.view(molecular_system, viewer='NGLView')
    view.clear()

    msm.thirds.nglview.set_color_by_value(
        view,
        b_factors[0],
        element='atom',
        min_value=np.float32(0.0),
        max_value=np.float32(1.0),
    )

    assert view._ngl_msg_archive[-1]['reconstruc_color_scheme'] is True
