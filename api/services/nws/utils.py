def format_coord(value: float | int | str) -> str:
    """
    To comply with NWS API, we need to ensure coordinates have a maximum of 4 digits after the decimal,
    but no trailing zeroes
    """
    return f"{value:.4f}".rstrip("0").rstrip(".")
