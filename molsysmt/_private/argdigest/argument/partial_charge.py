from molsysmt._private.smonitor import ArgumentError

functions_with_boolean = (
    "molsysmt.basic.get.get",
    "molsysmt.basic.compare.compare",
    "molsysmt.basic.iterator.__init__",
    "iterators.__init__",
)


def digest_partial_charge(partial_charge, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_boolean):
            if isinstance(partial_charge, bool):
                return partial_charge
        elif caller.startswith("molsysmt.form.") and caller.count(".to_") == 2:
            return partial_charge

        if caller == "molsysmt.basic.set.set" or caller.endswith(
            "set_partial_charge_to_atom"
        ):
            if partial_charge is None:
                return None
            import numpy as np

            from molsysmt import pyunitwizard as puw

            try:
                values = (
                    puw.get_value(partial_charge, to_unit="elementary_charge")
                    if puw.is_quantity(partial_charge)
                    else partial_charge
                )
                values = np.asarray(values)
                if (
                    values.ndim == 1
                    and values.dtype.kind in "iuf"
                    and np.isfinite(values).all()
                ):
                    return values.astype(np.float64, copy=False)
            except Exception:
                pass

    raise ArgumentError(
        "partial_charge", value=partial_charge, caller=caller, message=None
    )
