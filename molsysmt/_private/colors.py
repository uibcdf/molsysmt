import numpy as np
import matplotlib.colors as mcolors
from matplotlib.pyplot import colormaps as mcolormaps

def color_is_hex(color):

    output = False

    if isinstance(color, str):
        if len(color)==7 and color[0]=='#':
            output = True
        if len(color)==6:
            output = True

    return output

def color_is_rgb(color):

    output = False

    if isinstance(color, (list, tuple, np.ndarray)):
        if len(color)==3 and all(isinstance(ii,(int, np.int64, float)) for ii in color):
            output = True

    return output

def is_color(color):

    return color_is_hex(color) or color_is_rgb(color)

def is_iterable_of_colors(color):

    output = False

    if isinstance(color, (list, tuple, np.ndarray)):
        output = all([is_color(ii) for ii in color])

    return output

def color_to_form(color, form):

    output = None

    if form=='rgb':

        if color_is_rgb(color):
            output = color
        else:
            output = mcolors.to_rgb(color)

    elif form=='hex':

        if color_is_hex(color):
            output = color
        else:
            output = mcolors.to_hex(color)

    return output

def color_to_list_of_colors(color, n_colors, form='rgb'):

    output = None

    if color_is_hex(color) or color_is_rgb(color):

        aux_color = color_to_form(color, form)
        output = [aux_color for ii in range(n_colors)]

    elif is_iterable_of_colors(color):
        if len(color)==n_colors:
            output = [color_to_form(ii, form) for ii in color]

    return output

def get_list_of_colors_from_values(values, min_value=None, mid_value=None, max_value=None,
        symmetrical=False, scale='linear', colormap='bwr', form='rgb'):

    if scale=='linear':

        if mid_value is not None:

            if not symmetrical:

                if min_value is None:
                    min_value = min(values)

                if max_value is None:
                    max_value = max(values)

                norm = mcolors.TwoSlopeNorm(vmin=min_value, vcenter=mid_value, vmax=max_value)

            else:

                if (max_value is None) and (min_value is None):
                    min_value = min(values)
                    max_value = max(values)
                    halfrange= max(abs(max_value-mid_value),abs(min_value-mid_value))
                elif (min_value is not None):
                    halfrange= abs(min_value-mid_value)
                elif (max_value is not None):
                    halfrange= abs(max_value-mid_value)

                halfrange= max(abs(max_value-mid_value),abs(min_value-mid_value))
                norm = mcolors.CenteredNorm(v_center=mid_value, halfrange=halfrange)

        else:

            if min_value is None:
                min_value = min(values)

            if max_value is None:
                max_value = max(values)

            norm = mcolors.Normalize(vmin=min_value, vmax=max_value)

    elif scale=='log':

        raise NotImplementedError

    data = norm(values)
    cmap = mcolormaps[colormap]
    output_rgba = cmap(data)

    if form!='rgba':
        output = [color_to_form(ii, form=form) for ii in output_rgba]
    else:
        output = output_rgba

    return output

