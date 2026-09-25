# What is MolSysMT?

MolSysMT -**Mol**ecular **Sys**tems **M**ulti**T**oolkit - is a scientific
open-source Python library for working with molecular systems. One uniform API
lets you build a system, repair and prepare it, ask it questions, modify it,
analyse its structures and visualise it, without changing library every time the
task changes.

This library was developed to provide a user-friendly interface for
computational molecular biology labs, such as the
[UIBCDF](https://www.uibcdf.org/), to use in their research. It is the core of
the MolSysSuite ecosystem.

MolSysMT does its own work. It has its own molecular model, its own HDF5-based
storage format, a structure-preparation pipeline that needs no external engine to
add missing heavy atoms, terminal cappings or hydrogens and to solvate a system,
and its own precompiled compute kernels for distances, contacts, neighbour lists,
RMSD and superposition, principal axes, PCA, SASA, dihedral angles and periodic
boundary conditions.

It is also deliberately open to the rest of the ecosystem. MolSysMT interoperates
with 89 forms — files, libraries and in-memory objects — so a system can arrive or
leave in whatever shape the rest of your workflow needs, and so you can hand work
over to a specialised tool whenever that is what you want. It was never designed
to replicate what MDAnalysis, MDTraj, PDBFixer, OpenMM, ParmEd, RDKit or NGLView
already do well. Whenever you use methods or tools from these packages, all credit
should be given to their respective authors, developers, maintainers, and
contributors.

MolSysMT is an open-source project shared under the [MIT license](https://github.com/uibcdf/molsysmt/blob/main/LICENSE). This means
that you have the right to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies without any limitations.

If you have suggestions, improvements, enhancement proposals, if you miss a
functionality, or you have identified a bug or a malfunction, feel free to
contribute to its development or interact with the authors and contributors by
using the [MolSysMT public GitHub repository](https://github.com/uibcdf/molsysmt).

When using MolSysMT, it is important to understand that the authors and
contributors do not provide any legal warranty or assume any liability of any
kind regarding its use and results.

We hope you find it useful!

[Diego Prada-Gracia and Liliana M. Moreno Vargas](who.md).

<br/>

<br/>

:::{figure} ../../_static/logo.svg
:width: 50%
:align: center
:::

<br/>

<br/>

