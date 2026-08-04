# Pending Documentation Proposals

This directory contains documentation that should exist and does not, or that
should be reorganized. Typically a contract has been decided and implemented, and
nothing in the user-facing pages tells a reader about it.

An entry should name the page or notebook where the explanation belongs, say what a
reader can currently conclude without it, and link to the normative statement in the
developer guide. These entries plan how to *explain* a rule; they never define one.

## Current triage

- [`convert_tutorial_multi_form_structure_axis.md`](convert_tutorial_multi_form_structure_axis.md)
  — the convert tutorial shows how to combine several forms into one molecular
  system but says nothing about which item then owns the structure axis, so a reader
  cannot tell what happens when a topology holding one reference conformation meets
  a trajectory.
