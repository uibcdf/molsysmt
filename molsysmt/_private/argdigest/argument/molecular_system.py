from os import PathLike
from pathlib import Path

from argdigest.core.caller import caller_matches


def normalize_molecular_system_paths(molecular_system):
    """Normalize path-like molecular-system inputs without changing container intent."""

    if isinstance(molecular_system, PathLike):
        return str(Path(molecular_system).absolute())
    if isinstance(molecular_system, list):
        return [normalize_molecular_system_paths(item) for item in molecular_system]
    if isinstance(molecular_system, tuple):
        return tuple(
            normalize_molecular_system_paths(item) for item in molecular_system
        )
    return molecular_system


def digest_molecular_system(molecular_system, caller=None):
    """Check if an object is a molecular system.

    Parameters
    ----------
    molecular_system : Any
        The molecular system object to be checked.
    caller: str, optional
        Name of the function or method that is being digested.

    Returns
    -------
    molecular_system : Any
        The molecular system object.

    Raises
    ------
    ArgumentError
        If the given object has a genuinely unsupported form.
    MolecularSystemVerificationError
        If form discovery or complementary-axis verification cannot finish.
        The original operational exception remains in the Python cause chain.
    """
    from molsysmt._private.molecular_system_validation import (
        assess_molecular_system,
        validate_molecular_system_argument,
    )
    from molsysmt.basic import are_multiple_molecular_systems, merge

    molecular_system = normalize_molecular_system_paths(molecular_system)

    if molecular_system is None and caller_matches(caller, "editable"):
        return None
    if molecular_system is None and caller == "molsysmt.basic.view.view":
        return None

    if caller == "molsysmt.basic.view.view":
        assessment = assess_molecular_system(molecular_system)
        if assessment.is_valid_single_system:
            return molecular_system
        elif are_multiple_molecular_systems(molecular_system):
            return merge(molecular_system, to_form="molsysmt.MolSys")

    return validate_molecular_system_argument(
        molecular_system,
        argument="molecular_system",
        caller=caller,
    )
