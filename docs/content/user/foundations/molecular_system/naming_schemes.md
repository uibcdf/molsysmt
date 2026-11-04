(user-foundations-group-naming-schemes)=
# Group naming schemes

:::{warning}
Development under [MolSysMT #549](https://github.com/uibcdf/molsysmt/issues/549)
is staged. Native group-aligned declarations and their dictionary/H5MSM transport
are implemented. The helper at `msm.element.group.get_1_letter_code_from_name`
and native sequence conversion use the declared convention. The older
`amino_acid` helpers and other classification/preparation/alignment consumers
still await coordinated migration. The general `from_naming_scheme` conversion
argument remains pending.
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

The planned conversion argument is `from_naming_scheme`; the direct name helper
uses `naming_scheme`. There is no global session preference. Ordinary conversion
preserves existing labels. Translating labels into another scheme is a distinct
explicit operation, not an implicit side effect of sequence projection.
The pending source override must diagnose contradictions with stored declarations
rather than silently replacing them.

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
