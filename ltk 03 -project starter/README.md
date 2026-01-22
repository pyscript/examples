When developing an application which is larger than a demo, its useful to have a better structure.

This series is about presenting a better project-based structure.

# Part 3:
Building on ideas described in Parts 1,2,3.
 - Pyodide (full python) or Micropython
 - "Loading" animation

Now adding:
## Reactive UI
The Ltk has a Reaactive parameter capability where named instance variables become reactive in the UI.
As the user changes the UI, the python variable will update and vice versa.
There is a simple mechanism to manage race conditions when changing one reactive variable affects any number of other reactive variables.

## Interactive SVG controls
An SVG module has been added so SVG style UI can be added and full interaction is available.
Either by using transforms to existing SVG elements or replacing the SVG in whole or in part.

In this demo we transform an svg rect to a random position when the button is clicked.