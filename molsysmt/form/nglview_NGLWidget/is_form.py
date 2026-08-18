def is_form(item):
    """
    Checking whether an item is an instance of form nglview.NGLWidget.

    Parameters
    ----------
    item : nglview.NGLWidget
        Source item in nglview.NGLWidget form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    output = False

    class_name = str(type(item))
    if 'nglview.widget.NGLWidget' in class_name:
        output = True

    return output
