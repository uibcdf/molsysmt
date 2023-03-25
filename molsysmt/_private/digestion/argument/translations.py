import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

def digest_translations(translations, caller=None):

    if caller is not None:
        if caller.endswith('digest_bioassembly'):
            from .translation import digest_translation
            if isinstance(translations, (np.ndarray, list, tuple)):
                return [digest_translation(ii) for ii in translations]

    raise ArgumentError('translations', value=rotation, caller=caller, message=None)


