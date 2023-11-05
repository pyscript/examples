import json

from js import Bokeh, JSON

from bokeh.embed import json_item
from bokeh.plotting import figure

# create a new plot with default tools, using figure
p = figure(width=400, height=400)

# add a circle renderer with x and y coordinates, size, color, and alpha
p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=15, line_color="navy", fill_color="orange", fill_alpha=0.5)
p_json = json.dumps(json_item(p, "myplot"))

Bokeh.embed.embed_item(JSON.parse(p_json))
