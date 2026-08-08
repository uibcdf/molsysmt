"""Contract for `convert`, whose extra keywords reach the converter it resolves.

The domain is keyed by the target form. See
`molsysmt/_private/argdigest/domain/converter_arguments.py` for why the origin form is
deliberately not part of the key.
"""

from argdigest import FunctionContract

contract = FunctionContract(
    caller='molsysmt.basic.convert.convert',
    admits='converter_arguments',
    description='Extra keywords are forwarded to the resolved converter.',
)
