from molsysmt._private.smonitor import ArgumentError


def digest_box_volume(box_volume, caller=None):

    if caller in {"molsysmt.basic.get.get", "molsysmt.basic.compare.compare"}:
        if isinstance(box_volume, bool):
            return box_volume

    raise ArgumentError("box_volume", value=box_volume, caller=caller, message=None)
