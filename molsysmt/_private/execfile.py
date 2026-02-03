### From debugpy/_vendored/pydevd/_pydev_bundle/_pydev_execfile.py
### I don't know why, but jupyter loads it by default. Python and IPython does not load it.

_CACHE = {}

def execfile(file, glob=None, loc=None):
    if glob is None:
        import sys
        glob = sys._getframe().f_back.f_globals
    if loc is None:
        loc = glob

    import os
    abs_path = os.path.abspath(file)

    if abs_path not in _CACHE:
        # It seems that the best way is using tokenize.open(): http://code.activestate.com/lists/python-dev/131251/
        # (but tokenize.open() is only available for python 3.2)
        import tokenize
        if hasattr(tokenize, 'open'):
            # version 3.2
            stream = tokenize.open(abs_path)  # @UndefinedVariable
        else:
            # version 3.0 or 3.1
            detect_encoding = tokenize.detect_encoding(open(abs_path, mode="rb").readline)
            stream = open(abs_path, encoding=detect_encoding[0])
        try:
            contents = stream.read()
        finally:
            stream.close()

        # compile first to have the filename set in debug mode
        _CACHE[abs_path] = compile(contents + "\n", abs_path, 'exec')

    # execute the script from cache
    exec(_CACHE[abs_path], glob, loc)