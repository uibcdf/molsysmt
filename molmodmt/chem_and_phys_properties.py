from .utils.exceptions import *
from .multitool import select as _select
from .multitool import convert as _convert

def get_masses(item=None,selection=None,engine='mdtraj'):

    if engine == 'mdtraj':

        tmp_item = _convert(item,'mdtraj')
        tmp_list = _select(tmp_item,selection)
        masses = [tmp_item.topology.atom(ii).element.mass for ii in tmp_list]
        del(tmp_item, tmp_list)
        return masses

    else:

        raise NotImplementedError(NotImplementedMessage)
