---
summary: Course contributor guide names an obsolete validator entrypoint.
issue: uibcdf/molsysmt#637
status: open
opened: 2026-11-07
closed:
severity: low
verification: reproduced
area: [docs, devtools]
guard:
normative:
blocked_by: []
supersedes: []
---

# Course validator entrypoint guidance

## What

The course contributor guide (`docs/content/course/AGENTS.md`, Course Tooling & Tracking) names `docs/content/course/devtools/validate_course.py`, a legacy validator with obsolete section/micro-guide requirements. The maintained release/source route instead runs `devtools/scripts/validate_course.py`.

## How verified

On isolated source `11796a8a203ddd4f4f9d58bdc9ad3c20eb4d83f2`, invoking the course-local script with `--help` executes its checker rather than showing help, exits 1 and reports 0/156 modules compliant. It demands legacy headings such as Working System & Prerequisites and Check Your Understanding. The canonical `python devtools/scripts/validate_course.py` exits 0 on the same source. No notebook is executed or modified by these checks. The first invocation selected the wrong tool; its output must not be presented as a failing current course gate.

A complete 566-issue inventory found #142, but it concerned numbering/anchors in the canonical checker and is closed; it does not retire or redirect this legacy entrypoint. PR #543 exposes the ambiguity during contributor receiving but does not need to change course content to satisfy the legacy checker.

## Proposed disposition

Make the contributor guide name the maintained command. Decide whether the legacy script should be removed, explicitly archived, or delegated to the canonical validator, and protect that chosen entrypoint contract. Preserve the course notebooks and accepted sections rather than adding obsolete boilerplate. This is a nonblocking developer-tool/documentation follow-up, independent of scientific validation, #421 acceptance and release publication.
