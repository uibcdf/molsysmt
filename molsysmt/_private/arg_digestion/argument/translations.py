import numpy as np
from molsysmt._private.smonitor import ArgumentError
from .translation import digest_translation

def digest_translations(translations, caller=None):

    if caller is not None:
        if caller.endswith('digest_bioassembly'):
            if isinstance(translations, (np.ndarray, list, tuple)):
                return [digest_translation(ii) for ii in translations]

    raise ArgumentError('translations', value=translations, caller=caller, message=None)

