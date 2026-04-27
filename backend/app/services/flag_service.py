import secrets


def generate_flag() -> str:
    random_part = secrets.token_hex(8)
    return f"FLAG{{{random_part}}}"
