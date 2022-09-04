from ...exceptions import ArgumentError
from ...variables import is_all

def digest_bioassembly(bioassembly, caller=None):

    if caller.startswith('molsysmt.build.make_bioassembly'):
        if isinstance(bioassembly, dict):
            is_bioassembly=True
            for aux in bioassembly:
                if isinstance(aux, dict):
                    if not ('chains' in aux):
                        is_bioassembly=False
                        break
                    elif not ('rotations' in aux):
                        is_bioassembly=False
                        break
                    elif not ('translations' in aux):
                        is_bioassembly=False
                        break
                else:
                    break
            if is_bioassembly:
                return bioassembly

    if caller=='molsysmt.basic.get.get':

        if isinstance(bioassembly, bool):
            return bioassembly


    raise ArgumentError('bioassembly', value=bioassembly, caller=caller, message=None)

