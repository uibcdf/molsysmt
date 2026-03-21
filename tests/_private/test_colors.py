"""
Tests for molsysmt._private.colors module (53% coverage → improve).
"""

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# color_is_hex
# ---------------------------------------------------------------------------

class TestColorIsHex:
    def test_7char_hex(self):
        from molsysmt._private.colors import color_is_hex
        assert color_is_hex('#FF0000') is True

    def test_6char_hex(self):
        from molsysmt._private.colors import color_is_hex
        assert color_is_hex('FF0000') is True

    def test_rgb_tuple_not_hex(self):
        from molsysmt._private.colors import color_is_hex
        assert color_is_hex((1.0, 0.0, 0.0)) is False

    def test_short_string_not_hex(self):
        from molsysmt._private.colors import color_is_hex
        assert color_is_hex('red') is False


# ---------------------------------------------------------------------------
# color_is_rgb
# ---------------------------------------------------------------------------

class TestColorIsRgb:
    def test_list_rgb(self):
        from molsysmt._private.colors import color_is_rgb
        assert color_is_rgb([1.0, 0.0, 0.0]) is True

    def test_tuple_rgb(self):
        from molsysmt._private.colors import color_is_rgb
        assert color_is_rgb((0, 128, 255)) is True

    def test_ndarray_rgb(self):
        from molsysmt._private.colors import color_is_rgb
        assert color_is_rgb(np.array([0.5, 0.5, 0.5])) is True

    def test_string_not_rgb(self):
        from molsysmt._private.colors import color_is_rgb
        assert color_is_rgb('red') is False

    def test_wrong_length(self):
        from molsysmt._private.colors import color_is_rgb
        assert color_is_rgb([1.0, 0.0]) is False


# ---------------------------------------------------------------------------
# is_color
# ---------------------------------------------------------------------------

class TestIsColor:
    def test_hex_is_color(self):
        from molsysmt._private.colors import is_color
        assert is_color('#AABBCC') is True

    def test_rgb_is_color(self):
        from molsysmt._private.colors import is_color
        assert is_color([1.0, 0.0, 0.0]) is True

    def test_string_not_color(self):
        from molsysmt._private.colors import is_color
        assert is_color('red') is False


# ---------------------------------------------------------------------------
# is_iterable_of_colors
# ---------------------------------------------------------------------------

class TestIsIterableOfColors:
    def test_list_of_hex(self):
        from molsysmt._private.colors import is_iterable_of_colors
        assert is_iterable_of_colors(['#FF0000', '#00FF00']) is True

    def test_list_of_rgb(self):
        from molsysmt._private.colors import is_iterable_of_colors
        assert is_iterable_of_colors([[1, 0, 0], [0, 1, 0]]) is True

    def test_mixed_not_colors(self):
        from molsysmt._private.colors import is_iterable_of_colors
        assert is_iterable_of_colors(['red', 'blue']) is False

    def test_non_iterable(self):
        from molsysmt._private.colors import is_iterable_of_colors
        assert is_iterable_of_colors('red') is False


# ---------------------------------------------------------------------------
# color_to_form
# ---------------------------------------------------------------------------

class TestColorToForm:
    def test_rgb_to_rgb(self):
        from molsysmt._private.colors import color_to_form
        color = [1.0, 0.0, 0.0]
        result = color_to_form(color, 'rgb')
        assert result == color

    def test_hex_to_rgb(self):
        from molsysmt._private.colors import color_to_form
        result = color_to_form('#FF0000', 'rgb')
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_hex_to_hex(self):
        from molsysmt._private.colors import color_to_form
        result = color_to_form('#FF0000', 'hex')
        assert result == '#FF0000'

    def test_rgb_to_hex(self):
        from molsysmt._private.colors import color_to_form
        result = color_to_form([1.0, 0.0, 0.0], 'hex')
        assert isinstance(result, str)
        assert result.startswith('#')


# ---------------------------------------------------------------------------
# color_to_list_of_colors
# ---------------------------------------------------------------------------

class TestColorToListOfColors:
    def test_single_hex_to_list(self):
        from molsysmt._private.colors import color_to_list_of_colors
        result = color_to_list_of_colors('#FF0000', 3, form='hex')
        assert len(result) == 3
        assert all(c == '#FF0000' for c in result)

    def test_single_rgb_to_list(self):
        from molsysmt._private.colors import color_to_list_of_colors
        color = [1.0, 0.0, 0.0]
        result = color_to_list_of_colors(color, 2, form='rgb')
        assert len(result) == 2

    def test_iterable_of_colors(self):
        from molsysmt._private.colors import color_to_list_of_colors
        colors = ['#FF0000', '#00FF00', '#0000FF']
        result = color_to_list_of_colors(colors, 3, form='hex')
        assert len(result) == 3


# ---------------------------------------------------------------------------
# get_list_of_colors_from_values
# ---------------------------------------------------------------------------

class TestGetListOfColorsFromValues:
    def test_basic_linear_no_midvalue(self):
        from molsysmt._private.colors import get_list_of_colors_from_values
        values = [0.0, 0.5, 1.0]
        result = get_list_of_colors_from_values(values, form='rgb')
        assert len(result) == 3

    def test_linear_with_midvalue(self):
        from molsysmt._private.colors import get_list_of_colors_from_values
        values = [-1.0, 0.0, 1.0]
        result = get_list_of_colors_from_values(values, mid_value=0.0, form='rgb')
        assert len(result) == 3

    def test_rgba_form(self):
        from molsysmt._private.colors import get_list_of_colors_from_values
        values = [0.0, 1.0]
        result = get_list_of_colors_from_values(values, form='rgba')
        assert result.shape[1] == 4  # RGBA

    def test_explicit_min_max(self):
        from molsysmt._private.colors import get_list_of_colors_from_values
        values = [0.0, 0.5, 1.0]
        result = get_list_of_colors_from_values(values, min_value=0.0, max_value=1.0, form='rgb')
        assert len(result) == 3

    def test_linear_with_midvalue_symmetrical(self):
        from molsysmt._private.colors import get_list_of_colors_from_values
        values = [-2.0, 0.0, 1.0]
        result = get_list_of_colors_from_values(values, mid_value=0.0, symmetrical=True, form='rgb')
        assert len(result) == 3
