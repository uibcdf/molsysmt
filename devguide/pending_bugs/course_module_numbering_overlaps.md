# Course Module Numbering Overlaps

**Status:** Confirmed

## Problem

`docs/content/course/index.md` and `README.md` describe a common core containing
modules 1–16. The filesystem contains 20 common-core notebooks numbered 01–20,
while every specialized path contains modules 17–50. Modules 17–20 therefore
have two meanings in the same curriculum.

The course contains 156 notebooks rather than a simple common 16 plus four
non-overlapping continuations.

## Impact

- lifecycle instructions cannot identify a module unambiguously;
- links and progress tracking can refer to different content;
- renumbering proposals and actual files disagree;
- students can receive conflicting sequence expectations.

## Required resolution

Choose the intended common-core boundary, define stable module identifiers that
do not depend only on display numbers, migrate filenames/indexes/cross-links,
and add a course-structure validator. Preserve redirects or an explicit mapping
if published links already exist.
