from ...exceptions import ArgumentError

def digest_nodes_name(nodes_name, caller=None):

    if caller=='molsysmt.topology.get_bondgraph.get_bondgraph':
        if isinstance(nodes_name, str):
            if nodes_name in ['atom_index', 'short_string', 'long_string']:
                return nodes_name

    raise ArgumentError('nodes_name', value=nodes_name, caller=caller, message=None)

