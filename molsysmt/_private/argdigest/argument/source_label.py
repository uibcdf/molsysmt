from molsysmt._private.smonitor import ArgumentError


def digest_source_label(source_label, caller=None):
    if source_label is None or isinstance(source_label, str):
        return source_label
    raise ArgumentError("source_label", value=source_label, caller=caller)
