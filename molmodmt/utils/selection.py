from .exceptions import *

_parser={
    'molmodmt' : 'MolModMT',
    'amber' : 'Amber',
    'mdanalysis' : 'MDAnalysis',
    'mdtraj' : 'MDTraj',
    'parmed' : 'ParmEd'
}

def digest_syntaxis(syntaxis):

    try:
        syntaxis = _parser[syntaxis.lower()]
        return syntaxis
    except:
        raise BadCallError('Wrong way of invoking this method. Either the engine is not implemented, either is mispelled.\n\
                           Check the online documentation  for more information: http://www.uibcdf.org/MolModMT')


def digest(selection, syntaxis="MolModMT"):

    syntaxis = digest_syntaxis(syntaxis)

    from molmodmt.topology import ion_residues

    if syntaxis=='MolModMT':

        selection=selection.replace('backbone','(atom.name==["CA", "N", "C", "O"])')

    elif syntaxis=="MDTraj":

        selection=selection.replace("dna","(resname DA DG DC DT DI)")
        selection=selection.replace("rna","(resname A G C U I)")
        selection=selection.replace("ion",'(resname '+' '.join(['"'+str(ii)+'"' for ii in ion_residues])+')')
        selection=selection.replace("cosolutes",'(resname '+' '.join(['"'+str(ii)+'"' for ii in ion_residues])+')')


    return selection, syntaxis

