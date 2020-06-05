def rgb2hex(rgb):

    r = int(rgb[0]) ; g = int(rgb[1]) ; b = int(rgb[2])
    hex = "0x{:02x}{:02x}{:02x}".format(r,g,b)
    return hex

def colorscale2hex(values,color_min=[255,0,0],color_max=[255,255,255],value_min=None,value_max=None,num_bins=254):

    from numpy import array

    if not value_min:
        value_min=values.min()
    if not value_max:
        value_max=values.max()

    color_bin=(array(color_max)-array(color_min))/float(num_bins)
    scale_bin=(value_max-value_min)/float(num_bins)

    colors_hex=[]
    for val in values:
        val_bin=(val-value_min)/scale_bin
        rgb_from_val=(color_bin*val_bin).astype(int)+array(color_min)
        colors_hex.append(rgb2hex(rgb_from_val))

    return colors_hex

