import types

form = 'string:uniprot_id'

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
