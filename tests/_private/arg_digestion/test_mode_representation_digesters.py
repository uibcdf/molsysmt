import matplotlib as mpl
import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.representation import digest_representation
from molsysmt._private.argdigest.argument.cmap import digest_cmap
from molsysmt._private.argdigest.argument.color_2 import digest_color_2
from molsysmt._private.argdigest.argument.color_values_scale import digest_color_values_scale
from molsysmt._private.argdigest.argument.color_values_scale_2 import digest_color_values_scale_2


def test_representation_is_caller_sensitive():
    assert digest_representation('cartoon', caller='molsysmt.third_party.nglview.add_representation') == 'cartoon'
    with pytest.raises(ArgumentError):
        digest_representation('cartoon')


def test_cmap_and_color_digesters_accept_supported_visual_inputs():
    cmap = digest_cmap('viridis')
    assert cmap.name == 'viridis'
    listed = mpl.colormaps['Set1']
    assert digest_cmap(listed) is listed

    assert digest_color_2('#ffffff') == '#ffffff'
    assert digest_color_2((1.0, 0.5, 0.0)) == (1.0, 0.5, 0.0)
    with pytest.raises(ArgumentError):
        digest_color_2('white')

    assert digest_color_values_scale('linear') == 'linear'
    assert digest_color_values_scale_2('log') == 'log'
    with pytest.raises(ArgumentError):
        digest_color_values_scale('exp')
