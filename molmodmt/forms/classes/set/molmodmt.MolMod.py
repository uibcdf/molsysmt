def set(item, atom_indices=None, **kwargs):

    for option in kwargs:
        if option=='box' and kwargs[option] is not True:
            item.trajectory.box=kwargs[option]
            item.trajectory.box2cell()
        if option=='cell' and kwargs[option] is not True:
            item.trajectory.cell=kwargs[option]
            item.trajectory.cell2box()

    pass


