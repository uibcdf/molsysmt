from molsysmt._private.dep_digestion import dep_digest
from depdigest import is_installed, check_dependency
from molsysmt import _depdigest

def info():
    """
    Display a summary of the dependency ecosystem.

    Returns
    -------
    pandas.io.formats.style.Styler
        A styled DataFrame showing the status of each library.
    """
    from pandas import DataFrame
    
    rows = []
    # LIBRARIES is the dictionary in _depdigest
    for key, info in _depdigest.LIBRARIES.items():
        pypi_name = info.get('pypi', key)
        installed = is_installed(pypi_name)
        rows.append({
            'Library': key,
            'Status': 'Installed' if installed else 'Not Installed',
            'Type': info.get('type', 'soft').capitalize(),
            'Install (PyPI)': f"pip install {pypi_name}",
            'Install (Conda)': f"conda install -c conda-forge {key}"
        })
        
    df = DataFrame(rows)
    df.sort_values(by=['Status', 'Type', 'Library'], ascending=[True, True, True], inplace=True)
    
    return df.style.hide(axis='index').set_properties(**{'text-align': 'left'})
