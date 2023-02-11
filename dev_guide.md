# Agreements

## Basic

## Get

- n_atoms is always an integer even when there is no topological info.
- n_structures is None when the form has no structural info. If the form can store structures n_structures is always an integer.
- if time, box, etc... (structural attributes) are not present in an object... the output is a list with as many Nones as structure_indices.

## Iterator

- Coordinates is always a numpy.ndarray with shape (n_frames, n_atoms, 3), even with n_frames=1.
- Box is always a numpy.ndarray with shape (n_frames, 3, 3), even with n_frames=1.

## Form

### Structural Iterator

- Coordinates is always a numpy.ndarray with shape (n_frames, n_atoms, 3), even with n_frames=1.
- Box is always a numpy.ndarray with shape (n_frames, 3, 3), even with n_frames=1.

## Native

- if time, box, etc... (structural attributes) are not present in an object... the output is a list with as many Nones as structures in the object.
if there are no structures... all attributes are equal to None.

