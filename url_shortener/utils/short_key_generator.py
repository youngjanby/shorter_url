import secrets
import string


def generator_short_key():
    alphabet = string.ascii_letters + string.digits

    chars = [secrets.choice(alphabet) for _ in range(6)]
    result = "".join(chars)

    return result