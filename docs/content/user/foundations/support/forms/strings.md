(user-foundations-support-forms-strings)=
# Strings

String forms in MolSysMT allow users to pass textual representations—ranging from PDB text buffers and chemical SMILES strings to database accession IDs and amino acid sequences—directly into API functions.

---

## Supported Strings

| String Form | Example Format / Content | Target Interpretation |
| :--- | :--- | :--- |
| **`string:pdb_text`** | Multi-line PDB formatted string | Parsed directly as a complete PDB structure in memory. |
| **`string:pdb_id`** | `"1TUP"`, `"4INS"` | Fetches structure dynamically from the RCSB Protein Data Bank. |
| **`string:uniprot_id`** | `"P04637"` | Fetches protein sequence and metadata from UniProt. |
| **`string:alphafold_id`** | `"AF-P04637-F1"` | Fetches predicted 3D structure from the AlphaFold DB. |
| **`string:smiles`** | `"CC(=O)OC1=CC=CC=C1C(=O)O"` | Parsed into small molecule topology and conformers via RDKit/OpenFF. |
| **`string:amino_acids_1`** | `"ACDEFGHIKLMNPQRSTVWY"` | 1-letter amino acid sequence parsed into peptide topology. |
| **`string:amino_acids_3`** | `"ALA-CYS-ASP-GLU-PHE"` | 3-letter amino acid sequence parsed into peptide topology. |
