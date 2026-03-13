import pytest

import molsysmt as msm
from molsysmt._private.arg_digestion.argument.as_entity import digest_as_entity
from molsysmt._private.arg_digestion.argument.as_entity_2 import digest_as_entity_2
from molsysmt._private.arg_digestion.argument.filename import digest_filename
from molsysmt._private.arg_digestion.argument.keys import digest_keys
from molsysmt._private.arg_digestion.argument.pairs import digest_pairs
from molsysmt._private.arg_digestion.argument.representation import digest_representation
from molsysmt._private.arg_digestion.argument.view import digest_view
from molsysmt._private.arg_digestion.argument.viewer import digest_viewer
from molsysmt._private.smonitor import ArgumentError


def test_viewer_and_misc_digesters():
    view = msm.view(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'], viewer='NGLView')
    assert digest_view(view) is view
    assert digest_viewer('nglview') == 'NGLView'
    assert digest_representation('cartoon', caller='molsysmt.thirds.nglview.add_representation.add_representation') == 'cartoon'
    assert digest_pairs(True) is True
    assert digest_filename('output.dat') == 'output.dat'
    assert digest_as_entity(True) is True
    assert digest_as_entity_2(False) is False
    assert digest_keys('group_name', caller='molsysmt.build.mutate.mutate') == 'group_name'

    with pytest.raises(ArgumentError):
        digest_viewer('bad-viewer')
    with pytest.raises(ArgumentError):
        digest_pairs('yes')
    with pytest.raises(ArgumentError):
        digest_filename(5)
