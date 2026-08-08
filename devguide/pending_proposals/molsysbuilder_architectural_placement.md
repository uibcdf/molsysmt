# Proposal: Architectural Placement of `MolSysBuilder` (`molsysmt.build.MolSysBuilder`)

> **Status:** Pending Architectural Discussion  
> **Date:** August 2026

## 🎯 Overview
Currently, `MolSysBuilder` is listed under native forms (`molsysmt.native.MolSysBuilder` and `docs/content/user/foundations/native_world/classes/molsysmt_MolSysBuilder.md`).

However, unlike static data containers (`molsysmt.MolSys`, `molsysmt.Topology`, `molsysmt.Structures`), `MolSysBuilder` is an **active procedural tool** designed for incremental construction, atom/group addition, and validation before compilation.

## 📋 Proposal Options
1. **Move to `molsysmt.build`**: Position `MolSysBuilder` under `molsysmt.build.MolSysBuilder` alongside build functions (`add_missing_heavy_atoms`, `add_hydrogens`), similar to how `Iterator` lives under `tools/basic/`.
2. **Dual Registration / Alias**: Retain form registration for `msm.get()` and `msm.info()` introspection on uncompiled builder objects while exposing `MolSysBuilder` primarily in the `build` toolbox module.
