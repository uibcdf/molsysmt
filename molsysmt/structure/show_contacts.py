from molsysmt._private.argdigest import arg_digest
from smonitor import signal

@signal(tags=['api', 'structure'])
@arg_digest()
def show_contacts(molecular_system, selection=None, center_of_atoms=False, weights=None, structure_indices="all",
                  selection_2=None, center_of_atoms_2=False, weights_2=None, structure_indices_2=None,
                  threshold='12 angstroms', pbc=False, syntax='MolSysMT', style='plotly', show=True,
                  skip_digestion=False):
    """
    Visualize the contact map between two sets of atoms as a 2-D heatmap.

    Computes the contact map via ``get_contacts`` and renders the first frame
    as a heatmap using either Plotly or Matplotlib.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, optional
        First set of atoms (rows of the contact matrix).  Nested iterables are
        treated as groups of atoms when ``center_of_atoms=True``.
    center_of_atoms : bool, default False
        If ``True``, use the (weighted) centroid of each group in ``selection``.
    weights : array-like, optional
        Per-atom weights for centroid computation of the first selection.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices over which contacts are evaluated.  Only the first frame
        of the resulting contact map is visualised.
    selection_2 : str, list, tuple or numpy.ndarray or None, default None
        Second set of atoms (columns of the contact matrix).  When ``None``,
        contacts are computed within ``selection`` itself.
    center_of_atoms_2 : bool, default False
        If ``True``, use the (weighted) centroid of each group in ``selection_2``.
    weights_2 : array-like, optional
        Per-atom weights for centroid computation of the second selection.
    structure_indices_2 : 'all', array-like or None, default None
        Frame indices for the second selection.  When ``None``, the same frames
        as ``structure_indices`` are used.
    threshold : str or quantity, default '12 angstroms'
        Distance cutoff for defining a contact.  Accepts any PyUnitWizard-parseable
        length quantity.
    pbc : bool, default False
        Apply minimum-image convention for periodic boundary conditions.
    syntax : str, default 'MolSysMT'
        Selection syntax used when selections are strings.
    style : {'plotly', 'matplotlib'}, default 'plotly'
        Plotting backend used to render the heatmap.
    show : bool, default True
        If ``True``, the figure is displayed immediately (``figure.show()`` for
        Plotly or ``plt.show()`` for Matplotlib).
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    plotly.graph_objects.Figure or matplotlib.figure.Figure
        The figure object produced by the selected plotting backend, containing
        the contact-map heatmap of the first frame.

    .. versionadded:: 1.0.0
    """

    from .get_contacts import get_contacts

    contact_map = get_contacts(molecular_system, selection=selection,
            center_of_atoms=center_of_atoms, weights=weights,
            structure_indices=structure_indices, selection_2=selection_2,
            center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
            structure_indices_2=structure_indices_2, threshold=threshold, pbc=pbc,
            syntax=syntax)
    contact_map_2d = contact_map[0].astype(int)

    if style == 'plotly':
        import plotly.graph_objects as go

        figure = go.Figure(data=go.Heatmap(z=contact_map_2d))
        if show:
            figure.show()
        return figure

    if style == 'matplotlib':
        import matplotlib.pyplot as plt

        figure, axis = plt.subplots()
        axis.imshow(contact_map_2d, origin='lower', interpolation='nearest')
        if show:
            plt.show()
        return figure

    return contact_map
