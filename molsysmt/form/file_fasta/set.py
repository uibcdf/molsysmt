from molsysmt._private.arg_digestion import arg_digest
import types

form = 'file:fasta'

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('set_')]
