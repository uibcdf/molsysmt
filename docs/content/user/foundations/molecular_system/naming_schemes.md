(user-foundations-group-naming-schemes)=
# Group naming schemes

:::{warning}
Development under [MolSysMT #549](https://github.com/uibcdf/molsysmt/issues/549)
is staged. Native group-aligned declarations and their dictionary/H5MSM transport
are implemented. The helper at `msm.element.group.get_1_letter_code_from_name`
and native sequence conversion use the declared convention. Sequence identity
and direct three-to-one-letter projection share that interpretation; alignment
uses native sequence conversion. Reference-parent reporting, amino-acid recognition, native group-type
reconstruction and non-standard-group reports now share the resolver.
Native atom/H expectations, missing-atom queries and bounded native preparation
now consume naming context too. Reference-bond maps and native missing-bond
candidates also use that context. Broader producer audits, external naming
adapters and the older scalar one-letter helper still await coordinated migration.
The general `from_naming_scheme` conversion
argument is available for explicit source interpretation and native transport.
:::

A group name is a label interpreted in a naming scheme. Identical labels can
refer to different compounds in a chemical dictionary and a force-field
vocabulary. A naming scheme explains the label; chemical assignments remain
stored independently in `ChemicalStates`.

## Schemes and scope

The native declaration vocabulary defines four explicit identifiers. Storing
one records the source vocabulary; it does not establish that every name in
that vocabulary is supported by a name resolver or a preparation method.

| Identifier | Intended meaning | Coverage and limits |
| --- | --- | --- |
| `sequence` | The shared DDBJ amino-acid code alphabet, including ambiguity symbols. | All 26 declared codes; XAA/XLE mean X/J. This is a sequence alphabet, not a chemical-component catalogue or atomic template inventory. |
| `amber` | The explicitly supported Amber peptide-state vocabulary, including GLH, HID/HIE/HIP, ASH, CYM/CYX and LYN. | Names describe reference states. Selecting this vocabulary does not prepare, protonate or parameterize a system. Other force-field naming schemes are not implied. |
| `ccd` | Component identifiers interpreted against a declared, pinned wwPDB Chemical Component Dictionary reference. | A component may be a peptide group or a non-peptide compound. Initial admitted entries must be curated and documented; full-dictionary coverage is not established by this review. |
| `legacy` | The existing MolSysMT parent/code table inherited from historical MDTraj mappings. | Explicit compatibility interpretation. It is a mixed historical catalogue, not a certified current CCD snapshot or a general Amber vocabulary. Some state names are absent and some mappings remain scientifically unverified. |

Profile version 1 admits 26 sequence symbols, twenty standard plus eight state
names for Amber, and 36 inspected CCD records (thirty peptide projections and six
non-peptide entries) from 4 November 2026. CCD support does not fall back to the
legacy table. The bundled generator/receipt retains source names, types, parents,
URLs and response digests. Recognizing a name does not establish an atomic
builder template or a certified complete CCD/Amber implementation.

## Important differences

This comparison records the bounded source review of 4 November 2026. The Amber
column describes names in its peptide vocabulary; the CCD column describes
independently inspected component records. The last column reports the current
legacy parent/code helper table, not all group-recognition machinery.

| Label | Amber interpretation | CCD record inspected | Legacy parent / letter |
| --- | --- | --- | --- |
| `GLH` | Protonated glutamate; parent GLU / E. | No record verified in this review. | GLN / Q; this does not justify applying Q to the native GLH template. |
| `HID` | Histidine with the delta-nitrogen H; parent HIS / H. | A hydroxyindole-acetate compound; non-polymer. | Absent. |
| `HIE` | Histidine with the epsilon-nitrogen H; parent HIS / H. | No record verified in this review. | Absent. |
| `HIP` | Doubly protonated histidine; parent HIS / H. | Phosphonohistidine; peptide-linking, parent HIS. | HIS / H. |
| `ASH` | Protonated aspartate; parent ASP / D. | A non-peptide heterocyclic ligand. | ASP / D. |
| `CYM` | Deprotonated cysteine; parent CYS / C. | No record verified in this review. | CYS / C. |
| `CYX` | Cysteine participating in a disulfide; parent CYS / C. | A non-peptide phosphorus-containing compound. | Absent. |
| `LYN` | Neutral lysine; parent LYS / K. | Lysine amide; peptide-linking, parent LYS. | LYS / K. |
| `XAA` | Outside the bounded Amber profile. | A non-peptide amino-thiazole compound. | XAA / X; also X in the sequence alphabet. |
| `XLE` | Outside the bounded Amber profile. | A non-peptide sulfonamide compound. | XLE / J through the shared alphabet; also J under sequence. |

The CCD requests for GLH, HIE and CYM returned HTTP 404 during this review.
That observation is not proof of absence from every historical or future
dictionary and cannot establish a default naming scheme.

A shared parent letter does not make chemical identities equivalent: the HIP
and LYN examples retain distinct meanings even where their parent letters agree.
Sequence projection must never become an implicit chemical substitution.

Primary references include the
[DDBJ sequence alphabet](https://www.ddbj.nig.ac.jp/ddbj/code-e.html),
[Amber naming table](https://dev-archive.ambermd.org/200603/att-0122/amber9.pdf),
[PDB2PQR naming documentation](https://pdb2pqr.readthedocs.io/en/v3.3.0/formats/xml-names.html)
and the independently inspected RCSB records for
[HID](https://www.rcsb.org/ligand/HID),
[HIP](https://www.rcsb.org/ligand/HIP),
[ASH](https://www.rcsb.org/ligand/ASH),
[CYX](https://www.rcsb.org/ligand/CYX) and
[LYN](https://www.rcsb.org/ligand/LYN).
The additional [XAA](https://www.rcsb.org/ligand/XAA) and
[XLE](https://www.rcsb.org/ligand/XLE) records establish why the sequence alphabet
has its own convention. The reviewed [MSE](https://www.rcsb.org/ligand/MSE),
[SEP](https://www.rcsb.org/ligand/SEP), [TPO](https://www.rcsb.org/ligand/TPO)
and [PTR](https://www.rcsb.org/ligand/PTR) records retain their peptide parents;
projecting a letter does not replace the modified chemical group.
The owning issue retains exact source revisions and inspection evidence.

## Default interpretation

Native sequence projection preserves names and reads stored group declarations.
The scalar helper takes its convention explicitly because it has no molecular
container. Without context it admits 24 unambiguous alphabet labels (excluding
XAA/XLE) and the four reviewed matching MSE/SEP/TPO/PTR parent projections.
Other unassessed meanings need explicit context. A missing declaration remains
unknown, including when reading older native files.

Without a declaration, only names whose interpretation is supported and
unambiguous may resolve. The state-label set above and XAA/XLE require an explicit
or stored scheme. Ambiguous or unassessed meanings require a diagnostic rather
than silently choosing Amber, CCD or the legacy table. Canonical amino-acid
names remain usable without repeating a scheme where their interpretation is
unambiguous for the requested operation.

The conversion argument is `from_naming_scheme`; the direct name helper
uses `naming_scheme`. There is no global session preference. Ordinary conversion
preserves existing labels. Translating labels into another scheme is a distinct
explicit operation, not an implicit side effect of sequence projection.
An explicit source convention must agree with every known declaration in the
selected groups, even when the resulting letters would coincide. A sequence
query leaves the source declarations unchanged. A native molecular output
retains the explicit declaration for its selected groups; when this adds missing
context, the result owns a separate topology even if sharing was requested.
The old input and its interaction analyses remain unchanged.

For a one-letter projection, explicit group positions preserve ordering and
repetitions. Molecular conversion retains the ordinary atom-selection contract
and maps selected atoms to their source groups. Sequence text can construct new
group slots from repeated source positions. Extracting an existing group-only
native inventory uses unique group positions, preserving its source labels and
order through the general hierarchy tool. Neither creates an atomic axis.
Conflicting unselected groups
do not prevent either operation. A native sequence query needs neither a
coordinate copy nor a chemical-state copy. Non-native inputs use their
registered native conversion route; this does not promise selective file I/O.

Sequence identity retains naming context and the original positions supplying
letters, including reordered or repeated groups. With all-group or index
selections, typed dictionaries decode only topology and H5MSM 0.5 requests only
that layer. A predicate that needs other domains keeps the ordinary selection
route. Sequence-only three-letter inputs use the sequence alphabet for canonical
symbols; other meanings need assessed unambiguous or explicit context. Unsupported
or context-dependent names never acquire the historical mapping implicitly.

## Mixed systems

The declaration belongs with group names in `Topology` and can differ between
groups. A system may combine an Amber-labelled protein and a CCD-labelled
ligand. File format, Python class, group IDs and matching atom counts do not
establish a common naming scheme.

Native declarations use one byte per group when any convention is known. If all
groups are unknown, no code vector is stored. An immutable group-index-ordered
view exposes the declared identifiers or `None`. New groups begin unknown;
copying, selection and merging retain each existing group's declaration.
Rebuilding a name-preserving hierarchy does not choose another convention.

Changing a declaration on an attached topology invalidates its named interaction
analyses, including evaluated-empty coverage. Previously held analyses remain
snapshots, coordinates are not copied and detectors are not run. Repeating the
same declaration is a no-op. Raw table mutation is not a coordinated editing
interface; a mismatched group axis is rejected rather than silently realigned.

The native and persistence contract preserves declarations through copying,
selection, reordering, combination and H5MSM round trips. Known declarations
select TopologyDict schema 0.3 and topology layer 4 inside H5MSM 0.5. Their
versioned registry prevents a reader from silently changing code meanings.
Existing H5MSM files do not acquire an invented scheme when loaded. Preparation
history records past operations and cannot substitute for a current declaration
after later edits.

Chemical-state selection does not rename stable groups. Changing the label's
interpretation does not itself change bonds, charge, coordinates or protonation.

## Recognition and parents

Reference-parent reporting and name recognition share the bounded naming
profiles. For example, GLH reports GLU under Amber and GLN under explicit legacy;
HID is recognized as an amino acid under Amber and as a small molecule under CCD.
A missing or unassessed type stays unknown. A negative amino-acid recognition
means that this profile does not recognize the label, not that the compound's
chemistry has been established as non-peptide. A scalar parent request with an
explicit but unsupported profile/name pair raises an error.

Raw molecular readers preserve ambiguous labels without choosing a convention;
their inferred group type is unknown. This permits loading the inventory before
a source declaration is available. A subsequent declaration is metadata only:
it does not rename groups, recompute stored types, repair chemistry or repartition
stable molecules. Native sequence queries can interpret a declared, assessed
amino acid whose stored type is unknown. Native type queries can request new
inference without editing the input; explicit group reconstruction writes types
using each group's stored convention. Existing stable molecule membership stays
unchanged in both cases.

A reference parent never establishes chemical-template equivalence. In
particular, CCD HIP/LYN share sequence parents with Amber labels while denoting
different compounds. Preparation and exact-template receiving remain separate
work under #549; these recognition changes do not certify their completion.
See the executed {ref}`parent examples <Tutorial_Get_standard_name>`,
{ref}`recognition examples <Tutorial_Is_amino_acid>` and
{ref}`type examples <Tutorial_Get_group_type_from_group_name>`.

## Chemical reference limits

Preparation does not use sequence parents as chemical templates. The historical
raw atom/bond catalogue mixes sources, including distinct compounds stored under
GLH, HIP, CYM and LYN. The named Amber-state reference layer retains only variants
whose heavy connectivity and per-parent H counts match the bundled Meeko-derived
fragments; labels alone cannot select a raw variant. Standard twenty names retain
the existing catalogue/pH behavior, while MSE/SEP/TPO/MLY have separate CCD-derived
heavy-only references. A source declaration does not itself validate ChemicalStates.

The eight state references currently cover internal peptide groups. Named-state
terminal H completion and unsupported layouts remain unassessed. A supported
inventory does not imply that coordinate placement is verified. The standard pH
and placement models retain their existing approximations. Raw catalogue access
is available for inspection, not as an automatic state selector.

Native molecular operations read group declarations; an audit can preserve an
ambiguous group as unassessed. OpenMM/PDBFixer naming adapters for the reviewed
contextual labels are not delivered, so the wrappers refuse those labels and
incompatible declarations on curated modified names. Only selected groups are
checked where selection is offered. Fixed-state preparation instead follows
ChemicalStates without interpreting group labels chemically.

Template-based bond candidates require the source convention too. They do not
turn ambiguous labels into unknown groups for untyped distance fallback. Declared
Amber states use verified layouts and local inferred types, preserving stored
type metadata. The PyTraj route requires explicit Amber context for the reviewed
state labels. Pure geometry remains a separate choice that does not select a
naming template; geometric candidates do not certify chemical bonds.

Raw readers remain permissive: they preserve supplied names and explicit edges,
while omitting automatic candidate inference for groups whose reviewed contextual
labels lack declarations. Such omitted connectivity is not labelled complete.
A later explicit template query requires the convention and can use the checked
reference; loading a file does not choose it implicitly.
