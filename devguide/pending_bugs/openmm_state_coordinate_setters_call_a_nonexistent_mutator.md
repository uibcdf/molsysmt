---
summary: OpenMM State coordinate setters call a nonexistent mutator
issue: uibcdf/molsysmt#736
status: active
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [form, diagnostics]
guard: tests/form/openmm_State/test_immutable_positions.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Refusing unsupported State coordinate assignment

## What

Public set passes structure_indices to State setters that do not accept it;
four controls fail at ArgDigest with UnknownArgumentError. Two direct-adapter
controls then expose AttributeError: OpenMM State has no setPositions method.
The captured object is not a live mutable Context. This is a MolSysMT adapter
contract defect, not a demonstrated ArgDigest or OpenMM provider failure.
Four separate controls find that the mutable Context alternative also rejects
the public structure_indices argument. Its real assignment behavior must remain
available rather than being conflated with State refusal.

## How

A two-particle Reference context captures positions without dynamics, then is
retired before testing the detached State. Public atom/system calls run under
nm/ps and pm/fs; direct hooks separate dispatch failure from the missing native
method. The original four-case and later six-case failures are preserved.

## Why

An advertised setter must not call a nonexistent provider method or expose an
unrelated argument-protocol failure. Add the shared structure selector to the
validated hook signature and refuse mutation with the existing catalogued
NotImplementedMethodError, preserving every captured coordinate. Direct callers
and the form article must identify Context/native Structures as editing routes.
The Context hooks accept that shared single-structure selector and continue
actual coordinate assignment with explicit nm conversion. Multiple/absent
poses are rejected before mutating the live context.
This implements no snapshot copy, new mutator or force-field algorithm; #592
retains independent-copy design and qualification.

## Receiving and exit

The original public and direct controls must receive the intended diagnostic
and unchanged coordinates; documentation, common checks and published closeout
remain due. The failed first GitHub create call is checked against the complete
board before retry; no duplicate is created. No provider report is warranted
for this transient upstream transport error or MolSysMT's own adapter defects.


## Source receiving — 2026-11-12

The initial corrected State cohort passes six controls. Four live-Context
public atom/system tests then independently reproduce the selector-signature
defect; adding the validated selector preserves actual partial/full assignment.
The final focused 34-case cohort passes both State refusal and Context mutation
under nm/ps and pm/fs, alongside #735 and the updated PDB doctests. No provider
upgrade or snapshot-copy implementation is introduced. Form documentation,
common checks and public closeout remain due.
