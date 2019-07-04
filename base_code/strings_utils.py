
def apostrophe(s):
    return "'s" in s or "’s" in s


def script(s):
    return "—" in s


def valid_name(n):
    return not apostrophe(n) and not script(n) and len(n) > 1 and n[0].isupper()
