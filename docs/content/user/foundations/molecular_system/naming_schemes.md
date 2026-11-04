(user-foundations-group-naming-schemes)=
# Group naming schemes

:::{warning}
The contract below is accepted for development under
[MolSysMT #549](https://github.com/uibcdf/molsysmt/issues/549).
Explicit scheme arguments and scheme persistence are not implemented on the
reviewed source `5f3af9374`. The existing name/code helpers still use the legacy
table. This page distinguishes that behavior from the planned scheme-aware API.
:::

A group name is a label interpreted in a naming scheme. Identical labels can
refer to different compounds in a chemical dictionary and a force-field
vocabulary. A naming scheme explains the label; chemical assignments remain
stored independently in `ChemicalStates`.

## Schemes and scope

The initial development scope defines three explicit identifiers. None is an
additional runtime-selectable option on the reviewed source.

| Identifier | Intended meaning | Coverage and limits |
| --- | --- | --- |
| `amber` | The explicitly supported Amber peptide-state vocabulary, including GLH, HID/HIE/HIP, ASH, CYM/CYX and LYN. | Names describe reference states. Selecting this vocabulary does not prepare, protonate or parameterize a system. Other force-field naming schemes are not implied. |
| `ccd` | Component identifiers interpreted against a declared, pinned wwPDB Chemical Component Dictionary reference. | A component may be a peptide group or a non-peptide compound. Initial admitted entries must be curated and documented; full-dictionary coverage is not established by this review. |
| `legacy` | The existing MolSysMT parent/code table inherited from historical MDTraj mappings. | Explicit compatibility interpretation. It is a mixed historical catalogue, not a certified current CCD snapshot or a general Amber vocabulary. Some state names are absent and some mappings remain scientifically unverified. |

The public documentation must report each implemented scheme's definition
version, reference snapshot, accepted names, unsupported cases and migration
behavior as development proceeds. Recognition of a name alone does not establish
that an atomic template or preparation method supports it.

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

The CCD requests for GLH, HIE and CYM returned HTTP 404 during this review.
That observation is not proof of absence from every historical or future
dictionary and cannot establish a default naming scheme.

A shared parent letter does not make chemical identities equivalent: the HIP
and LYN examples retain distinct meanings even where their parent letters agree.
Sequence projection must never become an implicit chemical substitution.

Primary references include the
[Amber naming table](https://dev-archive.ambermd.org/200603/att-0122/amber9.pdf),
[PDB2PQR naming documentation](https://pdb2pqr.readthedocs.io/en/v3.3.0/formats/xml-names.html)
and the independently inspected RCSB records for
[HID](https://www.rcsb.org/ligand/HID),
[HIP](https://www.rcsb.org/ligand/HIP),
[ASH](https://www.rcsb.org/ligand/ASH),
[CYX](https://www.rcsb.org/ligand/CYX) and
[LYN](https://www.rcsb.org/ligand/LYN).
The owning issue retains exact source revisions and inspection evidence.

## Default interpretation

The accepted target behavior preserves names and uses a stored naming-scheme
declaration where available. An explicit source declaration supplies missing
context; contradictions with stored declarations must be diagnosed. A missing
declaration remains unknown, including when reading older native files.

Without a declaration, only names whose interpretation is supported and
unambiguous may resolve. The initial state-label set above requires an explicit
or stored scheme. Ambiguous or unassessed meanings require a diagnostic rather
than silently choosing Amber, CCD or the legacy table. Canonical amino-acid
names remain usable without repeating a scheme where their interpretation is
unambiguous for the requested operation.

The planned conversion argument is `from_naming_scheme`; the direct name helper
uses `naming_scheme`. There is no global session preference. Ordinary conversion
preserves existing labels. Translating labels into another scheme is a distinct
explicit operation, not an implicit side effect of sequence projection.

## Mixed systems

The declaration belongs with group names in `Topology` and can differ between
groups. A system may combine an Amber-labelled protein and a CCD-labelled
ligand. File format, Python class, group IDs and matching atom counts do not
establish a common naming scheme.

The planned native and persistence contract preserves declarations through
copying, selection, reordering, combination and H5MSM round trips. It also covers
native dictionaries. The physical encoding and schema revisions remain part of
implementation design. Existing H5MSM files do not acquire an invented scheme
when loaded. Preparation history records past operations and cannot substitute
for a current declaration after later edits.

Chemical-state selection does not rename stable groups. Changing the label's
interpretation does not itself change bonds, charge, coordinates or protonation.
