---
summary: Expose explicit CIP stereochemistry analysis for reusable chemical workflows
issue: uibcdf/molsysmt#299
status: resolved
opened: 2026-10-02
closed: 2026-10-03
verification: reproduced
area: [api, attribute]
guard: tests/physchem/test_get_cip_stereochemistry.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Exposing reusable CIP analysis

**Reported:** 2026-10-02, during the SDF interoperability work requested by
DockingMT and the maintainer's request to expose useful general tools.
**Status:** Resolved on 2026-10-03 with public documentation, focused scientific
guards, explicit SDF integration and the accurate RDKit adapter primitive.

## What

Expose `physchem.get_cip_stereochemistry` as an experimental, form-agnostic,
read-only scientific analysis. Share its accurate assignment primitive with
explicitly enabled SDF stereo conversion and existing RDKit adapters. Track
the format work separately in uibcdf/molsysmt#215; PDBQT remains #214.

## How

The method is `hanson_2018`, DOI 10.1021/acs.jcim.8b00324, and the explicit
optional provider is RDKit's accurate `rdCIPLabeler`. The public boundary uses
argument digestion, dependency guarding, source-index selection and complete
chemical graph validation. Ranking precedes selection. Native element symbols
and explicit charges/orders are required; atom names and force-field types
are not guessed. State selection does not change the source reference state.

The dictionary separates atom R/S and r/s, absolute double-bond E/Z, and
cis/trans relative to named source reference atoms. Native SDF double bonds
retain the latter relationship. Empty arrays have defined shapes and dtypes.
Optional coordinate inference requires exactly one structure, finite positions
and explicit PyUnitWizard conversion to angstroms. It does not reconstruct PBC.

RDKit adapters analyze copies and use the accurate primitive. Native-to-RDKit
encoding verifies stored CIP labels, including dependent pseudoasymmetric
centers, rather than assuming that a clockwise tag means R. A legacy cleanup
operation was found to erase native cis/trans declarations without bond-direction
flags. Preserving those declared tags fixes both E/Z and dependent CIP ranking.

SDF converters add keyword-only `stereo_engine=None`. The default remains
native and rejects active stereo. Explicit 'rdkit' preserves source atom axes
and hydrogen atoms, assigns before extraction, and verifies serialized stereo
before opening the destination. Query, enhanced and non-tetrahedral stereo
remain excluded. Uninterpretable parity-only declarations raise. Reports from
`convert(..., return_report=True)` account for the explicit verified writer;
standalone preflight queries describe the ordinary default route.

Successful public analysis retains detached bibliography and producer versions
and contributes to the application's current Ackredit session. Optional absence
or provider failure preserves completed science; no hooks or isolated sessions
are enabled. Utilities outside the scientific boundary need no attribution.

## Why

CTAB wedge/parity integers are relative encoding data, not absolute R/S labels.
A full CIP implementation needs ring duplication, isotopes and stereochemical
sequence rules. Hiding an incomplete labeler inside an SDF adapter would create
a competing chemical interpretation and prevent reuse in docking, validation
and state comparison.

## What is measured and what is assumed

Measured focused command:

```bash
python -m pytest --receptor=llm tests/physchem/test_get_cip_stereochemistry.py tests/form/file_sdf/test_stereochemistry.py --doctest-modules molsysmt/physchem/get_cip_stereochemistry.py -q
```

Final focused command (2026-10-03):

```bash
python -m pytest --receptor=llm tests/physchem/test_get_cip_stereochemistry.py tests/form/file_sdf/test_stereochemistry.py tests/form/rdkit_Mol/test_chemical_metadata.py tests/basic/test_get_conversion_report.py --doctest-modules molsysmt/physchem/get_cip_stereochemistry.py -q
```

Result: **51 passed in 22.81 seconds**. An earlier broader 791-test run had
790 passes and one failure: the accurate labeler normalized a declared E/Z
adapter tag to cis/trans. Preserving the original RDKit bond representation
while keeping accurate atom labels fixed that regression; the failing test
and all focused integration cases pass in the final command above. This record
does not claim a final 791-test green rerun.

The documentation HTML build passed with existing warnings, and API registry,
public signature guard, dependencies, form adapters, docstrings, developer guide,
course structure and Ruff checks passed. The two course changes are narrative;
existing executable cells and outputs are preserved.
Expected labels include L-alanine S, L-cysteine R, isotope tie-breaking,
E/Z and the Salome Rieder para-stereochemistry example from RDKit's independent
CIPLabeler tests (R/r/S at source indices 3/7/9). The existing 46-record SDF
corpus is achiral and is not evidence for general stereo coverage. No throughput
or universal CIP implementation claim is made.

## What was refuted

- Copying CTAB flags into CIP fields cannot preserve chemical configurations.
- RDKit's legacy approximate assignment is insufficient for pseudoasymmetry.
- A reference pair is not necessarily the highest-priority pair; relative
  cis/trans and absolute E/Z must remain separate.
- Cleaning all stereo tags during assignment can erase declared cis/trans
  relationships. The accurate labeler is applied without that destructive cleanup.
- A new partial native CIP algorithm is not justified by simple chiral examples;
  the explicit established optional provider is the bounded first implementation.

## Scope and exclusions

The tool covers supported tetrahedral and double-bond descriptors, not priority
tables, enhanced/relative-group modeling, stereoisomer enumeration or periodic
reconstruction. It does not make the SDF adapter a docking preparation pipeline.
PDBQT typing, torsion trees and full native metadata are independent work.

## Acceptance criteria

- Form-agnostic public validation, source immutability, full-graph ranking,
  source-index output, empty shapes and independent expected labels pass.
- Coordinate inference passes under alternate input units and a non-default
  application unit policy; multiple structures fail.
- Explicit SDF stereo round trips preserve labels, geometry and atom axes;
  the default remains dependency-free and rejects unsupported declarations.
- Real Ackredit reuse/enclosing scope, genuine absence, failure and detached
  bibliography tests pass without affecting scientific results.
- Docstrings, User Guide, Cookbook, applicable course modules and public API
  classification describe the bounded experimental behavior.

## Provenance

Linux development environment, Python 3.13.14, RDKit 2025.09.5, 2026-10-03.
This editable-environment evidence does not establish installed package support
on other Python minors or a published Ackredit dependency closure.

## Resolution

The public tool and explicitly enabled SDF adapter route satisfy this bounded
proposal. The module guard covers absolute labels, pseudoasymmetric dependencies,
source immutability, indexed selections, unit conversion, unsupported graphs and
optional attribution. Format-specific round trips and preflight options have
separate guards in `tests/form/file_sdf/test_stereochemistry.py`. Durable rules
live in [forms_and_conversions.md](../../forms_and_conversions.md). The broader
SDF validation and PDBQT representation work remain open under #215 and #214.
