def format_coordinates(
    latitude: float | int | str, longitude: float | int | str
) -> tuple[str, str]:
    """
    To comply with NWS API, we need to ensure coordinates have a maximum of 4 digits after the decimal,
    but no trailing zeroes
    """
    return (
        f"{latitude:.4f}".rstrip("0").rstrip("."),
        f"{longitude:.4f}".rstrip("0").rstrip("."),
    )


def set_icon_names(periods: dict):
    """periods is of the shape ForecastPeriod | HourlyForecastPeriod"""
    for period in periods:
        iconName: str = period["icon"].rsplit("/", 1)[1].split(",")[0]
        if "?" in iconName:
            iconName = iconName.split("?")[0]
        period["iconName"] = iconName
