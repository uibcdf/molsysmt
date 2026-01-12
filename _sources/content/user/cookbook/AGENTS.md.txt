# User Guide Cookbook Agents Guide

This guide is for agents editing the **Cookbook** section of the User Guide
under `docs/content/user/cookbook`.

## Purpose

- Provide practical, end-to-end recipes that combine multiple MolSysMT tools (and possibly external engines) to accomplish concrete tasks.
- Assume the reader has basic familiarity with MolSysMT and can refer back to individual tool tutorials for detailed behavior.

## Structure

- Keep `cookbook/index.md` as the entry point listing available recipes.
- Each recipe notebook (`*.ipynb`) should:
  - Start with a clear title and a short summary of the goal (for example, preparing a system, running a short simulation, analyzing a trajectory).
  - Outline prerequisites (for example, required external packages, example files, or demo systems).
  - Present steps in logical order, with short code cells and narrative explanations in between.
  - Link to relevant Tools tutorials and Showcase examples where helpful, using labeled sections and `{ref}` roles whenever possible instead of direct file paths.

## Style and scope

- Focus on workflows and “how to combine tools”, not on detailed API reference (which belongs in Tools and API docs).
- Keep examples reasonably lightweight so they can be executed in a typical user environment without long runtimes.
- Use MyST admonitions (`tip`, `warning`, `seealso`) to highlight important considerations or point to related recipes and tools.
