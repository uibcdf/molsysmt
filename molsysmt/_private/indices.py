from .variables import is_all
from molsysmt._private.smonitor import ArgumentError

def indices_iterator(indices=None, start=0, stop=None, step=1, chunk=1):

    output = None

    if is_all(indices):
        indices=None

    if indices is None:
        if stop is None:
            raise ArgumentError(argument='stop', caller='molsysmt._private.indices.indices_iterator',
                                message='stop must be provided when indices is None or all.')
        output = list(range(start, stop, step))
    else:
        if stop is None:
            stop=len(indices)
        if stop>=len(indices):
            stop=len(indices)
        output = indices[slice(start, stop, step)]
    
    if chunk>1:
        coutput = []
        chunks = len(output)//chunk
        where = 0
        for ii in range(chunks):
            coutput.append(output[where:where+chunk])
            where += chunk
        if where<len(output):
            coutput.append(output[where:])
        del(output)
        output=coutput
            
    return output.__iter__()

