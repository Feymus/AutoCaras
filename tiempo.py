def measure_time(f):
    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print ('%r (%r, %r) %2.2f sec' % \
        (f.__name__, args, kw, te-ts))
        return result
    return timed
