"""Declaring the redesigned tools addon without importing a browser at startup."""

from argdigest import arg_digest
from smonitor import signal


@signal(tags=["addon"])
@arg_digest(config="molsysviewer_molsysmt._argdigest")
def get_addon(*, skip_digestion=False):
    """Declaring MolSysMT tools for the compatible Viewer host.

    Parameters
    ----------
    skip_digestion : bool, default=False
        Whether to skip argument digestion for a trusted internal call.

    Returns
    -------
    molsysviewer.AddonSpec
        A lazy per-view expert facade. Graphical task panels are not provided
        by this initial read-tool delivery.

    Raises
    ------
    RuntimeError
        If the host lacks the view-lifetime boundary required by the facade.
    """
    from molsysviewer import AddonSpec, MolSysView

    from molsysmt import __version__

    from ._api import _MolSysMTTools

    if not isinstance(getattr(MolSysView, "closed", None), property):
        raise RuntimeError(
            "MolSysMT tools require a Viewer host with the closed-view lifecycle "
            "boundary. Update MolSysViewer to a qualified compatible version."
        )
    return AddonSpec(
        name="molsysmt",
        package="molsysmt",
        version=__version__,
        description="MolSysMT scientific tools bound to this view's molecular system.",
        state_factory=_MolSysMTTools,
    )
