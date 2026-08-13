"""Directional contracts for public selection syntaxes."""

import importlib

import pytest

import molsysmt as msm
from molsysmt.basic.selector import _dict_indices_to_selection, _dict_select
from molsysmt.supported._syntaxes import (
    selection_syntaxes,
    syntax_capabilities,
    translation_syntaxes,
)


def test_declared_directions_match_the_dispatch_tables():
    assert tuple(_dict_select) == selection_syntaxes
    assert tuple(_dict_indices_to_selection) == translation_syntaxes
    assert tuple(syntax_capabilities) == (
        'MolSysMT',
        'MDTraj',
        'MDAnalysis',
        'NGLView',
    )


def test_supported_syntaxes_reports_both_directions():
    observed = msm.supported.syntaxes().data.set_index('Syntax')

    assert observed.loc['MolSysMT', 'Selection input']
    assert not observed.loc['MolSysMT', 'Translation output']
    assert observed.loc['MDTraj', 'Selection input']
    assert observed.loc['MDTraj', 'Translation output']
    assert not observed.loc['NGLView', 'Selection input']
    assert observed.loc['NGLView', 'Translation output']


def test_historical_registry_module_keeps_public_report_callable():
    compatibility_module = importlib.import_module('molsysmt.supported.syntaxes')

    assert compatibility_module.syntaxes == tuple(syntax_capabilities)
    assert callable(msm.supported.syntaxes)
    assert tuple(msm.supported.syntaxes().data['Syntax']) == tuple(syntax_capabilities)


@pytest.mark.parametrize('syntax', ['Amber', 'ParmEd', 'MolSysMT_NEW', 'NGLView'])
def test_unimplemented_input_syntaxes_are_rejected_during_digestion(
    t4_h5msm_molsys,
    syntax,
):
    with pytest.raises(msm.ArgumentError, match='syntax'):
        msm.select(t4_h5msm_molsys, selection='all', syntax=syntax)


@pytest.mark.parametrize('to_syntax', ['Amber', 'ParmEd', 'MolSysMT_NEW', 'MDAnalysis'])
def test_unimplemented_output_syntaxes_are_rejected_during_digestion(
    t4_h5msm_molsys,
    to_syntax,
):
    with pytest.raises(msm.ArgumentError, match='to_syntax'):
        msm.select(t4_h5msm_molsys, selection=[0, 1], to_syntax=to_syntax)


def test_mdtraj_and_nglview_output_directions_are_executable(t4_h5msm_molsys):
    assert msm.select(t4_h5msm_molsys, [0, 1], to_syntax='MDTraj') == 'index 0 1'
    assert msm.select(t4_h5msm_molsys, [0, 1], to_syntax='NGLView') == '@0,1'
