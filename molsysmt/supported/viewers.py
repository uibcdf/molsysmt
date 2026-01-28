viewers = [
    'MolSysViewer',
    'NGLView',
]

lowercase_viewers = {ii.lower(): ii for ii in viewers}

viewers_forms = {
        'MolSysViewer': 'molsysviewer.MolSysView',
        'NGLView': 'nglview.NGLWidget',
        }
