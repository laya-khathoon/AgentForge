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
