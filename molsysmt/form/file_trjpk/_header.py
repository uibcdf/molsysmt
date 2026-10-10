import pickle


def _read_counts(filename):
    """Reading the two existing TRJPK count records without loading arrays."""
    with open(filename, "rb") as stream:
        return pickle.load(stream), pickle.load(stream)
