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

    # Visualization is currently disabled due to missing backend modules.
    # To be implemented in Fase 2 of Ecosystem Integration.

    return contact_map
