from molsysmt._private.smonitor import ArgumentError


def digest_n_cations(n_cations, caller=None):
    if caller in {"molsysmt.build.solvate.solvate", "molsysmt.build.add_ions.add_ions"}:
        from molsysmt.build._ion_replacement import nonnegative_integer

        return nonnegative_integer(
            n_cations, "n_cations", neutralize=True, caller=caller
        )

    raise ArgumentError("n_cations", value=n_cations, caller=caller, message=None)
