from functools import lru_cache, wraps
import numba as nb


def lazy_njit(signature, cache=True, **kwargs):
    """Returning a lazily-compiled Numba function with a fixed signature."""

    def decorator(func):
        @lru_cache(maxsize=1)
        def _compiled():
            return nb.njit(signature, cache=cache, **kwargs)(func)

        @wraps(func)
        def wrapper(*args, **kwds):
            return _compiled()(*args, **kwds)

        return wrapper

    return decorator
