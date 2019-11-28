# MolMod Elements

The fundamental elements are atoms, groups, components, molecules, entities and bioassemblies. They act as
building blocks of superior elements, defining this way hierarchical organization levels of a
molecular model. A bioassembly is composed by entities with one or more molecules. A molecule is composed by
components, a component by groups, and finnaly a by atoms.

```
atom ---> group ---> component ---> molecule ---> entities ---> bioassembly
```

## Atom

Atoms are the indivisible element of a classical molecular model.

### Main attributes

index: Index (0-based) of atom in main list of atoms of bioassembly.
id: External atom identification integer.
name: atom name.
type: atom type (any element in periodic table).

## Group

Sets of atoms are sometimes defined as building block elements of more complex structures. This is
the case of aminoacids and nucleotides. This is then the immediately superior hierarchical level
over "atoms".

### Main attributes

index: Index (0-based) of group in main list of atoms of bioassembly.
id: External group identification integer.
name: group name.
type: group type (ion, cosolute, water, aminoacid, nucleotide or None).

## Component

Components are composed by one or many groups, and thereby by one or many atoms.
Components are uniquely defined as the set of atoms, and groups, covalently bonded.
The name "component" is taken from graph or network theory where the "components" of a graph or a
network are the connected set of nodes (any node of a component is connected by at least a path of edges to any
other node of the same component). 
Thereby, a polymer made by nucleotides or aminoacids is a component, no matter is a fragment of a protein or one of the strands of a DNA fragment. And in coherence with this definition, an ion, a water molecule or a small molecules are also components.

### Main attributes

index: Index (0-based) of component in main list of atoms of bioassembly.
id: External component identification integer.
name: component name.
type: component type. (ion, cosolute, water, small molecule, polymer or None).

## Molecule

A molecule is composed by one or many components. A protein quaternary structure is composed by more than a polymer of
aminoacids, more than a component. In the same way a fragment of DNA is composed by two nucleotides
strands (components). While a peptide or a single folded protein are made by a single component.
And in coherence with this definition, an ion or a water molecule are perse a molecules composed by
single components.

### Main attributes

index: Index (0-based) of molecule in main list of atoms of bioassembly.
id: External molecule identification integer.
name: molecule name if any.
type: molecule type. (ion, cosolute, water, small molecule, peptide, protein, dna, rna or None).

## Entities

Entities are set of molecules defined by the same molecular nature. Water is an entity made by all
water molecules in the bioassembly, e.g. Or Urea can be another entity present in the molecular
model, or "Epstein Barr Nuclear Antigen 1" or "Trypanosoma Cruzi Triosephosphate Isomerase", no
matter the number of molecules of each nature can be found in the molecular model.

### Main attributes

index: Index (0-based) of entity in the list of all entities defined in the molecular model.
id: External identification integer of chain.
name: chain name if any.
type: entity type. (ion, cosolute, water, small molecule, peptide, protein, dna, rna or None).

## Bioassemblies

The last hierarchical level are bioassemblies. A bioassembly is the arrangement or the assembly of
all other elements. Per se a bioassembly can be a molecular model. But to be precise a molecular
model can be made by differenc bioassembly (see protein data bank).

### Main attributes

index: Index (0-based) of bioassembly in the list of all entities defined in the molecular model.
id: External identification integer of chain.
name: bioassembly name if any.
type: bioassembly type if any.

# Other MolMod set of elements

## Chain

Chains are ambiguously defined. Chain, as thy can be found in the protein data bank, are sets of components for sure. But it can not be
said that chains are composed always by molecules or that molecules are composed always by chains.
A set of molecules can sometimes define a chain (e.g.: crystal waters), or a molecule can be made up by more than a chain (e.g.: protein complex).

### Main attributes

index: Index (0-based) of chain in the list of all chains defined in the molecular model.
id: External identification integer of chain.
name: chain name if any.

entity: molecules (components, groups and atoms).

