def is_form(item):

    class_module = type(item).__module__
    class_name = type(item).__name__

    return 'openff.toolkit' in class_module and class_name == 'Topology'
