### Code to visualize the sanction graph and social network

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
# from numba import jit
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

class Visualization:

    def plot_sanction_graph(self, graph):

        fig,ax=plt.subplots(1, 1, figsize=(16,10))
        pos = nx.spring_layout(graph)
        labels = nx.get_edge_attributes(graph,'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        nx.draw(graph, pos, with_labels=True, alpha=0.9, font_size=14)
        
        return
        
    def plot_pol_network(self, graph, cmap):
        
        fig,ax=plt.subplots(1, 1, figsize=(16,10))
        pos = nx.kamada_kawai_layout(graph)
        
        nx.draw(graph, pos, node_size=600, edge_color='gray', node_color=cmap, with_labels=True, alpha=0.9, font_size=14, ax=ax)
        
        return
    
    def plot_sim_network(self, graph, states):
        
        fig,ax=plt.subplots(1, 1, figsize=(16,10))
        pos = nx.kamada_kawai_layout(graph)
        
        cmap = ListedColormap(["orange", "red", "lightblue", 'green', 'grey'])
        colors = [cmap(i) for i in states]
        plt.legend(graph.nodes())
        
        #print("Step ", self.sim_model.i)
        nx.draw(graph, pos, node_size=600, edge_color='gray', node_color=colors, with_labels=True, alpha=0.9, font_size=14, ax=ax)
        
        return
    
    def aggregate_sanction_graphs(self, SancGraphs):

        final_sanc_graph = nx.DiGraph()
        for g in SancGraphs:
            #Visualization().plot_sanction_graph(g)
            edges = g.edges.data()
            #print(edges)
            for ed in edges:
                n1 = ed[0]
                n2 = ed[1]
                w = ed[2]['weight']

                if(n1 not in final_sanc_graph):
                    final_sanc_graph.add_node(n1)

                if(n2 not in final_sanc_graph):
                    final_sanc_graph.add_node(n1)

                if((n1, n2) not in final_sanc_graph.edges):
                    final_sanc_graph.add_edge(n1, n2, weight = w)

                else:
                    final_sanc_graph[n1][n2]['weight'] += w
                    final_sanc_graph[n1][n2]['weight'] = round(final_sanc_graph[n1][n2]['weight'], 6)

        return final_sanc_graph

    def xy_normalized(self, l, lower, upper):

        l_inv = [1-abs(x) if x>0 else abs(x) for x in l]
        l_norm = [lower + (upper - lower) * x for x in l_inv]
        return l_norm

    def add_pol_polarity_score(self, data, col):

        num = data.shape[0]
        data['ppol'] = num * [0.50]

        values = data[data[col] > 0][col]
        norm_values = self.xy_normalized(values, 0.15, 0.30)
        data['ppol'].loc[data[data[col] > 0].index] = norm_values
        
        values = data[data[col] < 0][col]
        norm_values = self.xy_normalized(values, 0.75, 0.90)
        data['ppol'].loc[data[data[col] < 0].index] = norm_values

        color_map = [cm.jet(x) for x in data['ppol']]

        return color_map