import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.argdigest.argument.n_atoms import digest_n_atoms
from molsysmt._private.argdigest.argument.n_groups import digest_n_groups
from molsysmt._private.argdigest.argument.n_chains import digest_n_chains
from molsysmt._private.argdigest.argument.n_components import digest_n_components
from molsysmt._private.argdigest.argument.n_molecules import digest_n_molecules
from molsysmt._private.argdigest.argument.n_entities import digest_n_entities
from molsysmt._private.argdigest.argument.n_nucleotides import digest_n_nucleotides
from molsysmt._private.argdigest.argument.n_peptides import digest_n_peptides
from molsysmt._private.argdigest.argument.n_dnas import digest_n_dnas
from molsysmt._private.argdigest.argument.n_rnas import digest_n_rnas
from molsysmt._private.argdigest.argument.element import digest_element
from molsysmt._private.argdigest.argument.from_element import digest_from_element
from molsysmt._private.argdigest.argument.water_model import digest_water_model


def test_count_digesters_accept_boolean_int_and_native_counts():
    specs = [
        (digest_n_atoms, 'n_atoms'),
        (digest_n_groups, 'n_groups'),
        (digest_n_chains, 'n_chains'),
        (digest_n_components, 'n_components'),
        (digest_n_molecules, 'n_molecules'),
        (digest_n_entities, 'n_entities'),
    ]
    for digester, _ in specs:
        assert digester(True, caller='molsysmt.basic.get.get') is True
        assert digester(3, caller='molsysmt.basic.contains.contains') == 3
        assert digester(4, caller='molsysmt.basic.is_composed_of.is_composed_of') == 4
        assert digester(5, caller='molsysmt.native.topology.__init__') == 5
        assert digester(6, caller='molsysmt.native.molsys.__init__') == 6
        with pytest.raises(ArgumentError):
            digester('bad', caller='molsysmt.basic.get.get')


def test_element_digesters_accept_singular_plural_and_none_when_allowed():
    assert digest_element('atom') == 'atom'
    assert digest_element('atoms') == 'atom'
    assert digest_element(None, caller='molsysmt.basic.set.set') is None
    with pytest.raises(ArgumentError):
        digest_element(None)

    assert digest_from_element('group') == 'group'
    assert digest_from_element('groups') == 'group'
    assert digest_from_element(None, caller='molsysmt.topology.bonds_are_required_to_get_attribute') is None
    with pytest.raises(ArgumentError):
        digest_from_element(None)


def test_water_model_digester_accepts_boolean_none_and_known_models():
    assert digest_water_model(True, caller='molsysmt.basic.get.get') is True
    assert digest_water_model(None) is None
    assert digest_water_model('tip3p') == 'TIP3P'
    with pytest.raises(ArgumentError):
        digest_water_model('bad-model')


def test_composition_count_digesters_accept_the_three_callers_that_ask_for_them():
    """`n_nucleotides` was the one attribute of 118 with no digester, so it accepted
    any type and answered 0. See uibcdf/molsysmt#208."""
    for digester in (digest_n_nucleotides, digest_n_peptides, digest_n_dnas, digest_n_rnas):
        assert digester(True, caller='molsysmt.basic.get.get') is True
        assert digester(2, caller='molsysmt.basic.contains.contains') == 2
        assert digester(3, caller='molsysmt.basic.is_composed_of.is_composed_of') == 3
        with pytest.raises(ArgumentError):
            digester('no soy booleano', caller='molsysmt.basic.get.get')
        with pytest.raises(ArgumentError):
            digester(True, caller='molsysmt.native.topology.__init__')
