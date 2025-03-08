import numpy as np
from ...exceptions import ArgumentError

definitions = {
    'get_mass': ['OpenMM', 'physical'],
    'get_hydrophobicity': ['eisenberg', 'rao', 'sweet', 'kyte', 'abraham', 'bull', 'guy', 'miyazawa', 'roseman',
                         'wolfenden', 'chothia', 'hopp', 'manavalan', 'black', 'fauchere'],
    'get_volume': ['grantham'],
}

def digest_definition(definition, caller=None):

    if caller=='molsysmt.physchem.get_mass.get_mass':
        if isinstance(definition, str):
            if definition in ['OpenMM', 'physical']:
                return definition

    elif caller=='molsysmt.physchem.get_mass.get_mass':
        if isinstance(definition, str):
            if definition in definitions['get_mass']:
                return definition

    elif caller=='molsysmt.physchem.get_hydrophobicity.get_hydrophobicity':
        if isinstance(definition, str):
            if definition in definitions['get_hydrophobicity']:
                return definition

    elif caller=='molsysmt.physchem.get_volume.get_volume':
        if isinstance(definition, str):
            if definition in definitions['get_volume']:
                return definition

    return ArgumentError('definition', value=definition, caller=caller, message=None)

