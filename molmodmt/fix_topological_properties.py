from .multitool import get_form as _get_form

def fix_chains(item,chains=None):

    in_form = _get_form(item)

    if in_form=='parmed.Structure' or in_form=='parmed.GromacsTopologyFile':
        print("Bingo")
