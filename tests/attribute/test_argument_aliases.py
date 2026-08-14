from molsysmt.attribute import attributes, get_argument_aliases
from molsysmt._private.argdigest.normalization.attribute_synonyms import (
    _ATTRIBUTE_TAKING_CALLERS,
    TABLES as ATTRIBUTE_TABLES,
)
from molsysmt._private.argdigest.normalization.get_element_names import TABLES as ELEMENT_TABLES


def test_contract_has_versioned_plain_data():
    contract = get_argument_aliases()

    assert set(contract) == {
        'schema_version',
        'attribute_synonyms',
        'element_attribute_aliases',
    }
    assert contract['schema_version'] == 1
    assert isinstance(contract['attribute_synonyms'], dict)
    assert isinstance(contract['element_attribute_aliases'], dict)


def test_all_alias_targets_are_canonical_attributes_without_chains():
    synonyms = get_argument_aliases()['attribute_synonyms']

    assert not (set(synonyms) & set(attributes))
    assert set(synonyms.values()) <= set(attributes)
    assert not (set(synonyms.values()) & set(synonyms))
    assert all(alias != canonical for alias, canonical in synonyms.items())


def test_element_aliases_are_explicit_and_canonical():
    element_aliases = get_argument_aliases()['element_attribute_aliases']

    assert set(element_aliases) == {
        'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'bond'
    }
    for element, aliases in element_aliases.items():
        assert all(canonical in attributes for canonical in aliases.values())
        assert all(canonical.startswith(f'{element}_') for canonical in aliases.values())
        assert all(alias != canonical for alias, canonical in aliases.items())


def test_each_call_returns_a_defensive_copy():
    changed = get_argument_aliases()
    changed['attribute_synonyms']['invented'] = 'atom_name'
    changed['element_attribute_aliases']['atom']['name'] = 'group_name'

    fresh = get_argument_aliases()
    assert 'invented' not in fresh['attribute_synonyms']
    assert fresh['element_attribute_aliases']['atom']['name'] == 'atom_name'


def test_runtime_attribute_tables_match_the_public_provider():
    synonyms = get_argument_aliases()['attribute_synonyms']

    assert len(ATTRIBUTE_TABLES) == len(_ATTRIBUTE_TAKING_CALLERS)
    for table, caller in zip(ATTRIBUTE_TABLES, _ATTRIBUTE_TAKING_CALLERS, strict=True):
        assert table.applies_to == caller
        assert table.aliases == synonyms


def test_runtime_element_tables_match_the_public_provider():
    expected = get_argument_aliases()['element_attribute_aliases']
    observed = {table.when['element']: table.aliases for table in ELEMENT_TABLES}

    assert observed == expected
