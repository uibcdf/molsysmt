"""Interpret explicit source vocabularies at the public conversion boundary."""

import inspect

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all

CALLER = "molsysmt.convert"


def source_reader_accepts_scheme(source_form, target):
    """Identify a direct reader that interprets the declaration during reading."""
    from molsysmt.form import _dict_modules, load_converter

    if not isinstance(source_form, str) or source_form in {
        "molsysmt.Topology",
        "molsysmt.MolSys",
    }:
        return False
    module = _dict_modules[source_form]
    route = module._convert_to.get(target)
    return (
        route is not None
        and "from_naming_scheme"
        in inspect.signature(load_converter(module, route)).parameters
    )


def _native_source(source, source_form, target, options, scheme, *, query=False):
    """Read only the required domain; keep source-reading options on that read."""
    from molsysmt.basic import convert
    from molsysmt.form import _dict_modules, load_converter

    if isinstance(source_form, str) and source_form in {
        "molsysmt.Topology",
        "molsysmt.MolSys",
    }:
        return source, dict(options)
    if isinstance(source_form, str) and source_form in {
        "string:amino_acids_1",
        "string:amino_acids_3",
    }:
        from molsysmt.form._sequence_topology import from_string

        # A caller declaration precedes the sequence constructor's default.
        # It never replaces an existing native or persisted declaration.
        return from_string(
            source,
            1 if source_form.endswith("_1") else 3,
            "all",
            "all",
            caller=CALLER,
            naming_scheme=scheme,
        ), dict(options)

    consumed = {}
    if isinstance(source_form, str):
        module = _dict_modules[source_form]
        route = module._convert_to.get(target) or module._convert_to.get(
            "molsysmt.MolSys"
        )
        if route is not None:
            converter = load_converter(module, route)
            parameters = inspect.signature(converter).parameters
            consumed = {
                key: value
                for key, value in options.items()
                if key in parameters
                and key not in {"atom_indices", "group_indices", "copy_if_all"}
            }
            if (
                query
                and "get_missing_bonds" in parameters
                and "get_missing_bonds" not in consumed
                and options.get("bond_inference_engine") is None
            ):
                # A name-only projection needs inventory, not engine-dependent
                # graph reconstruction. Preserve explicit inference requests.
                consumed["get_missing_bonds"] = False
            if "from_naming_scheme" in parameters:
                # Readers that interpret labels while constructing chemistry
                # need the declaration before their first reconstruction.
                native = converter(source, from_naming_scheme=scheme, **consumed)
                return native, {
                    key: value for key, value in options.items() if key not in consumed
                }
    native = convert(source, to_form=target, **consumed)
    return native, {key: value for key, value in options.items() if key not in consumed}


