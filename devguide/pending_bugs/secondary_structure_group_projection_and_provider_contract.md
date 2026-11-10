---
summary: Secondary-structure adapter loses requested group order and lacks explicit provider boundary.
issue: uibcdf/molsysmt#694
status: active
opened: 2026-11-10
closed:
severity: high
verification: reproduced
area: [structure, units]
guard: tests/structure/get_secondary_structure/test_public_contract.py
normative:
blocked_by: []
supersedes: []
---

# Secondary-structure output loses selected-group correspondence

## What / How / Why

The original protected five-case receiving on 6bd879bda fails all five cases:
MolSysMT selections [3,1,3] lose repetition/order through np.unique; the MDTraj
syntax returns NumPy indices and reaches an ambiguous array/string truth test;
the public signature also lacks explicit skip_digestion/execution controls.
Four old tests check only full-system shapes/vocabulary/counts and miss this.
The optional MDTraj import has no direct provider guard. These defects precede
the pending #421 categorical report; the GUI must not repair or clone science.

## Implementation and criteria

Validate/project groups on their own source axis, retain explicit order and
repetitions on both axes, and compute DSSP in the complete molecular context.
Expose normal argument/provider/diagnostic boundaries, defined empty shapes,
source preservation and actual criterion/software credit. Use the registered
ChunkedExecutor for required large native/H5 coordinate reads; admit resident
labels explicitly. Foreign eager inputs retain their public conversion route;
force/large inputs without registered chunk support fail clearly. The first
attempt to use a foreign MDTraj iterator through the dictionary executor exposes
its unsupported output_type parameter; no heavy-support promise is fabricated.

Receive native forms/file/complementary contexts, both label vocabularies,
nonconsecutive/repeated axes, active units, empty/error/budget cases and actual
Ackredit/absence. Keep provider parity distinct from independent DSSP accuracy:
the governed scientific-evidence gap remains. MDTraj's implementation, based on
DSSP 2.2.0 and Kabsch–Sander (1983), owns the method; no MolSysMT criterion,
sequence prediction, new precision guarantee or scientific promotion is added.

The panel reports categorical codes with group and structure indices, actual
provider version and complete participant membership. A quoted blank is the
full DSSP loop code, and NA retains the provider's missing-backbone meaning.
No scalar color, occupancy/trajectory reduction, coordinate repair or hidden
periodic reconstruction is inferred. Native/HTML/Jupyter/representative Qt
receiving and lifecycle documentation remain required before closure/credit.

## Evidence history and scope

The initial correction has a local helper-call arity error (four fail/one pass),
then 23 passes/one foreign-iterator failure. The corrected eager/registered-chunked
routes pass all 24 original expanded controls. Expanded native/panel receiving
has 29 passes/four new fixture-key failures; the fixture now asserts the actual
selected_plot_unavailable field. Original outcomes remain preserved. Deliberate
tiny numerical-budget fixtures emit process-RSS warnings; these are not observed
shared-host memory pressure. Every process uses finite cgroup/resource controls.
No dependency floor, Rust backend, schema, package/tag/Release or remote matrix
changes. The eight remaining original GUI intents and all original weights stay
unchanged until their own receiving; supplemental fixes add no bonus.


## Directed receiving — 2026-11-10

All 33 expanded native/provider/panel cases pass after correcting the fixture's
field name. This includes group/structure repetitions, full-context backend
parity, nm/pm policies, actual native/H5 chunking, eager foreign inputs, empty
axes, invalid controls, configured admission, provider absence through the real
DepDigest checker and real Ackredit criterion/version capture. The complete
source, docstring/tutorial and graphical receiving follow on a clean cohort.


## Clean receiving and first browser attempt — 2026-11-10

Clean 707ea24b2 passes 186 affected cases, 116 registered scientific cases /
74 nodes, fourteen fast gates, the one-process HTML build and the representative
native Qt properties guard (seven checks). The first Jupyter workflow reaches
the exact DSSP values/axes but fails while reading innerText from a closed
provenance details element. The browser guard now opens that actual user control
before asserting visible provider text. The failed attempt is retained; no
deadline or scientific expectation is weakened.
