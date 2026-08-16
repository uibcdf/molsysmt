from IPython.display import IFrame

def load_html_in_jupyter_notebook(filename):
    """Load an NGLview HTML export inside a Jupyter notebook."""

    return IFrame(src=filename, width='100%', height='480px')
