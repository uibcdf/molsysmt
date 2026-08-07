from molsysmt._private.argdigest import arg_digest
import types

form = 'string:smiles'

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('set_')]
