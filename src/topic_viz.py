import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, Range1d
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
import pandas as pd


# import data

X = np.array(np.load("./final_X_25krandomwords.npy")).astype(float)
X_fischerLDA = np.array(np.load("./X_fischerLDA.npy")).astype(float)
raw_data = pd.read_csv("../data/raw_data.csv", index_col=0)

# few constants

to_theme = {0: "life science",
            1: "mechanics",
            2: "",
            3: "",
            4: "materials",
            5: "",
            6: "",
            7: "materials",
            8: "electricity",
            9: "",
            10: "chemistry",
            11: "information",
            12: "optics",
            13: "",
            14: "",
            15: "transport",
            16: "thermodynamics",
            17: "chemistry",
            18: "",
            19: "",
            20: "",
            21: "",
            22: "",
            23: "",
            24: "materials",
            25: "chemistry",
            26: "chemistry",
            27: "",
            28: "mechanics",
            29: "electricity"
           }
nonnull_idx = [i for (i,t) in list(to_theme.items()) if t]
nonnull_topics = [t for (i,t) in list(to_theme.items()) if t]
to_theme = dict(enumerate(nonnull_topics))
a = 14178
b = 14194


# set up slider

year_slider = Slider(title="year", value=1975, start=1960, end=2015, step=1)

TOOLS="resize,crosshair,pan,wheel_zoom,box_zoom,reset,tap,previewsave,box_select,poly_select, hover, undo, redo"

# create the figure
p = figure(tools=TOOLS, plot_width=700, plot_height=700, min_border=10,
min_border_left=50, toolbar_location="above", x_axis_location=None,
y_axis_location=None, x_range=Range1d(-10, 6), y_range=Range1d(-9,11))

p.background_fill_color = "#fafafa"

# ### Add the background year text
# We add this first so it is below all the other glyphs
text_source = ColumnDataSource({'year': ['lol']})
text = Text(x=-4, y=0, text='year', text_font_size='120pt', text_color='#EEEEEE')
p.add_glyph(text_source, text)

x=[0]
y=[0]
source1 = ColumnDataSource(data=dict(x=x, y=y))
p.scatter('x', 'y', source=source1, color="#dddddd", legend="patent abstracts")

x=[0]
y=[0]
source2 = ColumnDataSource(data=dict(x=x, y=y))
p.scatter('x', 'y', source=source2, color="red", size=20, alpha=.5, marker="circle_x", legend="year's average patent")

# ---- plot the topic centroids
centroids = ColumnDataSource(data=dict(
        x=X_fischerLDA[a:b,0],
        y=X_fischerLDA[a:b,1],
        qualifier=["topic center"]*(b-a),
        content=list(to_theme.values())
    ))

p.scatter('x', 'y', source=centroids, color="green",
          size=20, alpha=.7, marker="cross", legend="topic center")

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Type", "@qualifier"),
    ("Content", "@content")
]

# Set up callbacks

def update_data(attrname, old, new):

    # Get the current slider values
    year = year_slider.value

    # slice data
    indices = raw_data.year.isin([year])
    indices = [i for i,boo in enumerate(indices) if boo]
    X_tmp = X_fischerLDA[[indices]]

    # ---- plot all dots
    source1.data = dict(
            x=X_tmp[:,0],
            y=X_tmp[:,1],
            qualifier=["patent abstract"]*X_tmp.shape[0],
            content=[s[:80] for s in raw_data[raw_data.year == year].abstract.values])

    # ---- plot the years avg
    source2.data = dict(
            x=[np.mean(X_tmp[:,0])],
            y=[np.mean(X_tmp[:,1])],
            qualifier=["year's average patent"],
            content=[""])

year_slider.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(year_slider)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
