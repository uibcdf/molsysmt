"""
Tests for pre-flight memory footprint estimation and eager/heavy decision policy.
"""
import pytest
from molsysmt._private.execution import estimate_footprint, decide_mode


def test_estimate_footprint_basic():
    # 100 atoms, 1000 structures, float64 (8 bytes)
    # raw = 100 * 1000 * 3 * 8 = 2_400_000
    # with 20% margin = 2_880_000
    fp = estimate_footprint(n_atoms=100, n_structures=1000)
    assert fp == 2_880_000


def test_estimate_footprint_scaling():
    fp_small = estimate_footprint(100, 100)
    fp_large = estimate_footprint(100, 1000)
    assert fp_large == 10 * fp_small


def test_decide_mode_force():
    # 'force' always returns heavy regardless of footprint
    assert decide_mode(0, heavy_mode='force') == 'heavy'
    assert decide_mode(10**15, heavy_mode='force') == 'heavy'


def test_decide_mode_off():
    # 'off' always returns eager regardless of footprint
    assert decide_mode(0, heavy_mode='off') == 'eager'
    assert decide_mode(10**15, heavy_mode='off') == 'eager'


def test_decide_mode_auto_small():
    # Small footprint → eager
    assert decide_mode(1000, heavy_mode='auto') == 'eager'


def test_decide_mode_auto_large():
    # Footprint larger than any machine → heavy
    assert decide_mode(10**18, heavy_mode='auto') == 'heavy'
