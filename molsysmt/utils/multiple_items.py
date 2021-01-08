import numpy as np

def item_is_list(item):

    output = False
    if type(item) in [list, tuple]:
        output = True

    return output

def list_is_a_single_item(item):

    from molsysmt import get

    output = False
    if type(item) in [list, tuple]:
        has_topology = get(item, target='system', has_topology=True)
        if sum(has_topology)==1:
            output = True

    return output

def list_is_a_list_of_items(item):

    from molsysmt import get

    output = False
    if type(item) in [list, tuple]:
        has_topology = get(item, target='system', has_topology=True)
        if sum(has_topology)>1:
            output = True

    return output

def topology_and_trajectory_from_item(item):

    from molsysmt import get

    topology_item = None
    trajectory_item = None

    if type(item) in [list, tuple]:
        has_topology = get(item, target='system', has_topology=True)
        topology_item = item[np.argwhere(has_topology)[0,0]]
        has_coordinates = get(item, target='system', has_coordinates=True)
        trajectory_item = [item[ii] for ii in range(len(item)) if has_coordinates[ii]]
        if len(trajectory_item)==1:
            trajectory_item = trajectory_item[0]
    else:
        has_topology, has_coordinates = get(item, target='system', has_topology=True, has_coordinates=True)
        if has_topology:
            topology_item = item
        if has_coordinates:
            trajectory_item = item

    return topology_item, trajectory_item

