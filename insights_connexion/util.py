def string_to_bool(string):
    if string in ('True', 'true', 'yes', 'y'):
        return True
    elif string in ('False', 'false', 'no', 'n'):
        return False
    else:
        raise ValueError('Invalid string passed to string_to_bool.')
