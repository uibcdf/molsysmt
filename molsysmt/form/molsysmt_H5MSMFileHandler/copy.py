from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest(form="molsysmt.H5MSMFileHandler")
def copy(item, output_filename=None, skip_digestion=False):
    """
    Reporting the unavailable independent-copy route of a legacy H5MSM handler.

    Copying a live legacy handle is not implemented. Copy its file path after
    finishing any writer, or convert to a resident MolSys before copying.
    Parameters
    ----------
    item : molsysmt.native.H5MSMFileHandler
        Open legacy 0.3/0.4 handler. The source remains unchanged and open.
    output_filename : str or pathlib.Path, default=None
        Requested destination. No destination is created by this unsupported
        route, including when the default None is retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Raises
    ------
    NotImplementedMethodError
        Always. Recognizing the handler form does not implement an independent
        resource snapshot or change its ownership and read/write mode.

    Notes
    -----
    ``msm.copy(filename)`` performs the supported byte-preserving file operation
    and keeps its stored version. An automatic destination is process-owned;
    an explicit filename is caller-owned. Finish a writer before copying its
    path so that buffered changes are not mistaken for a complete snapshot.
    This route does not flush, reopen, close or publish a copy of the handler.

    See Also
    --------
    molsysmt.basic.copy : Copy supported resident objects and file paths.

    Examples
    --------
    Copy the path after finishing any writer instead of copying its live handle:

    >>> import molsysmt as msm
    >>> source = msm.systems['pentalanine']['traj_pentalanine.h5msm']
    >>> copied = msm.copy(source)
    >>> msm.get_form(copied)
    'file:h5msm'

    .. admonition:: User guide

       See :ref:`Tutorial_Form_molsysmt_H5MSMFileHandler` for legacy handler
       capabilities and supported file/resident alternatives.

    .. versionadded:: 1.0.0
    """

    raise NotImplementedMethodError(
        caller="molsysmt.form.molsysmt_H5MSMFileHandler.copy.copy"
    )
