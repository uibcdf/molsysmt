from ..exceptions import WrongSelectionError, WrongSelectionSyntaxError
from ..exceptions import WrongMultipleSelectionsError
from ..lists_and_tuples import is_list_or_tuple

def digest_selection(selection, syntax="MolSysMT", caller=None):
    """ Checks if a given selection has the correct type and syntax

        Parameters
        ----------
        item : str or list of int
            An instance of one of the forms supported by MolSysMT.
        syntax : str, default="MolSysMT"
            Name of the syntax used in the selection.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongSelectionError or WrongSelectionSyntaxError or WrongSyntaxError
            A WrongSelectionError is raised if the selection object is not in deed a selection.
            A WrongSelectionSyntaxError is raised if the selection is not using the expected
            syntax.
            A WrongSyntaxError is raised if the syntax given is not in deed a syntax.

    """

    from .syntax import digest_syntax
    from .atom import digest_atom_indices

    syntax = digest_syntax(syntax)

    if isinstance(selection, str):
        return selection

    try:
        selection = digest_atom_indices(selection)
        return selection
    except:
        pass

    raise WrongSelectionError(selection, syntax, caller=caller)

def digest_multiple_selections(selections, syntax="MolSysMT", caller=None):
    """ Checks if a list of selections have the correct types and syntax

       Parameters
       ----------
       item : list or tuple
           List of tuple of selections to be checked.
       syntax : str, default="MolSysMT"
           Name of the syntax used in the selections.
       caller: str, optional
           Name of the function or method that is being digested.

       Raises
       ------
       WrongSelectionError or WrongSelectionSyntaxisError or WrongSyntaxisError or WrongMultipleSelectionsError
           A WrongMultipleSelectionsError is raised if a single, or none, selection is given.
           A WrongSelectionError is raised if the a selection given is not in deed a selection.
           A WrongSelectionSyntaxisError is raised if a selection given is not using the expected
           syntax.
           A WrongSyntaxisError is raised if the syntax given is not in deed a syntax.

    """
    if is_list_or_tuple(selections):
        return [digest_selection(ii, syntax) for ii in selections]

    raise WrongMultipleSelectionsError(selections, caller=caller)

