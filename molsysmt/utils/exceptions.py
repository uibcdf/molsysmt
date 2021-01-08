class BadCallError(ValueError):
    pass

class IncompleteElementError(Exception):
    pass

class NotWithThisFormError(ValueError):
    def __init__(self):
        super().__init__(NotWithThisFormMessage)

NotImplementedMessage = 'It has not been implemeted yet.\n Write a new issue in \
                         https://github.com/uibcdf/MolSysMT/issues asking for it.'

BadCallMessage = 'Wrong way of invoking this method.\nCheck the online documentation \
        for more information: http://www.uibcdf.org/MolSysMT'

NotWithThisFormMessage = 'This method can not be applied over this molecular system form.'
