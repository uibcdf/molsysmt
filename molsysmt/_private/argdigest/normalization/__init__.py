"""Declared argument-name aliases.

One module per family of rules. Each declares `table` or `TABLES` with `AliasTable`
instances; ArgDigest discovers them, composes them most-specific-first and applies them
before both the function contract and the argument digesters. Nothing here is code: the
aliases a function accepts can therefore be listed rather than read out of a branch.
"""
