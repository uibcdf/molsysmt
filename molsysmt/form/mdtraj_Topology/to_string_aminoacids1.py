from molsysmt._private.digestion import digest

@digest(form='mdtraj.Topology')
def to_string_aminoacids1(item, group_indices='all', digest=True):

    from . import to_string_aminoacids3
    from ..string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1

    tmp_item = to_string_aminoacids3(item, group_indices=group_indices, digest=False)
    tmp_item = string_aminoacids3_to_string_aminoacids1(tmp_item, digest=False)

    return tmp_item

