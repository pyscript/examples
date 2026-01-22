
# Here we assume all calcs are done in yds/in
# but we want to present unit agnostically.
# - all epi/wpi,ppi are in delivered in inches
# - all yds/ft/in/m/cm/mm are delivered in yds
# E.g. "3epcm" becomes "7.5epi", "1ft" becomes "0.333yds"

import re

# convert value in units to result in yards (or inch for epi/ppi/epcm) (use multiply)
convert_factors = {"yd": 1, "yds": 1, "ft": 0.333333, "in": 0.027777777,
                   "m": 1.09361, "cm": 0.0109361, "mm": 0.00109361,
                   # epi are in inches
                   "wpi": 1, "epi": 1, "ppi": 1, "wpcm": 2.54, "epcm": 2.54, "ppcm": 2.54}

yard_based = ["yd", "m"]
unit_swaps = {"in":"cm", "cm":"in",
              "ft":"cm",
              "yd":"m", "m":"yd",
              "wpi":"wpcm", "wpcm":"wpi",
              "epi":"epcm", "epcm":"epi",
              "ppi":"ppcm", "ppcm":"ppi"}
metric_units = ["m", "cm", "wpcm", "epcm","ppcm"]

# 3epcm (7.5epi),  3.5-4 epcm (9-10 ppi),  1 epcm (2.5ppi)

def parse_units(measure):
    """
    12yd, 3ft, 2m, 20cm, 200mm, 10in
    7epi, 7ppi, 10epcm
    - just extract number and units
    """
    # Pyodide
    match = re.match(r"(^[0-9]*\.?[0-9]*)(.*)", str(measure))
    #p = re.compile(r"(^[0-9]*\.?[0-9]*)(.*)")
    #found = p.findall(measure)
    #if found:
    #    num, unit = found[0]
    # Micropython
    #match = re.match("(^[0-9]*\.?[0-9]*)(.*)", str(measure))
    if match:
        num, unit = match.group(1), match.group(2)
        #
        if num and not num[-1].isalpha():
            number = float(num)
        else:
            number = -1
    return number, unit


def parse_to_US(measure):
    """
    12yd, 3ft, 2m, 20cm, 200mm, 10in
    7epi, 7ppi, 10epcm
    - convert to yd or epi
    """
    number, unit = parse_units(measure)
    if unit in convert_factors.keys():
        val = number * convert_factors[unit]
        if val == int(val):
            val = int(val)
    else:
        #print("Sorry - did not understand units:",measure)
        #val, unit = -1, None
        val, unit = int(number), "yd"  # more useful for this application
    return val, unit

def convert_sett(sett):
    """
    if epi then return inches conversion factor
    else cm factor
    """
    if sett in ['epi', 'wpi', 'ppi']:
        return convert_factors['in']
    else:
        return convert_factors['cm']
        
def convert_imp(value, units, inches=False):
    """
    Convert value from yards into units.
    - if inches then from inches to units
    Return a well presented float. 0,1 decimal place
    """
    result = value / convert_factors[units]
    if inches:
        result *= convert_factors['in']
    remainder = (result - int(result)) 
    # small values get meaningful decimal points of accuracy
    if remainder >= result/100:
        return f"{result:.1f}{units}"
    else:
        return f"{result:.0f}{units}"

def format_nice(value):
    """
    use single decimal point
    - remove '.0' for neatness
    """
    vstr = f"{value:1.1f}"
    if vstr[-2:] == ".0":
        vstr = vstr[:-2]
    return vstr



# Testing
if __name__ == "__main__":
    a = "22m"
    p = parse_units(a)
    print(f"Parse: '{a}' = {p}  or nicely as '{format_nice(p[0])}'")
    imp = parse_to_US(a)
    print(f"in yds (imperial) = {imp[0]}")
    m = convert_imp(imp[0], "cm")
    print(f"and back to '{m}'")
    print(f"or perhaps {imp[0] / convert_factors['ft']:1.2f} 'ft'")
    

    