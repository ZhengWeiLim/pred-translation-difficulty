from unidecode import unidecode


def clean_str(chars):
    chars = chars.rstrip().replace('\u200e', '').replace('\u200b', '').replace('  ', ' ')
    return chars


def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())

def isdecodable(s):
    try:
        decoded = unidecode(s, errors="strict")
        return True
    except:
        return False


