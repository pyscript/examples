import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np

from js import console
from pyodide_http import patch_all
patch_all()

pn.extension(design='material')

csv_file = ("https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv")
data = pd.read_csv(csv_file, parse_dates=["date"], index_col="date")
console.log("Downloaded data")

# Panel Widgets
variable_widget = pn.widgets.Select(name="variable", value="Temperature", options=list(data.columns))
window_widget = pn.widgets.IntSlider(name="window", value=30, start=1, end=60)
sigma_widget = pn.widgets.IntSlider(name="sigma", value=10, start=0, end=20)
console.log("Set up widgets!")

# Interactive hvplot pipeline
## Compute the outliers
data = data.interactive()
avg = data[variable_widget].rolling(window=window_widget).mean()
residual = data[variable_widget] - avg
std = residual.rolling(window=window_widget).std()
outliers = np.abs(residual) > std * sigma_widget

## Plot the average variable line together with the outliers as points
pipeline = (
    avg.hvplot(height=300, width=400, color="blue", legend=False)
    * avg[outliers].hvplot.scatter(color="orange", padding=0.1, legend=False)
)

# Compute the number of outliers
count = outliers.pipe(
    lambda s: pn.indicators.Number(
        name='Outliers count', value=s.sum(),
        colors=[(10, 'green'), (30, 'gold'), (np.Inf, 'red')]
    )
)

# Servable App
pn.Column(pipeline.widgets(), pn.Row(count.output(), pipeline.output())).servable(target='panel')
