from molsysmt._private.arg_digestion import arg_digest
from smonitor import signal

@signal(tags=['api', 'structure'])
@arg_digest()
def show_contacts(molecular_system, selection=None, center_of_atoms=False, weights=None, structure_indices="all",
                  selection_2=None, center_of_atoms_2=False, weights_2=None, structure_indices_2=None,
                  threshold='12 angstroms', pbc=False, syntax='MolSysMT', style='plotly', show=True,
                  skip_digestion=False):
    """
    To be written soon...
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
