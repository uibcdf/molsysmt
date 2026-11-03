"""Protect executable-plan inventory without treating an audit as a runtime test."""

from devtools.scripts.audit_conversion_execution import (
    audit_plan,
    declared_edges,
    planned_edges,
    read_plan,
)


def _plan():
    return {
        "schema_version": 1,
        "profile": "control",
        "source_forms": ["native"],
        "target_forms": ["native"],
        "accepted_unexecuted_edges": {
            "external": {"targets": ["native"], "reason": "Needs an external fixture."}
        },
    }


def test_new_unexecuted_route_requires_explicit_disposition():
    graph = {("native", "native"), ("external", "native")}
    report = audit_plan(graph, _plan())
    assert report["errors"] == []
    assert report["execution"] == "not performed by this audit"
    assert report["planned_smoke_edges"] == 1
    graph.add(("new", "native"))
    assert "New unexecuted edge: new -> native" in audit_plan(graph, _plan())["errors"]


def test_new_route_inside_profile_becomes_an_executable_case():
    plan = _plan()
    plan["target_forms"].append("other")
    graph = {("native", "native"), ("external", "native"), ("native", "other")}
    assert ("native", "other") in planned_edges(graph, plan)
    assert audit_plan(graph, plan)["errors"] == []


def test_retired_or_newly_covered_debt_must_be_removed():
    plan = _plan()
    assert (
        "Stale unexecuted debt: external -> native"
        in audit_plan({("native", "native")}, plan)["errors"]
    )
    plan["source_forms"].append("external")
    assert (
        "Stale unexecuted debt: external -> native"
        in audit_plan({("native", "native"), ("external", "native")}, plan)["errors"]
    )


def test_debt_requires_a_reason():
    plan = _plan()
    plan["accepted_unexecuted_edges"]["external"]["reason"] = ""
    assert (
        "external: unexecuted edges require a reason."
        in audit_plan({("external", "native")}, plan)["errors"]
    )


def test_repository_execution_plan_is_current():
    assert audit_plan(declared_edges(), read_plan())["errors"] == []


def test_declared_inventory_ignores_visibility_filter_and_restores_policy():
    from molsysmt import configure

    expected = declared_edges()
    with configure.context(show_all_capabilities=False):
        assert declared_edges() == expected
        assert configure.show_all_capabilities is False


def test_explicit_routes_are_selected_and_cannot_conceal_stale_debt():
    plan = _plan()
    graph = {("native", "native"), ("external", "native")}
    plan["explicit_edges"] = [["external", "native"]]
    assert ("external", "native") in planned_edges(graph, plan)
    assert (
        "Stale unexecuted debt: external -> native" in audit_plan(graph, plan)["errors"]
    )
    plan["accepted_unexecuted_edges"] = {}
    assert audit_plan(graph, plan)["errors"] == []
    plan["explicit_edges"].append(["unknown", "native"])
    assert any(
        "Invalid explicit edge" in error for error in audit_plan(graph, plan)["errors"]
    )
