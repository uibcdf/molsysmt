import numpy as np

def box2invbox(box):

    return np.linalg.inv(box)

def length_edges_box(box):

    raise NotImplementedError()

def angles_box(box):

    raise NotImplementedError()

def lengths_and_angles_to_box(lengths, angles):

    raise NotImplementedError()

def wrap_pbc(coors, centers, box, ortho):

    raise NotImplementedError()

def wrap_mic(coors, centers, box, ortho):

    raise NotImplementedError()

def unwrap(coors, box, ortho):

    raise NotImplementedError()

