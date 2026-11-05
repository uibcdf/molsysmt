"""Audit group-name declarations independently of chemical assignments."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all

# These routes store the declaration and its versioned vocabulary. Other targets
# may retain labels, but label equality does not preserve their declared meaning.
PRESERVING_TARGETS = frozenset(
    {
        "molsysmt.Topology",
        "molsysmt.MolSys",
        "molsysmt.MolSysBuilder",
        "molsysmt.TopologyDict",
        "molsysmt.MolSysDict",
        "file:h5msm",
    }
)


def audit(
    source,
    source_form,
    target_form,
    selection,
    structure_indices,
    syntax,
    options,
    scheme,
):
    """Inspect selected declarations without changing a source or writing a target."""
    from molsysmt._private.name_resolution import (
        check_source_scheme,
        group_positions,
        stored_topology,
    )
    from molsysmt.basic import select
    from molsysmt.basic.conversion_report import ConversionIssue
    from molsysmt.native import Topology

    topology = stored_topology(
        source, caller="molsysmt.get_conversion_report", required=False
    )
    if topology is None and scheme is not None:
        from molsysmt._private.naming_conversion import _native_source
        from molsysmt.form import _dict_modules

        forms = source_form if isinstance(source_form, (tuple, list)) else [source_form]
        reduced_target = (
            "molsysmt.Topology"
            if any(
                _dict_modules[form].attributes.get("group_name", False)
                for form in forms
            )
            else "molsysmt.MolSys"
        )
        native, _ = _native_source(source, source_form, reduced_target, options, scheme)
        topology = (
            native
            if isinstance(native, Topology)
            else getattr(native, "topology", None)
        )
        if topology is None:
            raise ArgumentError(
                "from_naming_scheme",
                value=scheme,
                caller="molsysmt.get_conversion_report",
                message="Source naming interpretation requires a topology with group names.",
            )
    if topology is None:
        return [], False
    from molsysmt.native._group_naming import stored

    if scheme is None and stored(topology) is None:
        return [], False
    group_indices = options.get("group_indices", "all")
    atom_indices = options.get("atom_indices", "all")
    if not is_all(group_indices) and (
        not is_all(selection) or not is_all(atom_indices)
    ):
        raise ArgumentError(
            "group_indices",
            caller="molsysmt.get_conversion_report",
            message="Use either group positions or an atom selection, not both.",
        )
    if not is_all(atom_indices):
        if not is_all(selection):
            raise ArgumentError(
                "atom_indices",
                caller="molsysmt.get_conversion_report",
                message="Use either selection or explicit atom positions, not both.",
            )
        selection = atom_indices
    if not is_all(selection):
        if topology.n_atoms == 0 or target_form in {
            "string:amino_acids_1",
            "string:amino_acids_3",
        }:
            group_indices = select(
                topology, element="group", selection=selection, syntax=syntax
            )
        else:
            positions = select(
                source, element="atom", selection=selection, syntax=syntax
            )
            group_indices = (
                topology.atoms.iloc[positions]["group_index"].dropna().unique().tolist()
            )
    positions = group_positions(
        topology, group_indices, caller="molsysmt.get_conversion_report"
    )
    codes = check_source_scheme(
        topology, positions, scheme, caller="molsysmt.get_conversion_report"
    )
    present = bool(len(positions)) and (
        scheme is not None or codes is not None and np.any(codes[positions])
    )
    if (
        present
        and scheme is not None
        and target_form in ANALYSIS_TARGETS
        and (codes is None or (codes[positions] == 0).any())
    ):
        names, evaluated = analysis_metadata(source, structure_indices, coverage=True)
        if evaluated:
            return [
                ConversionIssue(
                    attribute="interactions",
                    kind="invalidation",
                    scope="interactions",
                    reason=f"Adding source naming declarations invalidates selected evaluated coverage in named analyses {list(names)!r} on the independent result; the source remains unchanged.",
                )
            ], True
    if present and target_form not in PRESERVING_TARGETS:
        return [
            ConversionIssue(
                attribute="group_naming_schemes",
                kind="unsupported",
                scope="topology",
                reason=f"{target_form} does not preserve the selected group-name declarations. Keeping labels alone does not retain their source vocabulary; use native inventory, typed dictionaries or H5MSM for that metadata.",
            )
        ], True
    return [], bool(present)


ANALYSIS_TARGETS = frozenset({"molsysmt.MolSys", "molsysmt.MolSysDict", "file:h5msm"})


def analysis_metadata(source, structure_indices="all", *, coverage=False):
    """Inspect names and optional coverage without decoding occurrence columns."""
    from molsysmt.native import MolSys, MolSysDict

    if isinstance(source, MolSys):
        records = source.interactions
        indices = (result.evaluated_structure_indices for result in records.values())
    elif isinstance(source, MolSysDict):
        records = source.data.get("interactions", {})
        if not isinstance(records, dict):
            raise ValueError("Invalid named interaction metadata.")

        def evaluated():
            from molsysmt.form._serialization import decode_array

            for record in records.values():
                leaves = [
                    entry["array"]
                    for entry in record.get("arrays", [])
                    if entry.get("path") == ["evaluated_structure_indices"]
                ]
                if len(leaves) != 1:
                    raise ValueError("Invalid named interaction coverage metadata.")
                yield decode_array(leaves[0])

        indices = evaluated()
    else:
        return (), False
    names = tuple(records)
    if not coverage:
        return names, False

    def relevant(values):
        if is_all(structure_indices):
            return bool(np.asarray(values).size)
        return bool(np.isin(values, np.atleast_1d(structure_indices)).any())

    return names, any(relevant(values) for values in indices)


def audit_analysis_projection(source, target_form):
    """Report named analyses omitted by representations without their domain."""
    from molsysmt.basic.conversion_report import ConversionIssue

    if target_form in ANALYSIS_TARGETS:
        return []
    names, _ = analysis_metadata(source)
    if not names:
        return []
    return [
        ConversionIssue(
            attribute="interactions",
            scope="interactions",
            reason=f"{target_form} has no supported storage for the named interaction analyses {list(names)!r}.",
        )
    ]
