from molsysmt._private.smonitor import ArgumentError


def digest_cmap(cmap, caller=None):

    # Matplotlib is imported here rather than at the top of the module on purpose.
    # ArgDigest discovers every digester in this package when it initializes, so a
    # module-level `from matplotlib.pyplot import colormaps` made *any* digested call load
    # the whole of Matplotlib -- measured at 315 ms -- to validate a colormap name that
    # most calls never pass.
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap
    from matplotlib.pyplot import colormaps

    if cmap is None:
        return None

    if isinstance(cmap, str):
        if cmap in colormaps:
            return colormaps[cmap]

    if isinstance(cmap, (LinearSegmentedColormap, ListedColormap)):
        return cmap

    raise ArgumentError('cmap', value=cmap, caller=caller, message=None)
