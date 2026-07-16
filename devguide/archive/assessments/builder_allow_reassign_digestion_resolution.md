# Builder `allow_reassign` Is Not Digested

**Status:** resolved 2026-07-13

## Problem

`MolSysBuilder.add_chain(..., allow_reassign=False)` is a decorated public
method, but ArgDigest reports that no digester is registered for
`allow_reassign`. Builder, topology-dictionary, and YAML round-trip tests emit
`DigestNotDigestedWarning` repeatedly when the method is exercised.

The flag changes whether existing group-to-chain assignments may be overwritten,
so accepting an unnormalized value is behaviorally significant rather than a
cosmetic warning.

## Required resolution

- Register or route a boolean digester for `allow_reassign` in this caller.
- Test accepted boolean values and rejection/normalization of invalid values.
- Assert that ordinary builder and declarative round trips do not emit
  `DigestNotDigestedWarning`.
- Check other public builder-specific arguments for the same gap.

## Resolution

`allow_reassign` now has a standard boolean digester. Focused tests verify both
accepted boolean values, rejection of a string value, and absence of
`DigestNotDigestedWarning` during the ordinary builder call.
