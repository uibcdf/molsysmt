# Forms and Conversions

## Form Adapters
Form adapters live under `molsysmt/form`. Each form module must define:
- `form_name`
- `form_type`
- `form_info`
- `_convert_to` dictionary where keys are form names and values are **strings** of the converter function names (e.g., `'to_molsysmt_MolSys'`).

## Lazy Discovery
Forms are discovered lazily. Mapping from form directory to dependency lives in
`molsysmt/_depdigest.py` (see `SPEC_DEPENDENCIES.md`).

### Conversion Path Resolution
1. When `msm.convert(A, to_form='B')` is called, the system calculates the shortest path in the conversion graph.
2. The values in `_convert_to` are strings to prevent loading submodule code until the edge in the graph is actually traversed.
3. The function `molsysmt.basic.convert._convert_one_to_one` handles the dynamic import of these string-named functions.

## Conversion Rules
- **Polymorphism in Handlers**: Native file handlers (`H5MSMFileHandler`, `PDBFileHandler`) must be able to instantiate themselves from a file path string during conversion to ensure long chains of `msm.convert` don't break.
- **Unit Standardization**: Every converter must use `PyUnitWizard` to ensure outputs are in MolSysMT standard units (nanometers, degrees, picoseconds).
- **ID Normalization**: All topological IDs (atom_id, group_id, etc.) must be converted to strings during ingestion to ensure uniform behavior across forms.

## Key 1.0.0 Additions
The following "Hardened" forms were added or finalized during the 1.0.0 sprint:
- **`rdkit.Mol`**: Full support for cheminformatics-grade molecules, including bond orders and conformers.
- **`biopython.PDBStructure`**: Support for BioPython's `Bio.PDB.Structure` objects.
- **`MDAnalysis.AtomGroup`**: Direct support for MDAnalysis selections without full Universe conversion.
- **`molsysviewer.MolSysView`**: The official viewer is now a first-class molecular system.
