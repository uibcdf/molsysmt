from molsysmt._private.exceptions import ArgumentError

def digest_keys(keys, caller=None):


    if caller == 'molsysmt.build.mutate.mutate':

        if isinstance(keys, str):

            if keys.lower() in ['group_index', 'group_indices',
                    'residue_index', 'residue_indices']:
                return 'group_index'
            elif keys.lower() in ['group_id', 'group_ids',
                    'residue_id', 'residue_ids']:
                return 'group_id'
            elif keys.lower() in ['group_name', 'group_names',
                    'residue_name', 'residue_names']:
                return 'group_name'

    raise ArgumentError('keys', value=keys, caller=caller, message=None)
