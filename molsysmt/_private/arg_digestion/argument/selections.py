from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all
from argdigest.core.caller import caller_matches


def digest_selections(selections, syntax="MolSysMT", molecular_systems=None, caller=None):

    from .selection import digest_selection

    if molecular_systems is not None and caller_matches(
        caller,
        'merge',
        'concatenate_structures',
    ):
        from molsysmt._private.smonitor import ArgumentLengthError

        n_molecular_systems = len(molecular_systems)
        if isinstance(selections, (list, tuple)):
            if len(selections) != n_molecular_systems:
                raise ArgumentLengthError(
                    argument='selections',
                    expected=n_molecular_systems,
                    actual=len(selections),
                    caller=caller,
                )
            return [
                digest_selection(selection, syntax=syntax, caller=caller)
                for selection in selections
            ]

        return [
            digest_selection(selections, syntax=syntax, caller=caller)
            for _ in range(n_molecular_systems)
        ]

    if isinstance(selections, (list, tuple)):
        return [digest_selection(ii, syntax=syntax, caller=caller) for ii in selections]
    elif is_all(selections):
        return selections

    raise ArgumentError('selections', value=selections, caller=caller)
