"""Internal chemical-state resolution helpers for public orchestration APIs."""

from contextlib import ExitStack
from functools import wraps
from inspect import signature


def _native_topologies(molecular_system):
    """Yield distinct native topologies contained in a molecular-system input."""

    from molsysmt.native import MolSys, Topology

    pending = [molecular_system]
    seen = set()
    while pending:
        item = pending.pop()
        if isinstance(item, (list, tuple)):
            pending.extend(item)
        elif isinstance(item, MolSys):
            topology = item.topology
            if id(topology) not in seen:
                seen.add(id(topology))
                yield topology
        elif isinstance(item, Topology) and id(item) not in seen:
            seen.add(id(item))
            yield item


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
        chemical_state = arguments.arguments.get('chemical_state', 'reference')
        if chemical_state == 'reference':
            return function(*args, **kwargs)

        molecular_system = arguments.arguments.get('molecular_system')
        if chemical_state == 'structure':
            molsystems = list(_native_molsystems(molecular_system))
            if len(molsystems) != 1:
                from molsysmt._private.smonitor import ArgumentError

                raise ArgumentError(
                    argument='chemical_state',
                    value=chemical_state,
                    caller=function.__module__ + '.' + function.__name__,
                )
            chemical_state = molsystems[0]._resolve_structure_chemical_state_index(
                arguments.arguments.get('structure_indices', 'all')
            )

        topologies = list(_native_topologies(molecular_system))
        if not topologies:
            from molsysmt._private.smonitor import ArgumentError

            raise ArgumentError(
                argument='chemical_state',
                value=chemical_state,
                caller=function.__module__ + '.' + function.__name__,
            )

        with ExitStack() as stack:
            for topology in topologies:
                stack.enter_context(topology._using_chemical_state(chemical_state))
            return function(*args, **kwargs)

    return wrapped
