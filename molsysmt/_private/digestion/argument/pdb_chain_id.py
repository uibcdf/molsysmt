from ...exceptions import ArgumentError

def digest_pdb_chain_id(pdb_chain_id, caller=None):

    if isinstance(pdb_chain_id, str):
        if pdb_chain_id.lower() in ['chain_id', 'chain_name']:
            return pdb_chain_id.lower()

    raise ArgumentError('pdb_chain_id', value=pdb_chain_id, caller=caller, message=None)

