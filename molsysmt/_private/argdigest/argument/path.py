import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_path(path, caller=None):

    if caller == "molsysmt.topology.get_covalent_paths.get_covalent_paths":
        if isinstance(path, (list, tuple, np.ndarray)):
            return path

    raise ArgumentError("path", value=path, caller=caller, message=None)
