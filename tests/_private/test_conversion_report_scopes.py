"""Testing the static and instance-aware conversion scope contract."""

from molsysmt.basic.conversion_report import ConversionIssue
from molsysmt.native import Topology
from molsysmt._private import conversion_report


def test_conversion_issue_scope_default_preserves_existing_callers():
    issue = ConversionIssue(
        attribute='formal_charge',
        reason='The target cannot represent formal charge.',
    )

    assert issue.kind == 'unsupported'
    assert issue.scope == 'chemical_state'

    issue_with_positional_kind = ConversionIssue(
        'bond_type',
        'The target cannot represent the supplied bond type.',
        'adapter_limitation',
    )
    assert issue_with_positional_kind.kind == 'adapter_limitation'
    assert issue_with_positional_kind.scope == 'chemical_state'


def test_static_identity_scope_requires_route_evidence():
    assert conversion_report.get_conversion_audit_scopes(
        'example.Form', 'example.Form'
    ) == ('representation',)
    assert not conversion_report.is_conversion_audit_exhaustive(
        'example.Form', 'example.Form'
    )


def test_static_cross_form_scope_defaults_to_chemical_state():
    assert conversion_report.get_conversion_audit_scopes(
        'example.Source', 'example.Target'
    ) == ('chemical_state',)
    assert not conversion_report.is_conversion_audit_exhaustive(
        'example.Source', 'example.Target'
    )


def test_explicit_registry_pair_is_exhaustive(monkeypatch):
    pair = ('example.Source', 'example.Target')
    monkeypatch.setattr(
        conversion_report,
        '_EXHAUSTIVE_AUDIT_PAIRS',
        frozenset({pair}),
    )

    assert conversion_report.get_conversion_audit_scopes(*pair) == ('all',)
    assert conversion_report.is_conversion_audit_exhaustive(*pair)


def test_runtime_identity_instance_strengthens_static_scope():
    topology = Topology(n_atoms=1)

    report = conversion_report.build_conversion_report(
        topology,
        'molsysmt.Topology',
        'molsysmt.Topology',
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'exact'
