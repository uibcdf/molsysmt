from molsysmt._private.exceptions import ArgumentError

nglview_representations = [
        "cartoon",
        "surface",
        "licorice",
        "ribbon",
        "line",
        "ball_and_stick",
        ]

def digest_representation(representation, caller=None):


    if caller.startswith('molsysmt.thirds.nglview.'):

        if isinstance(representation, str):
            return representation

    raise ArgumentError('representation', value=representation, caller=caller, message=None)
