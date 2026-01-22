from pyscript.web import page, div, button, span, br
from pyscript import when, window, config
MICROPYTHON = config["type"] == "mpy"  # if we need to know if we're running pyodide or micropython

if '__terminal__' in locals():
    __terminal__.resize(60, 10)

def add_ui(toplevelpage):
    toplevelpage.append(
        div(
            button(span("Hello! "), span("World!")),
            br(),
            button("Click me!", id="my-button"),
            classes=["css-class1", "css-class2"],
            style={"border": "2px dashed red"}
            ))

def my_button_click_handler(event):
    print("The button has been clicked!")
    
if __name__ == "__main__":
    print(f"Printing to Terminal: ({"mpy" if MICROPYTHON else "pyodide"})")
    add_ui(page)
    # UI built
    when("click", "#my-button", handler=my_button_click_handler)
    # explain
    explanation = ["Index example:","- Specify micropython or pyodide in index.html",
                   "  - two manual changes needed in index.html to swap",
                   "- Add a loading animation",
                   "- Include a resized Terminal for manual debugging",
                   "- basic pyscript.web based dom manipulation"
                  ]
    print("\n".join(explanation))
    