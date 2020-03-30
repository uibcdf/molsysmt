
def _raise_not_implemented_error(item, indices=None, frame_indices=None, value=None):
    raise NotImplementedError

target_fields = {

        'atom' : {
            'name' : _raise_not_implemented_error
            },

        'group' : {
            'name' : _raise_not_implemented_error
            },

        'chain' : {
            },

        'molecule' : {
            },

        'system' : {
            'coordinates' : _raise_not_implemented_error,
            'box' : _raise_not_implemented_error
            }

        }

