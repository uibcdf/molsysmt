class BadCallError(ValueError):
    pass

class IncompleteElementError(Exception):
    pass

NotImplementedMessage = 'It has not been implemeted yet.\n Write a new issue in \
                         https://github.com/uibcdf/MolSysMT/issues asking for it.'

BadCallMessage = 'Wrong way of invoking this method.\nCheck the online documentation \
        for more information: http://www.uibcdf.org/MolSysMT'

