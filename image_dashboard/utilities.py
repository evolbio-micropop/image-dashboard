""" :module: Various utilities. """
def chunks(l, n):
    """Yield successive n-sized chunks from l.
    :credits: Henry Kirkwood at European XFEL.
    """
    # TODO: Check input.
    for i in range(0, len(l), n):
        yield l[i:i + n]
