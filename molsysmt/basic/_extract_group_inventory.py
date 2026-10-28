"""Resolve a partial hierarchy at the public extraction boundary."""

from molsysmt._private.variables import is_all


def extract_inventory(
    molecular_system,
    form,
    selection,
    structure_indices,
    element,
    syntax,
    copy_if_all,
    to_form,
):
    from molsysmt.basic import convert, get, has_attribute, select
    from molsysmt.native import MolSys, Topology
    from molsysmt.native._extract_group_inventory import extract

    if isinstance(molecular_system, (MolSys, Topology)):
        native = molecular_system
    else:
        from molsysmt.form import _dict_modules

        if (
            element is None
            and to_form is None
            and _dict_modules[form].form_type == "string"
        ):
            return None
        if has_attribute(molecular_system, "n_atoms", include_none=True):
            n_atoms = get(molecular_system, n_atoms=True)
            if n_atoms is None or n_atoms > 0:
                return None
        elif not has_attribute(molecular_system, "group_index", include_none=True):
            return None
        targets = _dict_modules[form]._convert_to
        if "molsysmt.MolSys" not in targets and "molsysmt.Topology" not in targets:
            return None
        target = (
            "molsysmt.MolSys"
            if "molsysmt.MolSys" in _dict_modules[form]._convert_to
            else "molsysmt.Topology"
        )
        native = convert(molecular_system, to_form=target)
    topology = native.topology if isinstance(native, MolSys) else native
    if (
        topology is None
        or topology.n_atoms
        or element not in (None, "group", "chain", "molecule", "entity")
    ):
        return None
    element = "group" if element is None else element
    indices = (
        "all"
        if is_all(selection)
        else select(native, selection=selection, element=element, syntax=syntax)
    )
    subset = extract(topology, indices, element, copy_if_all=copy_if_all)
    if isinstance(native, MolSys):
        output = native.extract(
            structure_indices=structure_indices,
            copy_if_all=copy_if_all or not is_all(indices),
        )
        output.topology = subset
    else:
        output = subset
    target = to_form or form
    if target in ("molsysmt.MolSys", "molsysmt.Topology"):
        if target == "molsysmt.MolSys" and isinstance(output, MolSys):
            return output
        if target == "molsysmt.Topology":
            return subset
    return convert(output, to_form=target)
