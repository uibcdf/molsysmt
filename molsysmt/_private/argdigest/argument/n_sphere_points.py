from molsysmt._private.smonitor import ArgumentError

def digest_n_sphere_points(n_sphere_points, caller=None):

    if isinstance(n_sphere_points, int) and not isinstance(n_sphere_points, bool):
        if n_sphere_points > 0:
            return n_sphere_points

    raise ArgumentError('n_sphere_points', value=n_sphere_points, caller=caller, message=None)
