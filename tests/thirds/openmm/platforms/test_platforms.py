"""
Unit and regression test for the copy module of the molsysmt package.
"""

import molsysmt as msm

def test_Platforms_1():

    platforms = msm.thirds.openmm.platforms.available_platforms(verbose=False)

    assert isinstance(platforms, list)

def test_Platforms_2(capsys):

    msm.thirds.openmm.platforms.available_platforms(verbose=True)

    captured = capsys.readouterr()

    assert captured.out.startswith('Platform')

def test_Platforms_3(capsys):

    msm.thirds.openmm.platforms.loading_failures()

    captured = capsys.readouterr()
    
    assert captured.out
