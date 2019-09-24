
def memory_of_ndarray( array, output='GB'):

    #1 == 1.0 Byte
    #1024 == 1.00 KB
    #1048576 == 1.00 MB
    #1073741824 == 1.00 GB
    #1099511627776 == 1.00 TB

    n={'B':0, 'KB':1, 'MB':2, 'GB':3, 'TB':4}

    return array.size*array.itemsize*(1.0/1024.0**n[output])

def memory_estimation_of_ndarray( shape, dtype='float64', output='GB'):

    import numpy as _np

    n={'B':0, 'KB':1, 'MB':2, 'GB':3, 'TB':4}

    size = 1
    for ii in shape:
        size = size*ii

    tmp=_np.ones([1], dtype=dtype)
    itemsize=tmp.itemsize

    return size*itemsize*(1.0/1024.0**n[output])


