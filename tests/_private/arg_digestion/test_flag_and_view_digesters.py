import nglview as nv
import pytest

from molsysmt import MolSysBuilder
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.progress_bar import digest_progress_bar
from molsysmt._private.arg_digestion.argument.verbose import digest_verbose
from molsysmt._private.arg_digestion.argument.to_html import digest_to_html
from molsysmt._private.arg_digestion.argument.constant_box import digest_constant_box
from molsysmt._private.arg_digestion.argument.constant_id_step import digest_constant_id_step
from molsysmt._private.arg_digestion.argument.constant_time_step import digest_constant_time_step
from molsysmt._private.arg_digestion.argument.keep import digest_keep
from molsysmt._private.arg_digestion.argument.wrap import digest_wrap
from molsysmt._private.arg_digestion.argument.view import digest_view


def test_boolean_flag_digesters_accept_only_bool():
    assert digest_progress_bar(True) is True
    assert digest_verbose(False) is False
    assert digest_to_html(True) is True
    assert digest_constant_box(False) is False
    assert digest_constant_id_step(True) is True
    assert digest_constant_time_step(False) is False
    with pytest.raises(ArgumentError):
        digest_progress_bar('yes')


def test_keep_and_wrap_digesters_use_caller_sensitive_semantics():
    keep_caller = 'molsysmt.build.remove_atoms_with_alternate_locations.remove_atoms_with_alternate_locations'
    assert digest_keep('A', caller=keep_caller) == 'A'
    with pytest.raises(ArgumentError):
        digest_keep('AA', caller=keep_caller)

    convert_caller = 'molsysmt.basic.convert.convert'
    assert digest_wrap('MIC', caller=convert_caller) == 'mic'
    assert digest_wrap('pbc', caller=convert_caller) == 'pbc'
    assert digest_wrap('unwrap', caller=convert_caller) == 'unwrap'
    with pytest.raises(ArgumentError):
        digest_wrap('bad', caller=convert_caller)


def test_view_digester_accepts_supported_view_objects():
    builder = MolSysBuilder()
    builder.add_atom(atom_name='Ar', atom_type='Ar')
    molsys = builder.build()
    ngl_view = nv.NGLWidget()
    ngl_view._ngl_component_ids = []
    assert digest_view(ngl_view) is ngl_view
    with pytest.raises(ArgumentError):
        digest_view(molsys)
