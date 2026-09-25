# Home Page Governance Directives (`index.AGENTS.md`)

This file defines the micro-governance rules, design philosophy, and content constraints for the MolSysMT home page ([`docs/index.ipynb`](index.ipynb)).

---

## 🎨 Design Philosophy & Aesthetic Directives

1. **Uncluttered & Spacious Layout:**  
   The home page must adhere to a clean, direct, and relaxed aesthetic ("less is more"). Avoid heavy grid dashboards, dense card matrices, or redundant navigation elements that duplicate the Sphinx sidebar.

2. **Linear Product-First Presentation:**  
   The page structure flows naturally:
   - Header: Centered logo, tagline, and essential release badges.
   - **`## Install it`**: Clean, one-liner installation instruction.
   - **`## Use it`**: Minimal, executable Python code snippet showing real library capabilities.
   - **`## Citation`**: Paper and software citation tabs.
   - **Hidden Toctree**: Pure Sphinx navigation tree (`:hidden:`) powering the sidebar menu without polluting the main content area.

---

## 🔒 Frozen Content & Inviolable Requirements

No contributor or AI agent may alter or remove the following core elements:

1. **Brand Identity Header:**
   - Centered logo figure referencing `_static/logo.svg` with `50%` width.
   - Tagline: *"A **Mol**ecular **Sys**tems **M**ulti**T**oolkit designed to simplify work with molecular models and simulations."*
   - **Badges Block Requirements:**
     - **Release Badge:** MUST match the current codebase version (e.g., `v0.21.0` / `molsysmt.__version__`); outdated hardcoded version strings are forbidden.
     - **License Badge:** MUST target `https://github.com/uibcdf/molsysmt/blob/main/LICENSE` (targeting legacy branches like `master` is forbidden).
     - **Conda & Python Badges:** Conda channel (`uibcdf`) and supported Python versions (`3.11 | 3.12 | 3.13`).
     - **Zenodo DOI Badge:** stable MolSysMT concept DOI
       (`10.5281/zenodo.1298752`). A historical version DOI must never be frozen into
       the home-page contract; see `devguide/release_and_citation.md`.

2. **Installation Block:**
   - Section heading: `## Install it`
   - Single command block: `conda install -c uibcdf molsysmt`

3. **Usage Demonstration ("Use it"):**
   - Section heading: `## Use it`
   - Executable Python code demonstrating loading, querying, and viewing a molecular system (`1BRS` protein selection):
     ```python
     import molsysmt as msm

     molecular_system = msm.convert('1BRS', selection='molecule_type=="protein"')
     msm.info(molecular_system, element='molecule')
     msm.view(molecular_system, selection='molecule_index==0')
     ```
   - *Requirement:* Must use deterministic, small bundled or online PDB examples that run cleanly without heavy computations.

4. **Citation Section:**
   - Section heading: `## Citation`
   - Tabbed block (```{tabs}`) with tabs for **Paper** (BibTeX link) and **Software** (Zenodo citation & BibTeX link).
   - The software citation uses the concept DOI and names the current release version.
     Direct readers to Zenodo when they need the DOI for one exact archived version.

5. **Hidden Sidebar Navigation Tree (`toctree`):**
   - Must maintain hidden toctrees referencing top-level sections:
     - `content/about/index.md`
     - `content/showcase/index.md`
     - `content/user/index.md`
     - `content/developer/index.md`
     - `api/index.md`
     - `content/ai_assistant.md`

---

## 🏷️ Section Anchors

- Top anchor: `(index-top)=`
- Install section anchor: `(index-install)=`
- Usage section anchor: `(index-use)=`
- Citation section anchor: `(index-citation)=`
