# Competitive Landscape and Vision

MolSysMT aims to provide a form-agnostic, unit-aware interface across molecular
data representations, analysis kernels, builders, optional third-party engines,
and visualization. This is a strategic direction, not evidence that MolSysMT
already supersedes mature specialist libraries.

The dated March 2026 comparison and capability inventory are archived under
`archive/assessments/` because several absolute claims were not reproducibly
supported and implementation status has changed.

## Comparison classes

MolSysMT does not sit in one category, so "how does it compare" has no single answer
until the reference class is chosen. Naming that class is a decision, and it belongs to
whoever writes the manuscript
([`pending_proposals/paper_main_tex_is_an_unfilled_template_and_the_manuscript_argument_is_unrecorded.md`](pending_proposals/paper_main_tex_is_an_unfilled_template_and_the_manuscript_argument_is_unrecorded.md)).
Four classes answer *what is it like*, in decreasing order of how crowded they are. A
fifth answers *what is it for*, and it reframes the other four.

**Trajectory analysis.** MDAnalysis, MDTraj, pytraj/cpptraj, LOOS. Mature, widely cited,
and not the ground MolSysMT is contesting.

**Unified molecular-system abstraction** — a native object model, many input formats, a
selection language, and analysis over the same abstraction. **Biotite** and **ProDy** are
the closest architectural analogues in structural biology, together with MDAnalysis.
Outside the domain, ASE and pymatgen are the same pattern in materials science, and their
adoption is the evidence that the abstraction wins where it wins.

- **Biotite** builds on a unified array-based structure representation with compiled
  inner loops, covers a broad set of structural-biology formats and analyses, is
  peer-reviewed and team-maintained. It is the nearest comparison on engineering and on
  scope of the abstraction.
- **ProDy** builds on a unified atom-group representation with a powerful selection
  language, and is long-established in normal-mode and ensemble analysis. It is the
  nearest comparison on the selection-and-attribute interface.

**Programmatic structure preparation** without requiring a simulation engine. PDBFixer is
the main Python-native incumbent and is narrow and tied to OpenMM; the alternatives
(tleap, `gmx pdb2gmx`, pdb2pqr, CHARMM-GUI, Modeller, pmx) are command-line, web, or
domain-specific. This is the thinnest class and the one where MolSysMT's `build`
namespace has the least-occupied ground — conditional on that namespace acquiring
governed evidence, which it does not have today
([`pending_proposals/the_evidence_matrix_cannot_show_the_surfaces_the_manuscript_will_lead_with.md`](pending_proposals/the_evidence_matrix_cannot_show_the_surfaces_the_manuscript_will_lead_with.md)).

**Conversion with declared fidelity.** InterMol pursued validated MD-input conversion and
is dormant; ParmEd converts widely without reporting loss; MDAnalysis exposes
`convert_to()` without a fidelity record. No occupied position was identified.

**Substrate for a tool ecosystem.** MolSysMT is the core of MolSysSuite: MolSysViewer
coordinates with it, MolSys-AI is built on it, and TopoMT, PharmacophoreMT and ElasNetMT
consume it. On that axis the analogues are not structural-biology libraries at all — they
are **ASE** in materials, **RDKit** in cheminformatics, **OpenMM** with its plugin
interface, and **MDAnalysis** with the MDAKits ecosystem. Each became a substrate rather
than a library, and each is judged by whether third parties build on it, not by beating a
specialist at one task.

This class changes how the previous four should be read:

- Breadth of accepted forms stops being a headline count and becomes the ingestion
  surface every downstream tool inherits.
- Conversion with declared fidelity stops being a feature and becomes the mechanism that
  makes the ecosystem possible: tools cannot exchange molecular systems across
  heterogeneous representations unless the conversions state what they lose.
- The governance apparatus — stability registry, support tiers, shared reporting
  protocol, cross-repository issue references, a shared unit policy — stops looking
  disproportionate for one library and becomes the minimum coordination for six
  repositories. The recurring cross-repository unit-policy failures are that problem
  appearing, not a fragile test.

One caveat is load-bearing and belongs in any claim made on this axis: **no third party
outside UIBCDF is known to build on MolSysMT.** ASE and RDKit are substrates because
outsiders adopted them. A suite of tools by the same authors demonstrates that the
abstraction serves its authors. Until external adoption exists, the substrate position is
a statement of design intent, and it must be made as one.

These are positioning statements, not measurements. **No reproducible comparison against
Biotite or ProDy has been run.** Until one exists under the dimensions below, this
section says which tools a reader will have in mind, not how MolSysMT scores against
them, and the substrate class carries the further caveat above. Biotite and ProDy were
absent from this document before 2026-08-19, which is why the external
audit of that date flagged the omission: a referee in this field knows them, and a
related-work section that compares only against MDTraj and MDAnalysis invites the
question in the first round.

## Evidence-based comparison dimensions

External comparisons should use reproducible workflows and current releases:

- accepted data forms and conversion fidelity;
- topology, trajectory, and selection semantics;
- units and numerical precision;
- analysis breadth and scientific parity;
- building and repair behavior;
- eager, chunked, CPU-parallel, and GPU execution;
- optional-dependency isolation and import cost;
- diagnostics and failure integrity;
- documentation, examples, release cadence, and community adoption.

Architectural breadth is a strength only when capability claims are backed by
delivery tests. Delegating to a backend does not automatically provide uniform
semantics, errors, units, or support across all input forms.

## Current differentiators worth strengthening

- a common molecular-system abstraction and conversion ecosystem;
- native topology/structure separation and declarative forms;
- selection and attribute access across multiple representations;
- integrated construction, analysis, visualization, and unit handling;
- explicit soft-dependency management;
- an educational course organized around scientific workflows.

## Current credibility constraints

The highest-value improvements are reliability rather than more headline
features: explicit form tiers, attribute-delivery validation, conversion
fidelity metadata, scientific reference tests, failure-safe heavy execution,
API stability governance, and executable documentation synchronization.

Any future scorecard should include the compared versions, environment, test
systems, exact commands, raw results, and known unsupported cases. Marketing
language must not be promoted into a normative developer contract.
