import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_path(path, caller=None):

    if caller == "molsysmt.topology.get_covalent_paths.get_covalent_paths":
        if not isinstance(path, (list, tuple, np.ndarray)):
            raise ArgumentError("path", value=path, caller=caller)
        if isinstance(path, np.ndarray) and path.ndim not in (1, 2):
            raise ArgumentError("path", value=path, caller=caller)
        if len(path) == 0:
            raise ArgumentError("path", value=path, caller=caller)

        positions = []
        for selector in path:
            if isinstance(selector, str):
                positions.append(selector)
            elif isinstance(selector, (int, np.integer)) and not isinstance(
                selector, (bool, np.bool_)
            ):
                positions.append(int(selector))
            elif isinstance(selector, (list, tuple, np.ndarray, range)):
                if isinstance(selector, (list, tuple)) and any(
                    isinstance(value, (bool, np.bool_)) for value in selector
                ):
                    raise ArgumentError("path", value=path, caller=caller)
                try:
                    indices = np.asarray(selector)
                except (TypeError, ValueError, OverflowError) as error:
                    raise ArgumentError("path", value=path, caller=caller) from error
                if indices.ndim != 1:
                    raise ArgumentError("path", value=path, caller=caller)
                if indices.size and indices.dtype.kind not in "iu":
                    if indices.dtype.kind != "O" or not all(
                        isinstance(value, (int, np.integer))
                        and not isinstance(value, (bool, np.bool_))
                        for value in indices
                    ):
                        raise ArgumentError("path", value=path, caller=caller)
                positions.append(indices.tolist())
            else:
                raise ArgumentError("path", value=path, caller=caller)
        return positions

    raise ArgumentError("path", value=path, caller=caller, message=None)
