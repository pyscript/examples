import panel as pn

pn.extension()

slider = pn.widgets.FloatSlider(start=0, end=10, name="Amplitude")


def callback(new):
    return f"Amplitude is: {new}"


pn.Row(slider, pn.bind(callback, slider)).servable(target="simple_app")
