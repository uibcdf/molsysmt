"""
Unit and regression test for the copy module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

def test_show_as_surface_1():

    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'])

    view = msm.view(molsys)
    view.clear()
    msm.thirds.nglview.show_as_surface(view, selection='group_index in [0,1,2]')

    selection = msm.select(molsys, selection='group_index in [0,1,2]', to_syntax='NGLview')

    aux = view._ngl_msg_archive[-1]
    assert (aux['target']=='compList')
    assert (aux['methodName']=='addRepresentation')
    assert (aux['args']==['surface'])
    assert (aux['kwargs']['sele']==selection)


def test_show_as_surface_2():

    molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'])

    view = msm.view(molsys)
    view.clear()
    msm.thirds.nglview.show_as_cartoon(view, selection='all')
    msm.thirds.nglview.show_as_surface(view, selection='group_index in [0,1,2]')

    selection = msm.select(molsys, selection='group_index in [0,1,2]', to_syntax='NGLview')

    aux = view._ngl_msg_archive[-1]
    assert (aux['target']=='compList')
    assert (aux['methodName']=='addRepresentation')
    assert (aux['args']==['surface'])
    assert (aux['kwargs']['sele']==selection)



