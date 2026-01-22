# Dimension Component using ltk's reactive MVP model

import ltk
from util_units import *

# Debug
def print(*args):
    ltk.find("body").append(" ".join(str(a) for a in args), "<br>")
if '__terminal__' in locals():  # resize terminal if started in index.html
    __terminal__.resize(60, 6)

class DC_params(ltk.Model):
    """
    Reactive UI parameters
    """
    measure: str = "250yd"
    units: str = "yd"
    altunits: str = "229m"
    
    def __init__(self, parent, defaults=["20","wpi","wpcm"], inch_base=False):
        super().__init__()
        self.parent = parent  # not strictly required at this child level but
        # needed for UI components with operationally dependent children.
        #
        self.defaults = defaults
        self.inch_base = inch_base
        self.inhibit_update = False
        #
        self.set_to_defaults()

    def set_to_defaults(self):
        self.measure = self.defaults[0] + self.defaults[1]
        self.units = self.defaults[1]
        self.altunits = convert_imp(int(self.defaults[0]), self.defaults[2], self.inch_base)

    def changed(self, name, value):
        """
        For this component:
        - toggle units btwn metric/imperial
        - allow overiding units
        - allow numeric only or numeric+units entry
        - show the alt units to be helpful eh
        """
        #print(f"DC:Change req: {name} to {value}")
        if not self.inhibit_update:
            #print(f"DC:Changing: {name} to {value}")
            self.inhibit_update = True  # inhibit rippling calls while we update
            if name == "measure":
                self.update_measure(value)
            elif name == "units":
                self.update_units(value)
            # reset ripple updates
            self.inhibit_update = False
        #else:
        #    print("- DC:Skipping change")

    def update_measure(self, value):
        num, unit = parse_units(value)
        if num and num > -1:
            # got a valid measure but maybe no units
            if not unit:
                # use on-screen units
                units = f"{self.units}"
                self.measure = f"{format_nice(num)}{units}"
                if units in metric_units:
                    num = num * convert_factors[units]
                self.altunits = convert_imp(num, unit_swaps[units], self.inch_base)
            else:  # unit from measure
                if unit not in convert_factors.keys():
                    unit = self.defaults[1]
                self.units = unit
                usnum,_ = parse_to_US(value)
                self.measure = convert_imp(usnum, unit)
                self.altunits = convert_imp(usnum, unit_swaps[unit])
        else:  # not valid so set default
            self.set_to_defaults()

    def update_units(self, newunit):
        num, altunits = parse_units(self.altunits)
        usnum, _ = parse_to_US(self.measure)
        if altunits == newunit:  # straight swap
            self.update_measure(f"{num}{newunit}")
        elif newunit in  unit_swaps:  # convert to newunit
            self.update_measure(convert_imp(usnum, newunit))
        else:  # not a unit
            self.update_measure(f"{usnum}{newunit}")  # will be defaulted


class Component(object):
    """
    Create an instance using: Component(label, defaults, force_inches)
    Add to UI by using: .create()
    Read/write values by using .params.name_of_var
    - Default is [value, unit, altunit] all strings
    """
    def __init__(self, label="Foo", defaults=["250","yd","m"], inch_base=False):
        self.label = label
        self.params = DC_params(self, defaults=defaults, inch_base=inch_base)

    def toggle_units(self, event, var):
        self.params.changed(var.name, unit_swaps[f"{var}"])

    def create(self):
        """
        Present the value, units as buttons and
        altunits as a label
        """
        return (
            ltk.VBox(
                ltk.Label(self.label).addClass("Item paramtitle"),
                ltk.HBox(
                    ltk.Input(self.params.measure).addClass("measure"),
                    ltk.Input(self.params.units).addClass("measure short").on("click", ltk.proxy(lambda event: self.toggle_units(event, self.params.units))),
                    ltk.Label(self.params.altunits).addClass("measure altlabel noborder")
                )
            ).addClass("param")
        )

# standalone development/examination
if __name__ == "__main__":
    w = Component()
    widget = w.create()
    widget.appendTo(ltk.window.document.body)
    ltk.find(".param").css("border 2px dashed red")