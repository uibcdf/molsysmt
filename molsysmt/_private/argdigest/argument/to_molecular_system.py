def digest_to_molecular_system(to_molecular_system, caller=None):

    from molsysmt._private.molecular_system_validation import validate_molecular_system_argument
    from .molecular_system import normalize_molecular_system_paths

    to_molecular_system = normalize_molecular_system_paths(to_molecular_system)

    return validate_molecular_system_argument(
        to_molecular_system,
        argument='to_molecular_system',
        caller=caller,
    )
