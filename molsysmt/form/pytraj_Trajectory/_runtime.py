"""Checking whether the installed PyTraj trajectory runtime is safe to use."""

from __future__ import annotations

import sys


def has_unsafe_frame_finalizer() -> bool:
    """
    Performing has unsafe frame finalizer on form pytraj.Trajectory.


    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    if sys.version_info < (3, 13):
        return False

    from pytraj import Frame

    return "__del__" in Frame.__dict__


def ensure_safe_runtime() -> None:
    """
    Performing ensure safe runtime on form pytraj.Trajectory.


    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    if has_unsafe_frame_finalizer():
        from molsysmt._private.smonitor import NotSupportedFormError

        raise NotSupportedFormError(
            form="pytraj.Trajectory",
            message=(
                "The installed PyTraj extension contains the obsolete Frame.__del__ "
                "finalizer and can abort under Python 3.13. Install a current "
                "Cython 3-compatible PyTraj build before using pytraj.Trajectory."
            ),
        )
