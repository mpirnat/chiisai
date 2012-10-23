"""Convert to base 62 (etc.)"""

base62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def base_encode(integer, alphabet=base62):
    """Encode a base10 integer as a Base X string."""
    if integer == 0:
        return alphabet[integer]

    result = []
    base = len(alphabet)
    while integer != 0:
        result.append(alphabet[integer % base])
        integer /= base
    result.reverse()
    return ''.join(result)


def base_decode(string_, alphabet=base62):
    """Decode a Base X string into a base10 integer."""
    base = len(alphabet)
    length = len(string_)
    integer = 0

    for i, char in enumerate(string_):
        power = (length - (i + 1))
        integer += alphabet.index(char) * (base ** power)

    return integer
