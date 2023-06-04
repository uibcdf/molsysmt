import numba as nb
from itertools import product

def make_numba_signature(arguments=None, output=None):
    
    aux_arguments=[]
    aux_output=[]
    
    if not isinstance(arguments, (list,tuple)):
        arguments = [arguments]
    
    for argument in arguments:
    
        if isinstance(argument, (list,tuple)):
            aux_argument=[]
            with_default=False
            n_default = 0
            for option in argument:
                if not option.__class__.__module__.startswith('numba.core.types.'):
                        n_default += 1
                        option=nb.types.Omitted(option)
                        aux_argument.append(option)
                        with_default=True
                if n_default>1:
                    raise ValueError("More than one default value")
            for option in argument:
                if option.__class__.__module__.startswith('numba.core.types.'):
                    aux_argument.append(option)
            aux_arguments.append(aux_argument)
        
        else:
            
            aux_arguments.append([argument])
    
    aux_arguments=list(product(*aux_arguments))
    
    if output is None:
        output=nb.void

    if isinstance(output,(list,tuple)):
        output=nb.types.Tuple(tuple(output))

    signature=[]
    
    for ii in aux_arguments:
        signature.append(output(*ii))
    
    if len(signature)==1:
        signature=signature[0]
    
    return signature

