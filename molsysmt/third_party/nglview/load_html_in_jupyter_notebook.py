from IPython.display import IFrame

def load_html_in_jupyter_notebook(filename):
    """
    Loading and rendering a standalone HTML viewer file inside a Jupyter Notebook.




    Parameters
    ----------
    filename : str or pathlib.Path
        Argument filename.

    Returns
    -------
    IPython.display.HTML
        Interactive HTML display object.




    .. versionadded:: 1.0.0
    """

    return IFrame(src=filename, width='100%', height='480px')
