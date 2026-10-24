(user-foundations-support-forms-strings)=
# Strings

String forms in MolSysMT allow users to pass textual representations—ranging from PDB text buffers and chemical SMILES strings to database accession IDs and amino acid sequences—directly into API functions.

---

| String Form | Example Format / Content | Target Interpretation |
| :--- | :--- | :--- |
| **`string:pdb_text`** | Multi-line PDB formatted string | Parsed directly as a complete PDB structure in memory. |
| **`string:pdb_id`** | `"1TUP"`, `"4INS"` | Fetches structure dynamically from the RCSB Protein Data Bank. |
| **`string:uniprot_id`** | `"P04637"` | Fetches protein sequence and metadata from UniProt. |
| **`string:alphafold_id`** | `"AF-P04637-F1"` | Fetches predicted 3D structure from the AlphaFold DB. |
| **`string:smiles`** | `"CC(=O)OC1=CC=CC=C1C(=O)O"` | Parsed into small molecule topology and conformers via RDKit/OpenFF. |
| **`string:amino_acids_1`** | `"ACDEFGHIKLMNPQRSTVWY"` | Native one-letter sequence-group representation. |
| **`string:amino_acids_3`** | `"AlaCysAspGluPhe"` | Native concatenated three-letter sequence-group representation. |


## Native sequence groups

Recognition, extraction and translation between one- and three-letter strings are
native operations. Biopython is optional when explicitly requesting Bio.Seq or
Bio.SeqRecord, and for alignment algorithms that use it. These output conversions
do not make Biopython the default string parser.

Sequence indices address original groups, including terminal caps in a
three-letter source. Select groups first; caps contribute no amino-acid letter
when converting to one-letter text or Biopython. Order and repeated positions
remain meaningful. Explicit format prefixes are removed before constructing a
Biopython sequence; empty string outputs retain their alphabet prefix. Empty
Biopython objects are valid, while empty selections for sequence alignment or
identity remain invalid. See {ref}`Cookbook_Sequence_source_groups`.
