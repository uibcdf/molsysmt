import numpy as np
import pytest
from matplotlib.colors import Colormap

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.color import digest_color
from molsysmt._private.arg_digestion.argument.color_values import digest_color_values
from molsysmt._private.arg_digestion.argument.colormap import digest_colormap
from molsysmt._private.arg_digestion.argument.file import digest_file
from molsysmt._private.arg_digestion.argument.form import digest_form
from molsysmt._private.arg_digestion.argument.show import digest_show
from molsysmt._private.arg_digestion.argument.style import digest_style
from molsysmt import pyunitwizard as puw

WRITE_H5_CALLER = 'molsysmt.form.molsysmt_Topology.write_topology_in_h5msm'
SHOW_CONTACTS_CALLER = 'molsysmt.structure.show_contacts.show_contacts'
COMPARE_CALLER = 'molsysmt.basic.compare.compare'


def test_digest_color_accepts_hex_named_and_rgb_triplets():
    assert digest_color('#aabbcc') == '#aabbcc'
    assert digest_color('red') == 'red'
    rgb = [0.1, 0.2, 0.3]
    assert digest_color(rgb) == rgb


def test_digest_color_rejects_invalid_values():
    with pytest.raises(ArgumentError):
        digest_color(3.14)

    with pytest.raises(ArgumentError):
        digest_color([0.1, 0.2])


def test_digest_color_values_accept_iterables_and_quantities():
    values = [1.0, 2.0, 3.0]
    assert digest_color_values(values) == values

    quantity = puw.quantity(np.array([1.0, 2.0]), 'kilocalorie/mole')
    digested = digest_color_values(quantity)
    np.testing.assert_allclose(digested, np.array([1.0, 2.0]))


def test_digest_colormap_accepts_name_and_instance():
    cmap = digest_colormap('viridis')
    assert isinstance(cmap, Colormap)
    assert digest_colormap(cmap) is cmap
    assert digest_colormap(None) is None

    with pytest.raises(ArgumentError):
        digest_colormap('not-a-colormap')


def test_digest_form_accepts_bool_for_compare_and_resolves_names():
    assert digest_form(True, caller=COMPARE_CALLER) is True
    assert digest_form('molsysmt.molsys', caller=COMPARE_CALLER) == 'molsysmt.MolSys'
    assert digest_form(['molsysmt.molsys', 'molsysmt.topology'], caller=COMPARE_CALLER) == [
        'molsysmt.MolSys',
        'molsysmt.Topology',
    ]
    assert digest_form(msm.systems['T4 lysozyme L99A']['181l.h5msm'], caller=COMPARE_CALLER) == msm.systems['T4 lysozyme L99A']['181l.h5msm']

    with pytest.raises(ArgumentError):
        digest_form('definitely-not-a-form', caller=COMPARE_CALLER)


def test_digest_show_and_style_validate_expected_contracts():
    assert digest_show(True) is True
    assert digest_show(False) is False

    with pytest.raises(ArgumentError):
        digest_show('yes')

    assert digest_style('plotly', caller=SHOW_CONTACTS_CALLER) == 'plotly'
    assert digest_style('matplotlib', caller=SHOW_CONTACTS_CALLER) == 'matplotlib'

    with pytest.raises(ArgumentError):
        digest_style('nglview', caller=SHOW_CONTACTS_CALLER)


def test_digest_file_accepts_h5msm_path_and_handler_for_h5_writer(tmp_path):
    source = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    assert digest_file(source, caller=WRITE_H5_CALLER) == source

    handler = msm.convert(source, to_form='molsysmt.H5MSMFileHandler')
    try:
        assert digest_file(handler, caller=WRITE_H5_CALLER) is handler
    finally:
        handler.file.close()

    with pytest.raises(ArgumentError):
        digest_file(tmp_path / 'not_h5msm.txt', caller=WRITE_H5_CALLER)
