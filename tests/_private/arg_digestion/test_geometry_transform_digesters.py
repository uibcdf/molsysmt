import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from molsysmt import pyunitwizard as puw
from molsysmt._private.arg_digestion.argument.center import digest_center
from molsysmt._private.arg_digestion.argument.fit import digest_fit
from molsysmt._private.arg_digestion.argument.groups_of_atoms import digest_groups_of_atoms
from molsysmt._private.arg_digestion.argument.origin import digest_origin
from molsysmt._private.arg_digestion.argument.point import digest_point
from molsysmt._private.arg_digestion.argument.vector import digest_vector
from molsysmt._private.arg_digestion.argument.vectors import digest_vectors
from molsysmt._private.arg_digestion.argument.rotation import digest_rotation
from molsysmt._private.arg_digestion.argument.rotations import digest_rotations
from molsysmt._private.arg_digestion.argument.translation import digest_translation
from molsysmt._private.arg_digestion.argument.translations import digest_translations
from molsysmt._private.smonitor import ArgumentError


def test_geometry_and_transform_digesters():
    assert np.array_equal(digest_center([0, 1], caller='molsysmt.basic.convert.convert'), np.array([0, 1], dtype='int64'))
    assert digest_center(True, caller='molsysmt.structure.align_principal_axes.align_principal_axes') is True
    assert np.array_equal(digest_fit([0, 2], caller='molsysmt.basic.convert.convert'), np.array([0, 2], dtype='int64'))
    assert digest_groups_of_atoms([[0, 1], [2, 3]]) == [[0, 1], [2, 3]]
    assert digest_origin(None, caller='molsysmt.third_party.nglview.add_arrows.add_arrows') is None
    assert digest_origin('atom_index==0', caller='molsysmt.third_party.nglview.add_arrows.add_arrows') == 'atom_index==0'

    point = digest_point(puw.quantity([0.0, 1.0, 2.0], 'nm'))
    assert point.shape == (1, 3)
    assert np.array_equal(digest_vector([1.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]))
    vectors = digest_vectors(puw.quantity([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], 'nm'), caller='molsysmt.third_party.nglview.add_cylinders.add_cylinders')
    assert vectors.shape[-1] == 3

    rot = digest_rotation(np.eye(3))
    assert rot.shape == (1, 1, 3, 3)
    assert isinstance(digest_rotation(Rotation.identity()), Rotation)
    rots = digest_rotations([np.eye(3), np.eye(3)], caller='digest_bioassembly')
    assert len(rots) == 2

    trans = digest_translation(puw.quantity([[1.0, 2.0, 3.0]], 'nm'))
    assert trans.shape[-1] == 3
    transs = digest_translations([puw.quantity([[1.0, 2.0, 3.0]], 'nm')], caller='digest_bioassembly')
    assert len(transs) == 1

    with pytest.raises(ArgumentError):
        digest_groups_of_atoms('bad')
    with pytest.raises(ArgumentError):
        digest_vector([1.0, 2.0])
