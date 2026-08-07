from molsysmt._private.smonitor import ArgumentError


def digest_return_report(return_report, caller=None):
    if isinstance(return_report, bool):
        return return_report

    raise ArgumentError(
        "return_report",
        value=return_report,
        caller=caller,
        message=None,
    )
