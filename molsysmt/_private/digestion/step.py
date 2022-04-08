from ..exceptions import *

def digest_step(step):

    output = None

    if (step is None) or (type(step)==int):

        output = step

    else:

        raise WrongStepError()

    return output

