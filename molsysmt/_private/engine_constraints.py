"""Translate physical constraint choices at the optional engine boundary."""


def openmm_constraints(value, *, caller):
    """Resolve one policy without constructing a model or changing its owner."""
    from openmm import app

    from molsysmt._private.smonitor import ArgumentChoiceError

    policies = {
        "none": None,
        "noconstraints": None,
        "hbonds": app.HBonds,
        "allbonds": app.AllBonds,
        "hangles": app.HAngles,
    }
    if isinstance(value, str):
        key = value.lower().replace(" ", "").replace("_", "").replace("-", "")
        if key in policies:
            return policies[key]
    elif any(value is option for option in policies.values()):
        return value
    raise ArgumentChoiceError(
        "constraints",
        value,
        [None, "hbonds", "all bonds", "h angles"],
        caller=caller,
    )
