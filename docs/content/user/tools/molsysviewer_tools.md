(user-tools-molsysviewer)=
# MolSysViewer tools addon

Use MolSysMT tools on the molecular system already loaded in your view. The
expert API follows MolSysMT's module/function hierarchy, with `view.molsys`
supplied as the primary input.

## Availability

The experimental source implementation provides six queries under
`view.addons.molsysmt.basic`: `get`, `select`, `info`, `get_attributes`,
`has_attribute` and `get_label`, plus independent extraction with `extract`
and managed native removal with `remove`.
Their root aliases are also available, such as `view.addons.molsysmt.get`.
Other scientific modules, editing families and graphical task panels
are still being implemented. This is not a complete MolSysMT mirror
or a claim that the currently published package pair contains these tools.

Install compatible versions of both components. MolSysMT supplies the
integration; MolSysViewer discovers its declared entry point automatically.
Source checkouts need current generated distribution metadata as well as an
editable installation after an entry-point change. No manual registration is needed in a correctly installed compatible
environment. Ordinary MolSysMT import and the core visualization backend work
independently of this optional interface.

## Querying the current system

```python
import molsysviewer as msv

with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    count = tools.basic.get(n_atoms=True)
    atoms = tools.basic.select(selection="atom_type=='N'")
    coordinates = tools.basic.get(
        element="atom", selection=atoms,
        structure_indices=[2, 0], coordinates=True,
    )
    summary = tools.basic.info(output_type="dictionary")
```

Coordinates retain the native physical quantity and structure order; the
standard MolSysMT length unit is nm. Scientific choices, defaults, result types,
errors and mutable-result ownership follow the native function. These wrappers
add no whole-trajectory copy or scene update. Native calculation/cache behavior
is unchanged; for example, `get_missing_bonds` retains its documented meaning.

| Bound tool | Native parameter and result reference |
| --- | --- |
| `tools.basic.get(...)` | {doc}`basic/get` |
| `tools.basic.select(...)` | {doc}`basic/select` |
| `tools.basic.info(...)` | {doc}`basic/info` |
| `tools.basic.get_attributes(...)` | {doc}`basic/get_attributes` |
| `tools.basic.has_attribute(...)` | {doc}`basic/has_attribute` |
| `tools.basic.get_label(...)` | {doc}`basic/get_label` |

The bound methods omit the primary `molecular_system` argument. You cannot
override it with another system. Inspect a signature or call `help` on the
method for the remaining native parameters. `skip_digestion` keeps the native
trusted-call contract; it does not bypass view lifetime checks.

## Extracting a molecular subset

```python
with msv.demo["pentalanine"] as view:
    subset = view.addons.molsysmt.basic.extract(
        selection=[0, 2, 4], structure_indices=[2, 0, 2],
        to_form="molsysmt.MolSys",
    )
```

This returns the native molecular result and leaves the view unchanged. Structure
order and repetitions follow {doc}`basic/extract`, as do output formats/files,
units, attached-analysis projection and the `copy_if_all` ownership policy.
An unrestricted `copy_if_all=False` call may retain native shared/live-reference
behavior; the addon does not add a defensive copy or observe later direct writes.
`view.extract(...)` is a separate operation that returns a new view with migrated
scene state. Neither method implicitly adopts its result into the source view.

## Removing atoms or structures

`remove` preserves {doc}`basic/remove`: `in_place=False` is the native default
and returns an independent molecular system. It does not replace `view.molsys`.
To edit the actual bound system and update its scene:

```python
with msv.demo["pentalanine"] as view:
    tools = view.addons.molsysmt
    tools.basic.remove(selection=[0], in_place=True)
    tools.basic.remove(structure_indices=[1], in_place=True, update_view=False)
    status = tools.get_sync_status()  # pending: science is already complete
    tools.sync_view()                # update the scene, not the science
```

Successful in-place removal returns native `None`. The keyword-only
`update_view=True` default synchronizes immediately; False defers only visual
reconciliation. Compatible deferred removals compose their atom/structure maps.
Queries read the current edited MolSys, while scene actions using old indices
are blocked until synchronization. Live windows display an Update view action.

The initial receiver supports retained nonempty atom/structure axes. Removing
every atom or structure in place is rejected before scientific execution; use
`in_place=False` for independent empty outputs. Surviving analyses follow native
extraction/projection semantics and retain their original evaluated scope: they
are not new calculations. Regions, saved/active atom selections, shapes and
structure-bound scene data follow the receiving host's map policies. Textual
region/selection queries are reevaluated; explicit atom lists are remapped.

### A completed edit whose display update fails

A scene synchronization error does not mean the removal failed. The host raises
`molsysviewer.system_edits.SystemEditSyncError` with `science_completed=True`,
`operation_id` and `scientific_result` (native None for this removal). Its cause
identifies the projection failure. Call `tools.sync_view()` to retry; do not
repeat the removal. The facade does not permanently retain large results.

If a scientific exception may have left partial writes, status is `uncertain`;
unchanged counts do not certify correspondence. Explicit recovery through
`view.addons.manager.system_edits.replace(molecular_system)` discards pending
scene reconciliation and loads a replacement. This is not scientific Undo and
does not revert caller-held references to the old edited system. Ordinary
`view.load` cannot silently discard unresolved managed edits.

## Reusing tool references

A cached `tools` object or method resolves the current `view.molsys` when each
call begins. After `view.load(..., mode="replace")`, later queries use the
replacement system. The facade does not keep a second authoritative MolSys.
Each view has its own binding. Disabling the addon's graphical activation does
not disable expert Python queries. Closing the view makes bound queries fail;
an empty view must first load a molecular system.

Results are native scientific values. These queries do not create scene objects
or attach every result automatically. Use the visual owners in MolSysViewer for
regions, selections, measurements or Interactions. General direct edits made
with MolSysMT or through returned live references retain explicit reconciliation
responsibilities. Only admitted addon writers coordinate their edits; there is
no observer for arbitrary external writes.

## Host and author documentation

MolSysViewer documents discovery, activation, configuration, lifecycle, its
addon catalogue and how to create an addon in its
[addon guide](https://www.uibcdf.org/molsysviewer/content/user/introduction/addons.html).
This MolSysMT guide owns the capabilities and use of the MolSysMT tools addon.
