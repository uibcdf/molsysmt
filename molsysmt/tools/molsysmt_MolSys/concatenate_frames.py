def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    tmp_item = extract(item)
    tmp_item.append_frames(step=step, time=time, coordinates=coordinates, box=box)

    return tmp_item

