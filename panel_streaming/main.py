import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import numpy as np

import pandas as pd
import panel as pn
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

df = pd.DataFrame(np.random.randn(10, 4), columns=list("ABCD")).cumsum()

rollover = pn.widgets.IntInput(name="Rollover", value=15)
follow = pn.widgets.Checkbox(name="Follow", value=True, align="end")

tabulator = pn.widgets.Tabulator(df, height=450, width=400).servable(target="table")


def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = "red" if val < 0 else "green"
    return "color: %s" % color


tabulator.style.map(color_negative_red)

p = figure(height=450, width=600)

cds = ColumnDataSource(data=ColumnDataSource.from_df(df))

p.line("index", "A", source=cds, line_color="red")
p.line("index", "B", source=cds, line_color="green")
p.line("index", "C", source=cds, line_color="blue")
p.line("index", "D", source=cds, line_color="purple")


def stream():
    data = df.iloc[-1] + np.random.randn(4)
    tabulator.stream(data, rollover=rollover.value, follow=follow.value)
    value = {k: [v] for k, v in tabulator.value.iloc[-1].to_dict().items()}
    value["index"] = [tabulator.value.index[-1]]
    cds.stream(value)


cb = pn.state.add_periodic_callback(stream, 200)

pn.pane.Bokeh(p).servable(target="plot")
pn.Row(rollover, follow, width=400).servable(target="controls")
