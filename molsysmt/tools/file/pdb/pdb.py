
class PDB():

    def __init__(filename):

        self._string = None
        self.

        with open(filename, 'r+') as fff:
            self.string = fff.read()

    def guess_version(self):

        return '3.3'
