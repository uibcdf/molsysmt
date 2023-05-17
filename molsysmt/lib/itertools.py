import numba as nb

@nb.njit(nb.void(nb.int64, nb.int64))
def infinite_sequence(a,b):
    num = a
    while True:
        yield num
        num += b
