import math
import pint
from pint.errors import RedefinitionError

# One (and only one) global registry for the whole project
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

# ---- Custom units / aliases ----
# Inches of water column at ~39°F (≈ 4°C).
# Commonly ~249.08891 Pa per inch H2O at 39°F.
try:
    ureg.define("inch_H2O_39F = 249.08891 * pascal = inH2O_39F = inH2O")
except RedefinitionError:
    # Safe to ignore if the module gets reloaded during dev
    pass

# ---- Convenience pseudo-units ----
# Add "unitless" units to convert percentages
try:
    ureg.define('unitless = [no_unit]')
    ureg.define('percent = unitless / 100 = percentage')
except RedefinitionError:
    pass


def convert(value, old_unit, new_unit):
    if value is None:
        return None
    return (Q_(value, old_unit)).to(Q_(new_unit)).magnitude


def pitch2deg(pitch):
    radian = math.atan(pitch / 12)
    return convert(radian, 'rad', 'deg')


# Useful conversions for faster parsing (evaluated once)
degC_to_K = convert(0, 'degC', 'K')               # 273.15
kwh_to_therms = convert(1, 'kWh', 'therms')
cfm_to_m3s = convert(1, 'cubic_feet/min', 'm^3/s')
