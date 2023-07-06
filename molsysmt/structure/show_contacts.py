
def show_contacts(molecular_system, selection=None, groups_of_atoms=None, group_behavior=None, structure_indices="all",
                 selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, structure_indices_2=None,
                 threshold='12 angstroms', pbc=False,
                 engine='MolSysMT', syntax='MolSysMT'):

    from .get_contacts import get_contacts
    from molsysmt.basic import get_label
    import plotly.express as px

    contact_map = get_contacts(molecular_system, selection=selection,
            groups_of_atoms=groups_of_atoms, group_behavior=group_behavior,
            structure_indices=structure_indices, selection_2=selection_2,
            groups_of_atoms_2=groups_of_atoms_2, group_behavior_2=group_behavior_2,
            structure_indices_2=structure_indices_2, threshold=threshold, pbc=pbc,
            engine=engine, syntax=syntax)

    CA_labels = get_label(molecular_system, selection=selection,
                          string='{group_name}-{group_id}')

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

    return fig.show()

