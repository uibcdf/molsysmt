"""Resolve atom selections and mutation specifications before engine edits."""

import numpy as np

from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    ArgumentError,
    StructuralInconsistencyError,
)

_CALLER = "molsysmt.build.mutate"


def resolve_mutation_targets(molecular_system, mutations, keys, selection, syntax):
    """Return deterministic (group index, target name) pairs in the source space."""
    from molsysmt.basic import get, select

    if selection is None:
        raise ArgumentError("selection", caller=_CALLER)
    if isinstance(selection, str):
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    else:
        # Numeric selectors have the same axis irrespective of string syntax.
        array = np.asarray(selection)
        if array.dtype.kind == "b":
            atom_indices = select(molecular_system, mask=selection)
        else:
            atom_indices = select(molecular_system, selection=selection)
    enabled_groups = set(
        get(molecular_system, selection=atom_indices, group_index=True)
    )
    group_names, group_ids = get(
        molecular_system, element="group", group_name=True, group_id=True
    )
    n_groups = len(group_names)
    targets = {}

    def add_target(index, name, old_name=None):
        if index not in enabled_groups:
            return
        if (
            old_name is not None
            and group_names[index].casefold() != old_name.casefold()
        ):
            raise ArgumentChoiceError(
                "mutations",
                old_name,
                [group_names[index]],
                caller=_CALLER,
                message=f"Group {index} has name {group_names[index]!r}, not {old_name!r}.",
            )
        name = name.upper()
        if index in targets and targets[index] != name:
            raise ArgumentError(
                "mutations",
                caller=_CALLER,
                message=f"Conflicting mutation targets for group index {index}.",
            )
        targets[index] = name

    def by_id(label):
        matches = [
            index for index, value in enumerate(group_ids) if str(value) == label
        ]
        if not matches:
            raise ArgumentError(
                "mutations",
                caller=_CALLER,
                message=f"No group has group_id {label!r}.",
            )
        selected = [index for index in matches if index in enabled_groups]
        if len(selected) > 1:
            raise StructuralInconsistencyError(
                reason=f"Multiple selected groups have group_id {label!r}; narrow selection.",
                caller=_CALLER,
            )
        return selected

    if isinstance(mutations, str):
        mutations = [mutations]
    if isinstance(mutations, dict):
        for key, name in mutations.items():
            _validate_name(name)
            if keys == "group_index":
                if (
                    isinstance(key, (bool, np.bool_))
                    or not isinstance(key, (int, np.integer))
                    or not 0 <= key < n_groups
                ):
                    raise ArgumentError(
                        "mutations",
                        caller=_CALLER,
                        message=f"Mutation group indices must be integers in [0, {n_groups}).",
                    )
                add_target(int(key), name)
            elif keys == "group_id":
                if isinstance(key, (bool, np.bool_)) or not isinstance(
                    key, (str, int, np.integer)
                ):
                    raise ArgumentError(
                        "mutations",
                        caller=_CALLER,
                        message="Group IDs must be string labels or integers converted to strings.",
                    )
                for index in by_id(str(key)):
                    add_target(index, name)
            elif keys == "group_name":
                _validate_name(key)
                for index, actual_name in enumerate(group_names):
                    if actual_name.casefold() == key.casefold():
                        add_target(index, name)
            else:
                raise ArgumentError("keys", value=keys, caller=_CALLER)
    elif isinstance(mutations, (list, tuple)):
        for specification in mutations:
            if not isinstance(specification, str) or specification.count("-") < 2:
                raise ArgumentError(
                    "mutations",
                    caller=_CALLER,
                    message="Mutation strings must have source-name, group-ID and target-name separated by hyphens.",
                )
            old_name, remainder = specification.split("-", 1)
            label, name = remainder.rsplit("-", 1)
            _validate_name(old_name)
            _validate_name(name)
            if not label:
                raise ArgumentError(
                    "mutations",
                    caller=_CALLER,
                    message="Mutation strings require a nonempty group ID.",
                )
            for index in by_id(label):
                add_target(index, name, old_name)
    else:
        raise ArgumentError("mutations", caller=_CALLER)
    return sorted(targets.items())


def _validate_name(name):
    if not isinstance(name, str) or not name or name != name.strip() or "-" in name:
        raise ArgumentError(
            "mutations",
            caller=_CALLER,
            message="Mutation group names must be nonempty strings without surrounding whitespace or hyphens.",
        )


def pdbfixer_mutation_arguments(fixer, targets):
    """Refuse provider addresses that could select a different source group."""
    groups = list(fixer.topology.residues())
    arguments = []
    for index, name in targets:
        group = groups[index]
        addressed = [other for other in groups if other.chain.id == group.chain.id]
        try:
            labels = [int(other.id) for other in addressed]
        except (TypeError, ValueError) as error:
            raise ArgumentError(
                "mutations",
                caller=_CALLER,
                message="PDBFixer mutation requires integer group IDs in each addressed chain; use the native engine for other labels.",
            ) from error
        if len(set(labels)) != len(labels):
            raise StructuralInconsistencyError(
                reason="PDBFixer mutation requires unique integer group IDs across chains sharing the addressed chain ID.",
                caller=_CALLER,
            )
        if int(group.id) < 0:
            raise ArgumentError(
                "mutations",
                caller=_CALLER,
                message="PDBFixer mutation strings cannot address negative group IDs.",
            )
        arguments.append((f"{group.name}-{int(group.id)}-{name}", group.chain.id))
    return arguments
