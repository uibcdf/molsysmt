

class Iterator:
    """ A class that allows to iterate trough trajectories of any type.
    """
    def __init__(self,
                 molecular_system,
                 start=0,
                 interval=1,
                 stop=None,
                 chunk_size=None,
                 selection="all",
                 syntaxis="MolSysMT"
                 ):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        return 1.0, 1.0, [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]
