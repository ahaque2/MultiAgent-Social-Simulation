import time, enum, math
import numpy as np
import pandas as pd
import pylab as plt
import sys
import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector

import networkx as nx
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import pylab as pl
from IPython import display
from numba import jit
from matplotlib import cm

from bokeh.io import show, output_notebook
from bokeh.models import ColumnDataSource, GeoJSONDataSource, ColorBar, HoverTool, Legend, LinearColorMapper, ColorBar
from bokeh.plotting import figure
from bokeh.palettes import brewer
from bokeh.models.glyphs import Line
from bokeh.palettes import Category10, Viridis
output_notebook()
import panel as pn
import panel.widgets as pnw
pn.extension()


from state import State

#Post = {'author':2 , 'content': 'A positive Trump post', 'type': 0, 'party_mention': None, 'pov': 0, 'emotion_score':{}}
cmap = ["orange", "red", "blue", 'green', 'grey']
states = ['origin', 'received', 'not-received', 'spreader', 'distinterested']
colors = dict(zip(cmap, states))

print(colors)
