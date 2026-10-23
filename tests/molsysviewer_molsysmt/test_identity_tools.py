"""Receiving bound identity queries and an explicitly supplied collection utility."""

import inspect

import molsysviewer as msv
import pytest

import molsysmt as msm

pytest.importorskip("molsysviewer.system_edits")


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            yield result


@pytest.mark.parametrize(
    "name",
    [
        "get_form",
        "is_a_molecular_system",
        "are_multiple_molecular_systems",
        "where_is_attribute",
    ],
)
def test_signature_and_digestion_exception_are_explicit(view, name):
    native = inspect.signature(getattr(msm.basic, name))
    expected = list(native.parameters.values())
    if name != "are_multiple_molecular_systems":
        expected = expected[1:]
    if name != "where_is_attribute":
        assert "skip_digestion" not in native.parameters
        expected.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    bound = getattr(view.addons.molsysmt.basic, name)
    assert list(inspect.signature(bound).parameters.values()) == expected
    assert bound.digestion_plan is not None
    assert getattr(view.addons.molsysmt, name) == bound
    documentation = inspect.getdoc(bound)
    if name == "are_multiple_molecular_systems":
        assert "\nmolecular_systems :" in documentation
        assert "no current view.molsys is inserted" in documentation
    else:
        assert "current view.molsys" in documentation
        assert "\nmolecular_system :" not in documentation
    if name != "where_is_attribute":
        assert "receives no such argument" in documentation


@pytest.mark.parametrize("name", ["get_form", "is_a_molecular_system"])
@pytest.mark.parametrize("trusted", [False, True])
def test_undigested_native_helpers_keep_native_results(view, name, trusted):
    native = getattr(msm.basic, name)
    before = view.export_state()
    status = view.addons.molsysmt.get_sync_status()
    expected = native(view.molsys)
    actual = getattr(view.addons.molsysmt, name)(skip_digestion=trusted)
    assert type(actual) is type(expected)
    assert actual == expected
    assert getattr(msm.basic, name) is native
    assert view.export_state() == before
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize(
    "attribute, include_none",
    [
        ("coordinates", False),
        ("COORDINATES", False),
        ("atom_name", False),
        ("velocities", False),
        ("velocities", True),
    ],
)
def test_location_preserves_native_live_item_form_and_none_policy(
    view, attribute, include_none
):
    expected_item, expected_form = msm.where_is_attribute(
        view.molsys, attribute, include_none=include_none
    )
    before = view.export_state()
    actual_item, actual_form = view.addons.molsysmt.where_is_attribute(
        attribute, include_none=include_none
    )
    assert actual_item is expected_item
    assert actual_form == expected_form
    if actual_item is not None:
        assert actual_item is view.molsys
    assert view.export_state() == before


@pytest.mark.parametrize("kind", ["one", "two", "tuple", "empty", "bare", "invalid"])
def test_explicit_collection_is_not_prefixed_combined_or_reinterpreted(view, kind):
    reference = msm.copy(view.molsys)
    cases = {
        "one": [reference],
        "two": [view.molsys, reference],
        "tuple": (reference,),
        "empty": [],
        "bare": reference,
        "invalid": [object()],
    }
    inputs = cases[kind]
    expected = msm.are_multiple_molecular_systems(inputs)
    before = view.export_state()
    target = view.molsys
    actual = view.addons.molsysmt.are_multiple_molecular_systems(
        inputs, skip_digestion=(kind == "tuple")
    )
    assert type(actual) is type(expected)
    assert actual == expected
    assert view.molsys is target
    assert view.export_state() == before
    if kind == "empty":
        assert actual is False
    elif kind == "one":
        assert actual is True  # Native meaning: a valid container, not at least two.


def test_explicit_collection_works_before_loading_and_does_not_load(view):
    with msv.MolSysView() as empty:
        inputs = [view.molsys]
        status = empty.addons.molsysmt.get_sync_status()
        assert empty.addons.molsysmt.are_multiple_molecular_systems(inputs) is True
        assert empty.molsys is None
        assert empty.addons.molsysmt.get_sync_status() == status
        for name, args in [
            ("get_form", ()),
            ("is_a_molecular_system", ()),
            ("where_is_attribute", ("coordinates",)),
        ]:
            with pytest.raises(ValueError, match="Load a molecular system"):
                getattr(empty.addons.molsysmt, name)(*args)


@pytest.mark.parametrize(
    "name",
    [
        "get_form",
        "is_a_molecular_system",
        "are_multiple_molecular_systems",
        "where_is_attribute",
    ],
)
def test_invalid_addon_escape_hatch_is_rejected(view, name):
    args = {
        "are_multiple_molecular_systems": ([view.molsys],),
        "where_is_attribute": ("coordinates",),
    }.get(name, ())
    with pytest.raises(msm.ArgumentError):
        getattr(view.addons.molsysmt, name)(*args, skip_digestion="yes")


def test_unknown_location_attribute_retains_native_error(view):
    with pytest.raises(Exception) as native:
        msm.where_is_attribute(view.molsys, "not_an_attribute")
    with pytest.raises(type(native.value)):
        view.addons.molsysmt.where_is_attribute("not_an_attribute")


def test_collection_argument_remains_required_and_bound_primary_cannot_be_overridden(
    view,
):
    tools = view.addons.molsysmt
    with pytest.raises(Exception):
        tools.are_multiple_molecular_systems()
    target = view.molsys
    for name, args in [
        ("get_form", ()),
        ("is_a_molecular_system", ()),
        ("where_is_attribute", ("coordinates",)),
    ]:
        with pytest.raises(Exception):
            getattr(tools, name)(*args, molecular_system=target)
    assert view.molsys is target


def test_pending_native_data_is_read_without_projecting_it(view):
    tools = view.addons.molsysmt
    tools.remove(
        selection=[view.molsys.get_n_atoms() - 1], in_place=True, update_view=False
    )
    before = tools.get_sync_status()
    assert before["state"] == "pending"
    assert tools.get_form() == msm.get_form(view.molsys)
    assert tools.is_a_molecular_system() == msm.is_a_molecular_system(view.molsys)
    item, form = tools.where_is_attribute("coordinates")
    assert item is view.molsys and form == "molsysmt.MolSys"
    assert tools.are_multiple_molecular_systems([view.molsys]) is True
    assert tools.get_sync_status() == before


def test_cached_calls_follow_load_and_all_calls_reject_closed_view(view):
    tools = view.addons.molsysmt
    location = tools.where_is_attribute
    get_form = tools.get_form
    validate = tools.is_a_molecular_system
    explicit = tools.are_multiple_molecular_systems
    original = view.molsys
    with msv.demo["dialanine"] as other:
        view.load(other.molsys, mode="replace")
    item, form = location("coordinates")
    assert item is view.molsys and item is not original
    assert form == get_form() == "molsysmt.MolSys"
    assert validate() is True
    assert explicit([original]) is True
    view.addons.manager.disable("molsysmt")
    assert get_form() == "molsysmt.MolSys"
    view.close()
    for method, args in [
        (get_form, ()),
        (validate, ()),
        (location, ("coordinates",)),
        (explicit, ([original],)),
    ]:
        with pytest.raises(RuntimeError, match="closed view"):
            method(*args, skip_digestion=True)
