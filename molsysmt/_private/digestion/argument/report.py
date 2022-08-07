from molsysmt._private.exceptions import ArgumentError

def digest_report(report, caller=None):


    if caller == 'molsysmt.basic.compare.compare.compare':

        if isinstance(report, bool):
            return report

    raise ArgumentError('report', value=report, caller=caller, message=None)
