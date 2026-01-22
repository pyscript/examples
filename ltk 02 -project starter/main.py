#imports
import ltk
import svg as SVG
import random
from pyscript import config
MICROPYTHON = config["type"] == "mpy"  # if we need to know if we're running pyodide or micropython

if '__terminal__' in locals():
    __terminal__.resize(60, 30)

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

def button_click_handler(event):
    print("The button has been clicked, the svg transformed")
    # move the svg child
    x,y = random.randrange(0, 100-20), random.randrange(0, 100-20)
    ltk.find("#highlight").attr("transform", f"translate({x} {y})")

class UI_widget(object):
    """
    Top level object that shows App.
    """

    def __init__(self):
        self.explanation = ["Ltk project example:","- Swap between micropython or pyodide in index.html",
                            "- Everything from starter_01 but using the Ltk for UI instead",
                            "- 'Ltk' used instead of direct dom manipulation",
                            "- Ltk has jQuery base, so can also use that approach for Selectors and dom manipulation",
                            "- The Terminal is in a top level slider. Try moving it out of the way",
                            "- SVG is included for more complex UIs"
                          ]
    
    def create(self):
        info_paragraph = ltk.Paragraph("<br>".join(self.explanation)).attr("id","explanation").addClass("description")
        return (ltk.VBox(
                    ltk.HorizontalSplitPane(  # or VerticalSplitPane if your UI is better that way
                        ltk.Div(
                            # put your UI in here
                            # - can easily just remove these dummy panes when you no longer need the terminal
                            ltk.Div(
                                ltk.Button("Click me!", button_click_handler).attr("id","my-button")
                            ),
                            ltk.Div().attr("id", "graphic"),
                            # overall description
                            info_paragraph
                        ).attr("id", "mydiv").css("border", "2px solid red"),
                        
                        # For the terminal
                        ltk.Div().attr("id", "forterm").css("border", "2px solid green"),
                    "Temp-split-pane"
                    )
                 ))

    
if __name__ == "__main__":
    w = UI_widget()
    widget = w.create()
    widget.appendTo(ltk.window.document.body)

    # move terminal to sliding pane using one of these methods:
    # - the usual Javascript mechanism
    term = ltk.window.document.getElementsByTagName("py-terminal")[0]
    term_box = ltk.window.document.getElementById("forterm")
    # - OR
    # Using ltk.find - jquery style selectors and python lists
    term = ltk.find("py-terminal")[0]
    term_box = ltk.find("#forterm")[0]
    #
    term_box.appendChild(term)
    # - OR
    # Using the jQuery interface with all Jquery chaining flexibility
    ltk.jQuery("#forterm")[0].append(ltk.jQuery("py-terminal")[0])
    # remind us of py/mpy
    print(f"The Terminal: ({"mpy" if MICROPYTHON else "pyodide"})")
    # svg insert into Div
    somesvg = create_svg_box()
    ltk.find("#graphic").html(somesvg.outerHTML)

    