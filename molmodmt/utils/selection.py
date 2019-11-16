from .exceptions import *

_parser={
    'pandas' : 'Pandas',
    'amber' : 'Amber',
    'mdanalysis' : 'MDAnalysis',
    'mdtraj' : 'MDTraj',
    'parmed' : 'ParmEd'
}

def digest(selection, syntaxis="MDTraj"):

    try:
        syntaxis = _parser[syntaxis.lower()]
    except:
        raise BadCallError('Wrong way of invoking this method. Either the engine is not implemented, either is mispelled.\n\
                           Check the online documentation  for more information: http://www.uibcdf.org/MolModMT')


    from molmodmt.topology import ion_residues

    if syntaxis=="MDTraj":

        selection=selection.replace("dna","(resname DA DG DC DT DI)")
        selection=selection.replace("rna","(resname A G C U I)")
        selection=selection.replace("ion",'(resname '+' '.join(['"'+str(ii)+'"' for ii in ion_residues])+')')
        selection=selection.replace("cosolutes",'(resname '+' '.join(['"'+str(ii)+'"' for ii in ion_residues])+')')

    return selection, syntaxis

