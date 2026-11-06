from molsysmt._private.smonitor import ArgumentError


def digest_n_anions(n_anions, caller=None):
    if caller in {"molsysmt.build.solvate.solvate", "molsysmt.build.add_ions.add_ions"}:
        from molsysmt.build._ion_replacement import nonnegative_integer

        return nonnegative_integer(n_anions, "n_anions", neutralize=True, caller=caller)

    raise ArgumentError("n_anions", value=n_anions, caller=caller, message=None)
