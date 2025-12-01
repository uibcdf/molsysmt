
def show_contacts(molecular_system, selection=None, center_of_atoms=False, weights=None, structure_indices="all",
                  selection_2=None, center_of_atoms_2=False, weights_2=None, structure_indices_2=None,
                  threshold='12 angstroms', pbc=False, syntax='MolSysMT', style='plotly', show=True,
                  skip_digestion=False):
    """
    Visualize a contact map between two selections.

    Parameters
    ----------
    molecular_system : molecular system
        Input system to analyze.
    selection, selection_2 : str, list, tuple, numpy.ndarray or None
        Atom selections (MolSysMT syntax or indices). If `selection_2` is `None`, contacts are computed within `selection`.
    center_of_atoms, center_of_atoms_2 : bool, default False
        Whether to use centers of groups of atoms for each selection.
    weights, weights_2 : array-like, optional
        Weights for centers if `center_of_atoms` is True.
    structure_indices, structure_indices_2 : 'all' or array-like
        Structures/frames to analyze (0-based).
    threshold : quantity or str, default '12 angstroms'
        Distance cutoff for defining contacts.
    pbc : bool, default False
        Whether to consider periodic boundary conditions.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    style : {'plotly', 'matplotlib'}, default 'plotly'
        Backend for visualization.
    show : bool, default True
        If True, render the figure; otherwise return it.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    object
        The figure object (Plotly Figure or Matplotlib Figure) or the result of `fig.show()` when `show=True`.
    """

    from .get_contacts import get_contacts
    from molsysmt.basic import get_label

    contact_map = get_contacts(molecular_system, selection=selection,
            center_of_atoms=center_of_atoms, weights=weights,
            structure_indices=structure_indices, selection_2=selection_2,
            center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
            structure_indices_2=structure_indices_2, threshold=threshold, pbc=pbc,
            syntax=syntax)

    CA_labels = get_label(molecular_system, selection=selection,
                          string='{group_name}-{group_id}')


    if style=='plotly':

        import plotly.express as px

        fig = px.imshow(~contact_map, animation_frame=0, binary_string=True, height=600, origin='lower')

        fig.update_layout(
            xaxis = dict(
                tickmode = 'array',
                tickvals = list(range(0,contact_map.shape[1],25)),
                ticktext = CA_labels[::25],
                tickangle = 45
            ),
            yaxis = dict(
                tickmode = 'array',
                tickvals = list(range(0,contact_map.shape[1],25)),
                ticktext = CA_labels[::25],
                tickangle = 45
            )
        )

        if show:
            return fig.show()
        else:
            return fig

    elif style=='matplotlib':

        from matplotlib import pyplot as plt

        fig, ax = plt.subplots()

        ax.imshow(contact_map[0], cmap='Greys', origin='lower')

        if show:
            return plt.show()
        else:
            return fig
