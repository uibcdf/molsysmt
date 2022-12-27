class FileAlreadyHandledError(Exception):

    def __init__(self, filename):

        full_message = f"The file {filename} is already handled by MolSysMT."


