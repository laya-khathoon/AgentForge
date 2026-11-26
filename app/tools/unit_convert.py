"""Fifth AgentForge tool: convert a number between common units.

Argument format: `<number> <from unit> to <to unit>`, for example
`5 km to miles`. Only fixed lookup tables are used, nothing is evaluated.
"""

_LENGTH_IN_METRES = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "inch": 0.0254,
    "ft": 0.3048,
    "mile": 1609.344,
}

_WEIGHT_IN_GRAMS = {
    "mg": 0.001,
    "g": 1.0,
    "kg": 1000.0,
    "oz": 28.349523125,
    "lb": 453.59237,
}


def _convert_with_table(value, source, target, table):
    return value * table[source] / table[target]


def _convert_temperature(value, source, target):
    """Convert between c, f and k by going through celsius."""
    if source == "c":
        celsius = value
    elif source == "f":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15
    if target == "c":
        return celsius
    if target == "f":
        return celsius * 9 / 5 + 32
    return celsius + 273.15


_ALIASES = {
    "millimetre": "mm", "millimeter": "mm", "millimetres": "mm", "millimeters": "mm",
    "centimetre": "cm", "centimeter": "cm", "centimetres": "cm", "centimeters": "cm",
    "metre": "m", "meter": "m", "metres": "m", "meters": "m",
    "kilometre": "km", "kilometer": "km", "kilometres": "km", "kilometers": "km",
    "inches": "inch", "in": "inch", "foot": "ft", "feet": "ft",
    "miles": "mile", "mi": "mile",
    "milligram": "mg", "milligrams": "mg", "gram": "g", "grams": "g",
    "kilogram": "kg", "kilograms": "kg", "kgs": "kg",
    "ounce": "oz", "ounces": "oz", "pound": "lb", "pounds": "lb", "lbs": "lb",
    "celsius": "c", "fahrenheit": "f", "kelvin": "k",
}
_MAX_CHARS = 100


def _normalise(unit):
    unit = unit.strip().lower().rstrip(".")
    return _ALIASES.get(unit, unit)


def _kind(unit):
    if unit in _LENGTH_IN_METRES:
        return "length"
    if unit in _WEIGHT_IN_GRAMS:
        return "weight"
    if unit in ("c", "f", "k"):
        return "temperature"
    return None


def unit_convert(argument=None):
    """Convert `<number> <unit> to <unit>` and return the answer as text."""
    if argument is not None and not isinstance(argument, str):
        return "Cannot convert: give text like '5 km to miles'"
    if not argument or not argument.strip():
        return "Nothing to convert. Give something like: 5 km to miles"
    if len(argument) > _MAX_CHARS:
        return f"Cannot convert: input is too long (maximum {_MAX_CHARS} characters)"
    parts = argument.lower().split()
    if "to" not in parts or parts.count("to") != 1:
        return "Cannot convert: use the form '<number> <unit> to <unit>'"
    split_at = parts.index("to")
    left, right = parts[:split_at], parts[split_at + 1:]
    if len(left) != 2 or len(right) != 1:
        return "Cannot convert: use the form '<number> <unit> to <unit>'"
    try:
        value = float(left[0])
    except ValueError:
        return f"Cannot convert: '{left[0]}' is not a number"
    if value != value or value in (float("inf"), float("-inf")):
        return "Cannot convert: the number must be finite"
    source, target = _normalise(left[1]), _normalise(right[0])
    kind = _kind(source)
    if kind is None:
        return f"Cannot convert: unknown unit '{left[1]}'"
    if _kind(target) is None:
        return f"Cannot convert: unknown unit '{right[0]}'"
    if kind != _kind(target):
        return f"Cannot convert {left[1]} to {right[0]}: they measure different things"
    if kind == "length":
        result = _convert_with_table(value, source, target, _LENGTH_IN_METRES)
    elif kind == "weight":
        result = _convert_with_table(value, source, target, _WEIGHT_IN_GRAMS)
    else:
        result = _convert_temperature(value, source, target)
    return f"{value:g} {left[1]} = {round(result, 4):g} {right[0]}"
