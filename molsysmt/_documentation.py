
html_figures = {
    'index.ipynb' : ['_static/nglview/index_fig1.html',
        ],

        }

counter = {ii:0 for ii in html_figures}

def next_htmlfile(notebook_path):

    index = counter[notebook_path]
    counter[notebook_path]+=1

    return html_figures[notebook_path][index]

