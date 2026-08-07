from molsysmt._private.smonitor import ArgumentError

def digest_int_precision(int_precision, caller=None):

    if isinstance(int_precision, str):

        if caller is not None and (
            caller.endswith('to_file_h5msm') or caller == 'molsysmt.basic.convert.convert'
        ):
            if int_precision in ['single', 'double']:
                return int_precision

    raise ArgumentError('int_precision', value=int_precision, caller=caller, message=None)
