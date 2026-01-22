#imports
import ltk
import svg as SVG
import random
import dimension_component as DC

from pyscript import config
MICROPYTHON = config["type"] == "mpy"  # if we need to know if we're running pyodide or micropython

if '__terminal__' in locals():  # resize terminal if started in index.html
    __terminal__.resize(60, 10)

# globals
g_widget = None  # Hold ref to widget for nested components
# for SVG
solid_style = {"fill":"#AA0", "stroke":"#A00", "stroke-width":"1px"}

def create_svg_box(size=5):
    overall = 100
    box_size = 100 / size
    highlight_svg = SVG.svg(width=overall, height=overall,
                            preserveAspectRatio="xMidYMid meet",
                            viewBox=f"0 0 {overall+2} {overall+2}")
    # Transform the group to move its children
    grp = SVG.g(id="highlight", transform='translate(0 0)', style=solid_style)
    highlight_svg.appendChild(grp)
    grp.appendChild(SVG.rect(x=0, y=0, width=box_size, height=box_size))
    #
    return highlight_svg

## Events
# - moved event to Reactive area for event control so no global handlers
# UNUSED
def button_click_handler_dperecated(event):
    print("The non-reactive button has been clicked, the svg transformed")
    print(f"- checkbox clicked {g_widget.params.count_check_ticks} times.")
    # move the svg child
    x,y = random.randrange(0, 100-20), random.randrange(0, 100-20)
    ltk.find("#highlight").attr("transform", f"translate({x} {y})")

### Reactive UI variables and behaviour
class Reactive_params(ltk.Model):
    """
    """
    # These variables are all reactive
    check_me = False
    Drawin = 12  # Can use Drawin: int = 12 but python runtime does not check
    Draw_label = "Subtract 2"

    def __init__(self):
        """
        variables instanced here will not be reactive (only the classvars above)
        but its a good place to put all the other variables your widget needs.
        """
        super().__init__()
        self.inhibit_update = False
        self.count_check_ticks = 0  # as a useless example

    def changed(self, name, value):
        """
        Called whenever a UI element is changed by user.
         - name is always a string.
        Do whatever changes are required in here
        Also invoked for internal changes
        - inhibit_update is used to prevent needless rippling
        """
        #print("- Change requested:",name,value)
        if not self.inhibit_update:
            self.inhibit_update = True  # inhibit rippling calls while we update
            print("Changing:", name, value)
            if name == "check_me":
                # changing another reactive value does not ripple because of global inhibit var
                if self.check_me:
                    self.Draw_label = "Add 2 extra"
                    self.Drawin -=  2
                else:
                    self.Draw_label = "Subtract 2"
                    self.Drawin += 2
            # reset ripple updates
            self.inhibit_update = False

    def button_click_handler(self, event):
        print("The non-reactive button has been clicked, the svg transformed")
        print(f"- checkbox clicked {self.count_check_ticks} times.")
        # move the svg child
        x,y = random.randrange(0, 100-20), random.randrange(0, 100-20)
        ltk.find("#highlight").attr("transform", f"translate({x} {y})")

### UI
class UI_widget(object):
    """
    Top level object that shows App.
    """

    def __init__(self):
        self.params = Reactive_params()
        self.explanation = ["Ltk project example:",
                            "- Everything from starter_03 and building a UI element from a separate component file.",
                            "- This means you can construct standalone UI components to include when needed.",
                            "- Making single file components that can be reused is critical for large projects.",
                            "",
                            " In the index.html - you can uncomment script lines to run:",
                            "- the base module that is imported 'util_units.y' which runs a test",
                            "- the single file component (with tests) 'dimension_component.py'",
                            "- or the main.py which uses the single file component twice",
                            "",
                            "(Use ctrl-shift while moving the mouse over ltk UI elements for descriptions.)"
                          ]

    def label_box(self):
        """
        Can make parts of the UI like this
        """
        return (ltk.HBox(
                    ltk.Label(self.params.Draw_label),
                    ltk.Checkbox(self.params.check_me).attr("id", "check_1")
                ).css("border","1px dashed cyan")
               )

    def create(self):
        """
        Return the UI structure
        """
        # Use a single file component defined elsewhere
        measure1 = DC.Component("Length", defaults=["250","yd","m"], inch_base=False).create()
        measure2 = DC.Component("Width", defaults=["22","yd","m"], inch_base=False).create()
        return (
            ltk.VBox(
                ltk.HorizontalSplitPane(  # or VerticalSplitPane if your UI is better that way
                    ltk.Div(  # put your UI in here
                        # - can easily just remove these dummy panes when you no longer need the terminal
                        ltk.VBox(
                            ltk.Button("Click me!", self.params.button_click_handler).attr("id","my-button"),
                            self.label_box(),
                            ltk.HBox(
                                ltk.Label("Draw-in").addClass("basetext"),
                                ltk.Input(self.params.Drawin).attr("type","number").attr("id","drawin").addClass("short")
                            ),
                            measure1,
                            measure2
                        ),
                        ltk.Div().attr("id", "graphic"),
                        # our description
                        ltk.Paragraph("<br>".join(self.explanation)).attr("id","explanation").addClass("description")
                    ).attr("id", "mydiv").css("border", "2px solid red"),
                    # Other side for the terminal
                    ltk.Div().attr("id", "forterm").css("border", "2px solid green"),
                    "Temp-split-pane"
                )
             )
        )

    
if __name__ == "__main__":
    g_widget = UI_widget()
    widget = g_widget.create()
    widget.appendTo(ltk.window.document.body)  # ui is now running
    #
    # move terminal to sliding pane
    term = ltk.find("py-terminal")[0]
    term_box = ltk.find("#forterm")[0]
    term_box.appendChild(term)
    #
    print(f"The Terminal: ({"mpy" if MICROPYTHON else "pyodide"})")
    # svg insert into Div
    somesvg = create_svg_box()
    ltk.find("#graphic").html(somesvg.outerHTML)

    