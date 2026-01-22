When developing an application which is larger than a demo, its useful to have a better structure.

This series is about presenting a better project-based structure.

# Part 4:
Building on ideas described in Parts 1,2,3.
 - Pyodide (full python) or Micropython
 - "Loading" animation
 - Reactive UI
 - Interactive SVG  controls

## Single File Components
We are now building a UI element from a separate component file.
This means you can construct standalone UI components to include when needed.
 - Making single file components that can be reused is critical for large projects.

In the index.html - you can uncomment script lines to run:
  - the base module that is imported 'util_units.py' which runs a test,
  - the single file component (with tests) 'dimension_component.py' which also tests/demonstrates itself,
  - or the main.py which uses the single file component twice

## All events under Reactive (Model) class
Moving all toplevel events under the Model class (which enables reactivity) means we can use this as a single file component also.
This enables anything to be used in this way.
The testing under '__main__' means a component can be tested/checked on its own and then used as a component elsewhere without further modification.

(You can use ctrl-shift while moving the mouse over ltk UI elements for descriptions of those elements.)