import numpy as np
from ...exceptions import ArgumentError

functions_where_boolean = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.iterator.__init__',
    '.iterators.__init__'
    )

def digest_bioassembly(bioassembly, caller=None):

    from .chain_indices import digest_chain_indices
    from .rotations import digest_rotations
    from .translations import digest_translations

    if caller is not None:

        if caller.endswith(functions_where_boolean):
            if isinstance(bioassembly, bool):
                return bioassembly
            else:
                raise ArgumentError('bioassembly', value=bioassembly, caller=caller, message=None)

        if caller=='molsysmt.build.make_bioassembly.make_bioassembly':
            if isinstance(bioassembly, str):
                return bioassembly
            elif isinstance(bioassembly, dict):
                right_format=True
                try:
                    bioassembly['chain_indices']=digest_chain_indices(bioassembly['chain_indices'], caller='digest_bioassembly')
                    bioassembly['rotations']=digest_rotations(bioassembly['rotations'], caller='digest_bioassembly')
                    bioassembly['translations']=digest_translations(bioassembly['translations'], caller='digest_bioassembly')
                except:
                    right_format=False
                if right_format:
                    return bioassembly
            else:
                raise ArgumentError('bioassembly', value=bioassembly, caller=caller, message=None)

    if bioassembly is None:
        return None

    if isinstance(bioassembly, dict):
        right_format=True
        for name, aux_dict in bioassembly.items():
            try:
                aux_dict['chain_indices']=digest_chain_indices(aux_dict['chain_indices'], caller='digest_bioassembly')
                aux_dict['rotations']=digest_rotations(aux_dict['rotations'], caller='digest_bioassembly')
                aux_dict['translations']=digest_translations(aux_dict['translations'], caller='digest_bioassembly')
            except:
                right_format=False
                break
        if right_format:
            return bioassembly

    raise ArgumentError('bioassembly', value=bioassembly, caller=caller, message=None)
