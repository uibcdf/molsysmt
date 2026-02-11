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
            numba_options=[]
            default_option=None
            n_default = 0

            for option in argument:
                if option.__class__.__module__.startswith('numba.core.types.'):
                    numba_options.append(option)
                else:
                    n_default += 1
                    default_option = option

                if n_default > 1:
                    raise ValueError("More than one default value")

            if n_default == 1 and default_option is None:
                if len(numba_options) == 0:
                    raise ValueError("Optional None requires at least one numba type")
                for option in numba_options:
                    aux_argument.append(nb.optional(option))
            else:
                if n_default == 1:
                    aux_argument.append(nb.types.Omitted(default_option))
                aux_argument.extend(numba_options)

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
