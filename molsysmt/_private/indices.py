from .variables import is_all

def indices_iterator(indices=None, start=0, stop=None, step=1, chunk=1):
    
    output = None

    if is_all(indices):
        indices=None

    if indices is None:
        if stop is None:
            raise ValueError('stop needs to be different from None')
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

