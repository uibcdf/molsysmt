from types import SimpleNamespace

from devtools.scripts import validate_form_adapters as validator


def _module(*, getters=(), topological_pipe=None, structural_pipe=None, converters=None):
    module = SimpleNamespace(
        piped_topological_attribute=topological_pipe,
        piped_structural_attribute=structural_pipe,
        _convert_to=converters or {},
        attributes={"atom_name": True},
    )
    for getter_name in getters:
        setattr(module, getter_name, lambda item: item)
    return module


TOPOLOGICAL_ATTRIBUTE = {
    "get_from": ["atom"],
    "topological": True,
    "structural": False,
}


def test_attribute_delivery_accepts_a_catalog_compatible_direct_getter():
    modules = {
        "source": _module(getters=("get_atom_name_from_atom",)),
    }

    assert validator._attribute_is_deliverable(
        "source",
        "atom_name",
        modules,
        {"atom_name": TOPOLOGICAL_ATTRIBUTE},
    )


def test_attribute_delivery_follows_a_lazy_converter_pipe():
    modules = {
        "source": _module(
            topological_pipe="target",
            converters={"target": "to_target"},
        ),
        "target": _module(getters=("get_atom_name_from_atom",)),
    }

    assert validator._attribute_is_deliverable(
        "source",
        "atom_name",
        modules,
        {"atom_name": TOPOLOGICAL_ATTRIBUTE},
    )


def test_attribute_delivery_rejects_a_pipe_without_a_converter():
    modules = {
        "source": _module(topological_pipe="target"),
        "target": _module(getters=("get_atom_name_from_atom",)),
    }

    assert not validator._attribute_is_deliverable(
        "source",
        "atom_name",
        modules,
        {"atom_name": TOPOLOGICAL_ATTRIBUTE},
    )


def test_attribute_delivery_accepts_a_registered_derivation():
    module = _module()
    module.attributes.update({'box': True, 'box_lengths': True})
    module.get_box_from_system = lambda item: item
    modules = {'source': module}
    catalog = {
        'box_lengths': {
            'get_from': ['system'],
            'topological': False,
            'structural': True,
        }
    }

    assert validator._attribute_is_deliverable(
        'source',
        'box_lengths',
        modules,
        catalog,
    )


def test_delivery_baseline_comparison_is_a_monotonic_ratchet(monkeypatch):
    monkeypatch.setattr(
        validator,
        "_load_attribute_delivery_baseline",
        lambda: {"source": {"old_debt", "resolved_debt"}},
    )

    new, resolved = validator._compare_delivery_with_baseline(
        {"source": ["old_debt", "new_debt"]}
    )

    assert new == {"source": ["new_debt"]}
    assert resolved == {"source": ["resolved_debt"]}


def test_tier_1_delivery_debt_is_never_accepted():
    violations = {
        "contractual": ["atom_name"],
        "best_effort": ["group_name"],
    }
    tiers = {"contractual": 1, "best_effort": 2}

    assert validator._tier_1_delivery_violations(violations, tiers) == {
        "contractual": ["atom_name"]
    }
