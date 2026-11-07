from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Topology")
@dep_digest("openmm")
def copy(item, skip_digestion=False):
    """Creating an independent OpenMM topology with its declared metadata.

    Parameters
    ----------
    item : openmm.Topology
        Source topology, which is left unchanged.
    skip_digestion : bool
        Whether to skip argument digestion for a trusted internal call.
        The default is False.

    Returns
    -------
    openmm.Topology
        Independent topology retaining labels, insertion codes, known and
        unknown formal charges, bond type/order, empty inventory parents and
        periodic box vectors. This form contains no coordinate structures.

    See Also
    --------
    molsysmt.form.openmm_Topology.extract
        Extracting atoms through the same metadata-preserving builder.
    molsysmt.basic.copy
        Copying any supported molecular-system form.

    Examples
    --------
    >>> from openmm import app
    >>> source = app.Topology()
    >>> group = source.addResidue('LIG', source.addChain('A'))
    >>> atom = source.addAtom('N', app.element.nitrogen, group, formalCharge=1)
    >>> result = copy(source)
    >>> result is source, next(result.atoms()).formalCharge
    (False, 1)

    .. admonition:: User guide

       See :ref:`Tutorial_Form_openmm_Topology` and :ref:`Tutorial_Copy`.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, copy_if_all=True, skip_digestion=True)
