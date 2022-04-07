
def is_nglview_NGLWidget(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return (item_fullname=='nglview.widget.NGLWidget')

