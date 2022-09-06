from IPython.display import IFrame

def load_html_in_jupyter_notebook(filename):

    return IFrame(src=filename, width=700, height=700)

