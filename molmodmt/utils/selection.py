def parse_selection(selection,syntaxis="mdtraj"):

    from molmodmt.topology import ion_residues

    if syntaxis=="mdtraj":

        selection=selection.replace("dna","(resname DA DG DC DT DI)")
        selection=selection.replace("rna","(resname A G C U I)")
        selection=selection.replace("ion",'(resname '+' '.join(['"'+str(ii)+'"' for ii in ion_residues])+')')
        selection=selection.replace("cosolutes",'(resname '+' '.join(['"'+str(ii)+'"' for ii in ion_residues])+')')

    return selection

