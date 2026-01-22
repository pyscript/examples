When developing an application which is larger than a demo, its useful to have a better structure.

This series is about presenting a better project-based structure.

# Part 1:

## Pyodide (full python) or Micropython
We want to delay the decision of choosing between these two as long as possible.
To this end the index.html has both possible with Pyodide initially disabled.

## Loading animation
The very first time a user hits your page, there will be a delay.
This delay will always be longer for Pyodide than for Micropython.
The index.html has a preloading section for required css and a modal dialog.

## Terminal
When initially developing it's often useful to have the python terminal available.
The terminal takes up a bit of room but it can be resized.

## Initial user interaction
Dom manipulation is supported via pyscript.web
Next steps are to go to the ltk for all screen UI
