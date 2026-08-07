"""Function argument contracts: what each public function accepts and requires.

One module per function or family. Each declares a `FunctionContract`, which is data:
the accepted domain of a function that takes `**kwargs` is invisible to
`inspect.signature`, and declaring it here is what makes it enforceable *and* readable.

A function with no module here falls back to ArgDigest's default: a closed signature is
held to its own parameters, and a function with `**kwargs` admits anything until its
domain is declared.
"""
