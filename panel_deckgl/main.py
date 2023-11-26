import panel as pn
import pandas as pd
import param

from pyodide.http import open_url

MAPBOX_KEY = "pk.eyJ1IjoicGFuZWxvcmciLCJhIjoiY2s1enA3ejhyMWhmZjNobjM1NXhtbWRrMyJ9.B_frQsAVepGIe-HiOJeqvQ"

class App(param.Parameterized):
    data = param.DataFrame(precedence=-1)
    view = param.DataFrame(precedence=-1)
    arc_view = param.DataFrame(precedence=-1)
    radius = param.Integer(default=50, bounds=(20, 1000))
    elevation = param.Integer(default=10, bounds=(0, 50))
    hour = param.Integer(default=0, bounds=(0, 23))
    speed = param.Integer(default=1, bounds=(0, 10), precedence=-1)
    play = param.Event(label='▷')

    def __init__(self, **params):
        self.deck_gl = None
        super().__init__(**params)
        self.deck_gl = pn.pane.DeckGL(
            dict(self.spec),
            mapbox_api_key=MAPBOX_KEY,
            throttle={'click': 10},
            sizing_mode='stretch_both',
            margin=0
        )
        self.deck_gl.param.watch(self._update_arc_view, 'click_state')
        self._playing = False
        self._cb = pn.state.add_periodic_callback(
            self._update_hour, 1000//self.speed, start=False
        )

    @property
    def spec(self):
        return {
            "initialViewState": {
                "bearing": 0,
                "latitude": 40.7,
                "longitude": -73.9,
                "maxZoom": 15,
                "minZoom": 5,
                "pitch": 40.5,
                "zoom": 11
            },
            "layers": [self.hex_layer, self.arc_layer],
            "mapStyle": "mapbox://styles/mapbox/dark-v9",
            "views": [
                {"@@type": "MapView", "controller": True}
            ]
        }

    @property
    def hex_layer(self):
        return {
            "@@type": "HexagonLayer",
            "autoHighlight": True,
            "coverage": 1,
            "data": self.data if self.view is None else self.view,
            "elevationRange": [0, 100],
            "elevationScale": self.elevation,
            "radius": self.radius,
            "extruded": True,
            "getPosition": "@@=[pickup_x, pickup_y]",
            "id": "8a553b25-ef3a-489c-bbe2-e102d18a3211"
        }

    @property
    def arc_layer(self):
        return {
            "@@type": "ArcLayer",
            "id": 'arc-layer',
            "data": self.arc_view,
            "pickable": True,
            "getWidth": 1,
            "getSourcePosition": "@@=[pickup_x, pickup_y]",
            "getTargetPosition": "@@=[dropoff_x, dropoff_y]",
            "getSourceColor": [0, 255, 0, 180],
            "getTargetColor": [240, 100, 0, 180]
        }

    def _update_hour(self):
        self.hour = (self.hour+1) % 24

    @param.depends('view', watch=True)
    def _update_arc_view(self, event=None):
        data = self.data if self.view is None else self.view
        if not self.deck_gl or not self.deck_gl.click_state:
            self.arc_view = data.iloc[:0]
            return
        lon, lat = self.deck_gl.click_state['coordinate']
        tol = 0.001
        self.arc_view = data[
            (df.pickup_x>=float(lon-tol)) &
            (df.pickup_x<=float(lon+tol)) &
            (df.pickup_y>=float(lat-tol)) &
            (df.pickup_y<=float(lat+tol))
        ]

    @param.depends('hour', watch=True, on_init=True)
    def _update_hourly_view(self):
        self.view = self.data[self.data.hour==self.hour]

    @param.depends('speed', watch=True)
    def _update_speed(self):
        self._cb.period = 1000//self.speed

    @param.depends('play', watch=True)
    def _play_pause(self):
        if self._playing:
            self._cb.stop()
            self.param.play.label = '▷'
            self.param.speed.precedence = -1
        else:
            self._cb.start()
            self.param.play.label = '❚❚'
            self.param.speed.precedence = 1
        self._playing = not self._playing

    @param.depends('view', 'radius', 'elevation', 'arc_view', watch=True)
    def update_spec(self):
        if self.deck_gl:
            self.deck_gl.object = dict(self.spec)

url = 'https://s3.eu-west-1.amazonaws.com/assets.holoviews.org/data/nyc_taxi_wide.csv'
df = pd.read_csv(open_url(url))
app = App(data=df)
controls = pn.Param(app.param, sizing_mode='stretch_width', show_name=False)

app.deck_gl.servable(target='plot')
controls.servable(target='widgets')
