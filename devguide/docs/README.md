# Documentation Work Queues

This tree holds pending work whose deliverable is **user-facing documentation**:
the User Guide, the Cookbook, the API docstrings, and the Four Paths course.

It is separate from `../pending_bugs/` and `../pending_proposals/`, which hold work
whose deliverable is code or a design decision. The separation is about what has to
change, not about importance. A defect that is invisible to a reader of the library
but wrong in the reference pages belongs here; a defect in a public function
belongs there.

- [Pending bugs](pending_bugs/README.md) — documentation that is wrong, stale, or
  contradicts the implemented behaviour.
- [Pending proposals](pending_proposals/README.md) — documentation that is missing
  or should be reorganized.

An entry here should name the page or notebook it affects, state what a reader
currently takes away, and state what they should take away instead. Where the topic
already has a normative statement in the developer guide, link to it: these entries
are the plan for explaining a contract, never a second place to define it.

Moving a document into or out of this tree changes its documentary status; it does
not mean any page has been written or reviewed.
