from ..exceptions import *

elements = [
    'atom',
    'group',
    'component',
    'chain',
    'molecule',
    'entity',
    'system',
    'bond',
]

elements_from_plural={
    'atoms' : 'atom',
    'groups' : 'group',
    'residue' : 'group',
    'residues' : 'group',
    'components' : 'component',
    'chains' : 'chain',
    'molecules' : 'molecule',
    'entities' : 'entity',
    'systems' : 'system',
    'bonds' : 'bond',
}

def digest_element(element):

    try:
        tmp_element = element.lower()
        if tmp_element in elements_from_plural:
            tmp_element = elements_from_plural[tmp_element]
        elif tmp_element not in elements:
            raise BadCallError()
        return tmp_element
    except:
        raise BadCallError()

