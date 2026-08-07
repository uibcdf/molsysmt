import numpy as np
import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.alternate_location import digest_alternate_location
from molsysmt._private.argdigest.argument.attribute import digest_attribute
from molsysmt._private.argdigest.argument.bioassembly import digest_bioassembly
from molsysmt._private.argdigest.argument.center import digest_center
from molsysmt._private.argdigest.argument.comparison import digest_comparison
from molsysmt._private.argdigest.argument.compression import digest_compression
from molsysmt._private.argdigest.argument.compression_opts import digest_compression_opts
from molsysmt import pyunitwizard as puw


def test_digest_attribute_accepts_known_attributes_and_aggregates():
    assert digest_attribute('atom_name') == 'atom_name'
    assert digest_attribute('Topological', caller='molsysmt.basic.has_attribute.has_attribute') == 'topological'
    with pytest.raises(ArgumentError):
        digest_attribute('not_an_attribute')


def test_digest_center_accepts_convert_and_align_cases():
    assert digest_center('atom_index==0', caller='molsysmt.basic.convert.convert') == 'atom_index==0'
    assert np.array_equal(digest_center(3, caller='molsysmt.basic.convert.convert'), np.array([3], dtype='int64'))
    assert np.array_equal(
        digest_center([1, 2], caller='molsysmt.basic.convert.convert'),
        np.array([1, 2], dtype='int64'),
    )
    assert digest_center(None, caller='molsysmt.basic.convert.convert') is None
    assert digest_center(True, caller='molsysmt.structure.align_principal_axes.align_principal_axes') is True
    with pytest.raises(ArgumentError):
        digest_center('bad')


def test_digest_comparison_and_h5msm_compression_variants():
    assert digest_comparison('equal', rule='equal', caller='molsysmt.basic.compare.compare.compare') == 'equal'
    assert digest_comparison('in', rule='in', caller='molsysmt.basic.compare.compare.compare') == 'in'
    with pytest.raises(ArgumentError):
        digest_comparison('equal', rule='in', caller='molsysmt.basic.compare.compare.compare')

    caller = 'molsysmt.form.molsysmt_MolSys.to_file_h5msm'
    assert digest_compression('gzip', caller=caller) == 'gzip'
    assert digest_compression('lzf', caller=caller) == 'lzf'
    assert digest_compression_opts(0, caller=caller) == 0
    assert digest_compression_opts(9, caller=caller) == 9
    with pytest.raises(ArgumentError):
        digest_compression('zip', caller=caller)
    with pytest.raises(ArgumentError):
        digest_compression_opts(10, caller=caller)


def test_digest_bioassembly_accepts_boolean_and_declared_formats():
    boolean_caller = 'molsysmt.basic.get.get'
    assert digest_bioassembly(True, caller=boolean_caller) is True

    make_caller = 'molsysmt.build.make_bioassembly.make_bioassembly'
    single = {
        'chain_indices': [[0], [1]],
        'rotations': [np.eye(3), np.eye(3)],
        'translations': [
            puw.quantity([0.0, 0.0, 0.0], 'nanometers'),
            puw.quantity([1.0, 1.0, 1.0], 'nanometers'),
        ],
    }
    digested_single = digest_bioassembly(single, caller=make_caller)
    assert len(digested_single['chain_indices']) == 2

    mapping = {
        'bio1': {
            'chain_indices': [[0]],
            'rotations': [np.eye(3)],
            'translations': [puw.quantity([0.0, 0.0, 0.0], 'nanometers')],
        }
    }
    digested_mapping = digest_bioassembly(mapping)
    assert len(digested_mapping['bio1']['chain_indices']) == 1
    assert np.array_equal(digested_mapping['bio1']['chain_indices'][0], np.array([0], dtype='int64'))

    with pytest.raises(ArgumentError):
        digest_bioassembly({'bad': {}}, caller=make_caller)


def test_digest_alternate_location_accepts_boolean_none_and_mapping_payloads():
    boolean_caller = 'molsysmt.basic.get.get'
    assert digest_alternate_location(False, caller=boolean_caller) is False
    assert digest_alternate_location(None) is None

    payload = {
        0: {
            'location_id': np.array(['A', 'B']),
            'occupancy': np.array([[0.6, 0.4]], dtype=np.float64),
            'b_factor': puw.quantity([[10.0, 12.0]], 'angstroms**2'),
            'atom_id': ['1', '2'],
            'coordinates': puw.quantity([[[0.0, 0.0, 0.0], [0.1, 0.1, 0.1]]], 'nanometers'),
        }
    }
    digested = digest_alternate_location(payload)
    assert isinstance(digested, list)
    assert digested[0][0]['location_id'].shape == (2,)
    assert digested[0][0]['occupancy'].shape == (2,)
    assert digested[0][0]['b_factor'].shape == (2,)
    assert digested[0][0]['coordinates'].shape == (2, 3)

    bad_payload = {
        0: {
            'location_id': np.array(['A', 'B']),
            'occupancy': np.array([[0.6]], dtype=np.float64),
            'b_factor': puw.quantity([[10.0, 12.0]], 'angstroms**2'),
            'atom_id': ['1','2'],
            'coordinates': puw.quantity([[[0.0, 0.0, 0.0], [0.1, 0.1, 0.1]]], 'nanometers'),
        }
    }
    with pytest.raises(ArgumentError):
        digest_alternate_location(bad_payload)
