import numpy as np
import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.group_behavior import digest_group_behavior
from molsysmt._private.argdigest.argument.group_behavior_2 import digest_group_behavior_2
from molsysmt._private.argdigest.argument.groups_of_atoms import digest_groups_of_atoms
from molsysmt._private.argdigest.argument.groups_of_atoms_2 import digest_groups_of_atoms_2
from molsysmt._private.argdigest.argument.hydrogens import digest_hydrogens
from molsysmt._private.argdigest.argument.elements import digest_elements
from molsysmt._private.argdigest.argument.flexible_constraints import digest_flexible_constraints
from molsysmt._private.argdigest.argument.float_precision import digest_float_precision
from molsysmt._private.argdigest.argument.exclusion_rules import digest_exclusion_rules
from molsysmt._private.argdigest.argument.decomposition import digest_decomposition
from molsysmt._private.argdigest.argument.fit import digest_fit


def test_group_behavior_digesters_accept_supported_values():
    assert digest_group_behavior(None) is None
    assert digest_group_behavior('center of mass') == 'center of mass'
    assert digest_group_behavior('Geometric Center') == 'geometric center'
    assert digest_group_behavior_2('closest') == 'closest'
    with pytest.raises(ArgumentError):
        digest_group_behavior('bad')
    with pytest.raises(ArgumentError):
        digest_group_behavior_2('bad')


def test_groups_of_atoms_digesters_accept_nested_index_sequences():
    assert digest_groups_of_atoms(None) is None
    assert digest_groups_of_atoms([[0, 1], range(2, 4)]) == [[0, 1], [2, 3]]
    assert digest_groups_of_atoms_2(((0, 2), [1, 3])) == [[0, 2], [1, 3]]
    with pytest.raises(ArgumentError):
        digest_groups_of_atoms('bad')
    with pytest.raises(ArgumentError):
        digest_groups_of_atoms_2(['bad'])


def test_hydrogens_and_elements_caller_sensitive_semantics():
    assert digest_hydrogens(True, caller='molsysmt.basic.contains.contains') is True
    assert digest_hydrogens(None, caller='molsysmt.basic.contains.contains') is None
    with pytest.raises(ArgumentError):
        digest_hydrogens(True)

    assert digest_elements(True, caller='molsysmt.basic.compare.compare') is True
    with pytest.raises(ArgumentError):
        digest_elements(['H', 'O'])


def test_constraints_precision_exclusion_decomposition_and_fit_digesters():
    form_caller = 'molsysmt.form.openmm_Topology.to_openmm_System'
    assert digest_flexible_constraints('HBonds', caller=form_caller) == 'HBonds'
    assert digest_flexible_constraints(None, caller=form_caller) is None
    with pytest.raises(ArgumentError):
        digest_flexible_constraints(None)

    assert digest_float_precision('single', caller='molsysmt.form.molsysmt_MolSys.to_file_h5msm') == 'single'
    assert digest_float_precision('double', caller='molsysmt.form.molsysmt_Structures.to_file_h5msm') == 'double'
    with pytest.raises(ArgumentError):
        digest_float_precision('single')

    assert digest_exclusion_rules(None) == []
    assert digest_exclusion_rules('bonded') == ['bonded']
    assert digest_exclusion_rules(('bonded', 'same_group')) == ['bonded', 'same_group']
    assert digest_exclusion_rules(['bonded']) == ['bonded']
    with pytest.raises(ArgumentError):
        digest_exclusion_rules(1)

    assert digest_decomposition(True, caller='molsysmt.molecular_mechanics.get_potential_energy.get_potential_energy') is True
    with pytest.raises(ArgumentError):
        digest_decomposition('group')
    with pytest.raises(ArgumentError):
        digest_decomposition(True)

    convert_caller = 'molsysmt.basic.convert.convert'
    assert digest_fit(None, caller=convert_caller) is None
    assert digest_fit('name == "CA"', caller=convert_caller) == 'name == "CA"'
    np.testing.assert_array_equal(digest_fit(3, caller=convert_caller), np.array([3], dtype='int64'))
    np.testing.assert_array_equal(digest_fit([0, 2], caller=convert_caller), np.array([0, 2], dtype='int64'))
    with pytest.raises(ArgumentError):
        digest_fit('name == "CA"')