def convert_with_source_scheme(
    source, source_form, target, selection, structure_indices, syntax, scheme, options
):
    """Preserve source ownership while projecting or declaring selected groups."""
    from molsysmt.basic import convert, extract, select
    from molsysmt.native import MolSys, Topology

    from .name_resolution import check_source_scheme, group_positions, native_sequence

    query = target == "string:amino_acids_1"
    if not query and "atom_indices" in options and not is_all(selection):
        raise ArgumentError(
            "atom_indices",
            caller=CALLER,
            message="Use either selection or explicit atom_indices, not both.",
        )
    if not query and source_form in ("string:amino_acids_1", "string:amino_acids_3"):
        from molsysmt.form._sequence_topology import from_string

        remaining = dict(options)
        group_indices = remaining.pop("group_indices", "all")
        if not is_all(remaining.pop("atom_indices", "all")):
            raise ArgumentError(
                "atom_indices",
                caller=CALLER,
                message="A group-only inventory has no atomic selection axis; use group_indices.",
            )
        if not is_all(selection):
            if not is_all(group_indices):
                raise ArgumentError(
                    "group_indices",
                    caller=CALLER,
                    message="Use either selection or explicit group_indices, not both.",
                )
            group_indices = select(
                source, selection=selection, element="group", syntax=syntax
            )
        # Text constructs new slots, including repetitions; its temporary native
        # representation is not an existing inventory with source group IDs.
        native = from_string(
            source,
            1 if source_form.endswith("_1") else 3,
            group_indices,
            structure_indices,
            caller=CALLER,
            naming_scheme=scheme,
        )
        return convert(native, to_form=target, **remaining)
    reduced_target = (
        "molsysmt.Topology"
        if query or target in {"molsysmt.Topology", "molsysmt.TopologyDict"}
        else "molsysmt.MolSys"
    )
    native, remaining = _native_source(
        source, source_form, reduced_target, options, scheme, query=query
    )
    topology = (
        native if isinstance(native, Topology) else getattr(native, "topology", None)
    )
    if topology is None:
        raise ArgumentError(
            "from_naming_scheme",
            value=scheme,
            caller=CALLER,
            message="A source naming declaration requires a topology with group names.",
        )
    if not query and "atom_indices" in remaining:
        if not is_all(selection):
            raise ArgumentError(
                "atom_indices",
                caller=CALLER,
                message="Use either selection or explicit atom_indices, not both.",
            )
        atom_indices = remaining.pop("atom_indices")
        if topology.n_atoms == 0 and not is_all(atom_indices):
            raise ArgumentError(
                "atom_indices",
                caller=CALLER,
                message="A group-only inventory has no atomic selection axis; use group_indices.",
            )
        selection = atom_indices
    group_indices = remaining.pop("group_indices", "all")
    if not is_all(group_indices) and not is_all(selection):
        raise ArgumentError(
            "group_indices",
            value=group_indices,
            caller=CALLER,
            message="Use either selection or explicit group_indices, not both.",
        )
    if not is_all(selection):
        if query or topology.n_atoms == 0:
            group_indices = select(
                native, selection=selection, element="group", syntax=syntax
            )
        else:
            atoms = select(native, selection=selection, element="atom", syntax=syntax)
            group_indices = (
                topology.atoms.iloc[atoms]["group_index"].dropna().unique().tolist()
            )
    positions = group_positions(topology, group_indices, caller=CALLER)
    codes = check_source_scheme(topology, positions, scheme, caller=CALLER)
    if query:
        if remaining:
            raise ArgumentError(
                "from_naming_scheme",
                caller=CALLER,
                message=f"Unsupported sequence conversion options: {sorted(remaining)}.",
            )
        letters = native_sequence(
            topology, positions, caller=CALLER, from_naming_scheme=scheme
        )
        if source_form == "string:amino_acids_1":
            from molsysmt.form._sequence_selection import extract

            return extract(source, 1, "all", positions, "all", caller=CALLER)
        if source_form == "string:amino_acids_3" and not letters:
            return "amino_acids_1:"
        if source_form == "file:fasta":
            # Record occurrences are separate molecules, including empty ones.
            # One native interpretation/credit batch serves the complete query.
            records = [[] for _ in range(topology.n_molecules)]
            owners = topology.groups["molecule_index"].to_numpy()[positions]
            for letter, owner in zip(letters, owners, strict=True):
                records[int(owner)].append(letter)
            return ["".join(record) for record in records]
        return letters

    if topology.n_atoms and not is_all(group_indices) and is_all(selection):
        raise ArgumentError(
            "group_indices",
            caller=CALLER,
            message="Explicit group_indices with from_naming_scheme require a one-letter query or group-only inventory; use atom selection for an atomic molecular conversion.",
        )
    independent = False
    if topology.n_atoms == 0 and not is_all(group_indices):
        # Let the owner enforce unique inventory positions before assignment.
        native = extract(
            native,
            selection=positions,
            element="group",
            structure_indices=structure_indices,
            copy_if_all=False,
        )
        topology = native if isinstance(native, Topology) else native.topology
        positions = group_positions(topology, "all", caller=CALLER)
        codes = check_source_scheme(topology, positions, scheme, caller=CALLER)
        selection = structure_indices = "all"
        independent = True
    if len(positions) and (codes is None or (codes[positions] == 0).any()):
        # The copy owns stable/chemical domains; MolSys defers coordinate blocks.
        # A query above needs neither this snapshot nor any coordinate access.
        if not independent:
            native = (
                native.copy(deep=False, skip_digestion=True)
                if isinstance(native, MolSys)
                else native.copy(skip_digestion=True)
            )
        topology = native if isinstance(native, Topology) else native.topology
        topology.set_group_naming_schemes(scheme, group_indices=positions)
    return convert(
        native,
        to_form=target,
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        **remaining,
    )
