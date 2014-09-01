"""
	Provides combinations_with_replacement that is available in
	itertools in python2.7 but not python2.6

	recipe from:
		https://docs.python.org/2.6/library/itertools.html
"""

def combinations_with_replacement(iterable, r):
    "combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC"
    # number items returned:  (n+r-1)! / r! / (n-1)!
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)
