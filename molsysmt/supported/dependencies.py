from depdigest import get_info
from pandas import DataFrame

def dependencies():
    """
    Display a summary of the dependency ecosystem.

    Returns
    -------
    pandas.io.formats.style.Styler
        A styled DataFrame showing the status of each library.
    """
    rows = get_info('molsysmt')
    
    df = DataFrame(rows)
    df.sort_values(by=['Status', 'Type', 'Library'], ascending=[True, True, True], inplace=True)
    
    return df.style.hide(axis='index').set_properties(**{'text-align': 'left'})
