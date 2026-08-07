"""Contract for `get_label`.

`get_label` declares `**kwargs` and never reads it: nothing in its body mentions the
name. The door is open onto nothing, so anything passed through it is silently
discarded. Holding the function to its own signature closes it.
"""

from argdigest import FunctionContract

contract = FunctionContract(
    caller='molsysmt.basic.get_label.get_label',
    admits='signature',
    description='Takes no keyword beyond its signature; its **kwargs is unused.',
)
