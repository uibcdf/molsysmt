"""Internal chemical-state resolution helpers for public orchestration APIs."""

from contextlib import ExitStack
from functools import wraps
from inspect import signature


def _native_chemical_collections(molecular_system):
    """Yield chemical owners once, without requiring a stable Topology domain."""

    from molsysmt.native import ChemicalStates, MolSys, Topology

    pending = [molecular_system]
    seen = set()
    while pending:
        item = pending.pop()
        if isinstance(item, (list, tuple)):
            pending.extend(item)
            continue
        if isinstance(item, MolSys):
            collection = item.chemical_states
        elif isinstance(item, ChemicalStates):
            collection = item
        elif isinstance(item, Topology):
            # Transitional branch callers retain their existing route until C6
            # removes Topology's chemical facade and these producers together.
            collection = item._chemical_states_domain
        else:
            continue
        if collection is not None and id(collection) not in seen:
            seen.add(id(collection))
            yield collection


def _native_molsystems(molecular_system):
    """Yield distinct native MolSys objects contained in an input."""

    from molsysmt.native import MolSys

    pending = [molecular_system]
    seen = set()
    while pending:
        item = pending.pop()
        if isinstance(item, (list, tuple)):
            pending.extend(item)
        elif isinstance(item, MolSys) and id(item) not in seen:
            seen.add(id(item))
            yield item


def resolve_chemical_state(function):
    """Scope native state-dependent access to the public ``chemical_state`` argument."""

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
        if native_system is not molecular_system:
            arguments.arguments["molecular_system"] = native_system
            args, kwargs = arguments.args, arguments.kwargs
            molecular_system = native_system
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
                arguments.arguments.get("structure_indices", "all")
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
