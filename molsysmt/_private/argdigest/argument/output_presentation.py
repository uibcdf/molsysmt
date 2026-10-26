from molsysmt._private.smonitor import ArgumentError


def digest_output_presentation(output_presentation, caller=None):
    if output_presentation is None or isinstance(output_presentation, dict):
        return output_presentation
    raise ArgumentError("output_presentation", caller=caller)
