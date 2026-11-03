"""Internal chemical-state resolution helpers for public orchestration APIs."""

from contextlib import ExitStack
from functools import wraps
from inspect import signature


def _native_chemical_collections(molecular_system):
    """Yield chemical owners once, without requiring a stable Topology domain."""

    from molsysmt.native import (
        ChemicalStates,
        ChemicalStatesDict,
        MolSys,
        MolSysBuilder,
    )

    pending = [molecular_system]
    seen = set()
    while pending:
        item = pending.pop()
        if isinstance(item, (list, tuple)):
            pending.extend(item)
            continue
        if isinstance(item, (MolSys, MolSysBuilder)):
            collection = item.chemical_states
        elif isinstance(item, (ChemicalStates, ChemicalStatesDict)):
            collection = item
        else:
            continue
        if collection is not None and id(collection) not in seen:
            seen.add(id(collection))
            yield collection


def _native_molsystems(molecular_system):
    """Yield distinct native MolSys objects contained in an input."""

    from molsysmt.native import MolSys, MolSysBuilder

    pending = [molecular_system]
    seen = set()
    while pending:
        item = pending.pop()
        if isinstance(item, (list, tuple)):
            pending.extend(item)
        elif isinstance(item, (MolSys, MolSysBuilder)) and id(item) not in seen:
            seen.add(id(item))
            yield item if isinstance(item, MolSys) else item._query_view()


def resolve_chemical_state(function=None, *, convert_if_missing=False):
    """Scope native state-dependent access to the public ``chemical_state`` argument."""

    if function is None:
        return lambda target: resolve_chemical_state(
            target, convert_if_missing=convert_if_missing
        )

    function_signature = signature(function)

    @wraps(function)
    def wrapped(*args, **kwargs):
        arguments = function_signature.bind_partial(*args, **kwargs)
        chemical_state = arguments.arguments.get("chemical_state", "reference")
        if chemical_state == "reference":
            return function(*args, **kwargs)

        molecular_system = arguments.arguments.get(
            "molecular_system", arguments.arguments.get("self")
        )
        from molsysmt._private.h5msm import maybe_read_modular_h5msm

        native_system = maybe_read_modular_h5msm(molecular_system)
        from molsysmt.native import MolSysDict

        if isinstance(native_system, MolSysDict):
            from molsysmt.basic import convert

            native_system = convert(native_system, to_form="molsysmt.MolSys")
        if native_system is not molecular_system:
            argument_name = (
                "molecular_system"
                if "molecular_system" in function_signature.parameters
                else "self"
            )
            arguments.arguments[argument_name] = native_system
            args, kwargs = arguments.args, arguments.kwargs
            molecular_system = native_system
        if convert_if_missing and not list(
            _native_chemical_collections(molecular_system)
        ):
            from molsysmt.basic import convert

            molecular_system = convert(
                molecular_system, to_form="molsysmt.MolSys", copy_if_all=False
            )
            arguments.arguments["molecular_system"] = molecular_system
            args, kwargs = arguments.args, arguments.kwargs
        if chemical_state == "structure":
            molsystems = list(_native_molsystems(molecular_system))
            if len(molsystems) != 1:
                from molsysmt._private.smonitor import ArgumentError

                raise ArgumentError(
                    argument="chemical_state",
                    value=chemical_state,
                    caller=function.__module__ + "." + function.__name__,
                )
            chemical_state = molsystems[0]._resolve_structure_chemical_state_index(
                arguments.arguments.get(
                    "structure_indices",
                    arguments.arguments.get("structure_index", "all"),
                )
            )

        collections = list(_native_chemical_collections(molecular_system))
        if not collections:
            from molsysmt._private.smonitor import ArgumentError

            raise ArgumentError(
                argument="chemical_state",
                value=chemical_state,
                caller=function.__module__ + "." + function.__name__,
            )

        with ExitStack() as stack:
            for collection in collections:
                stack.enter_context(collection._using_chemical_state(chemical_state))
            return function(*args, **kwargs)

    return wrapped
