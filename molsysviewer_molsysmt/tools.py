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
        A lazy per-view expert facade and the qualified System task editor.

    Raises
    ------
    RuntimeError
        If the host lacks the view-lifetime boundary required by the facade.
    """
    from molsysviewer import AddonPanelSpec, AddonSpec, AddonWorkspaceSpec, MolSysView

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
        workspaces=(
            AddonWorkspaceSpec(
                id="molsysmt",
                title="Molecular tools",
                entry_panel="system",
                description="MolSysMT tools for this molecular system.",
                order=10,
            ),
        ),
        panels=(
            AddonPanelSpec(
                id="system",
                title="System",
                order=10,
                widget_class="molsysviewer_molsysmt._panel._SystemPanel",
                description="Remove atoms, extract a subset or copy the molecular system independently.",
            ),
        ),
        meta={"status": "experimental"},
    )
