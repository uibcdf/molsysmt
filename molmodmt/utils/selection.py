
def parse_selection(selection,syntaxis="mdtraj"):

    if syntaxis=="mdtraj":

        selection=selection.replace("dna","(resname DA DG DC DT DI)")
        selection=selection.replace("rna","(resname A G C U I)")

    return selection

