from ..exceptions import *

def digest_time(time):

    output = None

    if (time is None) or (type(time)==float):

        output = time

    else:

        raise WrongTimeError()

    return output

