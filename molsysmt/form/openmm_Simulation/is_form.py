def is_form(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return 'openmm.Simulation'==item_fullname

