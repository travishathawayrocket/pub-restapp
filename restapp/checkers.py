def username_check(value):
    if value <= 30:
        raise ValueError('username must be 30 characters or less')
    if value < 3:
        raise ValueError('username must be at least 3 characters in length')

    return value
