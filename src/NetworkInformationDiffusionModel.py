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

from Agent import MyAgent

import networkx as nx
from numba import jit


class NetworkInformationDiffusionModel(Model):
    """A model for information diffusion."""
    
    def __init__(self, post, G, se_flag, se_threshold):
        
        self.post = post
        self.i = -1
        
        self.G = G
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        self.running = True
        
        self.G_share = nx.DiGraph()
        
        self.G_sharing = G
        self.grid_sharing = NetworkGrid(self.G)
        
        # Create agents
        self.agents = []
        for i, node in enumerate(self.G.nodes()):
            a = MyAgent(i, self, se_flag, se_threshold, self.G)
            self.agents.append(a)
            self.grid.place_agent(a, node)
 
        self.agents[self.post['author']].create_post()
        self.datacollector = DataCollector(
            agent_reporters={"State": "state"})
        
    @jit
    def step(self, i):
        
        self.i = i
        self.datacollector.collect(self)
        self.schedule.step()