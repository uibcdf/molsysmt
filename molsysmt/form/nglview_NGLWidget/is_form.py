def is_form(item):
    """
    Checking whether an item is an instance of form nglview.NGLWidget.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form nglview.NGLWidget, False otherwise.
    """

    output = False

    class_name = str(type(item))
    if 'nglview.widget.NGLWidget' in class_name:
        output = True

    return output
