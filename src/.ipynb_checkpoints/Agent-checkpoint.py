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
from numba import jit

from state import State


class MyAgent(Agent):
    
    """ An agent in an epidemic model."""
    def __init__(self, unique_id, model, se_flag, se_threshold, G):
        super().__init__(unique_id, model)
        
        self.sim_model = model
        self.user_id = unique_id
        self.state = State.NOT_RECEIVED
        self.se_flag = se_flag
        self.G = G
        self.se_threshold = se_threshold
        
    def create_post(self):
        
        self.state = State.ORIGIN
        self.model.schedule.add(self)
        self.sim_model.G_share.add_node(self.user_id)
        
    def get_user_details(self, user_id, issue_id):
        
        pol_interest = self.G.nodes[user_id]['pol_interest']
        user_activity = self.G.nodes[user_id]['user_activity']
        user_stance = self.G.nodes[user_id]['issue_' + str(int(issue_id))]
        privacy_preference = self.G.nodes[user_id]['privacy_preference']
        
        return pol_interest, user_activity, user_stance, privacy_preference
        
    def compute_sanction_score(self, user_id):
        
        author = self.sim_model.post['author']
        issue_id = self.sim_model.post['issue']
        post_stance = self.sim_model.post['stance']
        
        pol_interest, user_activity, user_stance, privacy_preference = self.get_user_details(user_id, issue_id)
        sanction_score = user_activity * user_stance * post_stance * 10
          
        return round(sanction_score, 6)
    
    def compute_sharing_probability(self, user_id):
        
        issue_id = self.sim_model.post['issue']
        post_stance = self.sim_model.post['stance']
        
        pol_interest, user_activity, user_stance, privacy_preference = self.get_user_details(user_id, issue_id)
        sharing_prob = user_activity * abs(user_stance * post_stance) * privacy_preference * 10
        #sharing_prob = 1
           
        return round(sharing_prob, 6)
        
    def current_status(self):
        """Check current status"""
            
        if self.state == State.ORIGIN:
            self.share_post()
        
        elif self.state == State.RECEIVED:
            
            sharing_prob = self.compute_sharing_probability(self.user_id)
            rnd = self.random.random()
            
            if(rnd < sharing_prob):
                self.share_post()
                self.state = State.SPREADER
            
            else:
                self.state = State.DISINTERESTED
                
        elif self.state == State.DISINTERESTED:
            self.model.schedule.remove(self)
            

    def receiving_agents(self, agent):
        
        agent.state = State.RECEIVED
        self.model.schedule.add(agent)
        
        uid = agent.user_id
        sanction_score = self.compute_sanction_score(uid)
        self.sim_model.G_share.add_node(uid)
        self.sim_model.G_share.add_edge(uid, self.user_id, weight = sanction_score)
        
    def selective_exposure(self, neighbor_nodes):
        
        neighbor_nodes = list(neighbor_nodes)
        issue_id = self.sim_model.post['issue']
        
        user_stance = self.G.nodes[self.user_id]['issue_' + str(int(issue_id))]
        neighbour_stances = [self.G.nodes[_id]['issue_' + str(int(issue_id))] for _id in neighbor_nodes]
        
        nstance_df = pd.DataFrame()
        nstance_df['stance'] = [self.G.nodes[_id]['issue_' + str(int(issue_id))] for _id in neighbor_nodes]
        nstance_df['user_id'] = neighbor_nodes
        
        nstance_df =  nstance_df.assign(stance_diff = lambda x: (x['stance'] - user_stance))
        #nstance_df['stance'] - user_stance
        
        #df.assign(Percentage = lambda x: (x['Total_Marks'] /500 * 100))
        nstance_df['stance_diff'] = nstance_df['stance_diff'].abs()
        
        selected_neighbors = nstance_df[nstance_df['stance_diff'] <= self.se_threshold]['user_id']
        
#         pol_interest, user_activity, user_stance, privacy_preference = self.get_user_details(self.user_id, issue_id)
#         npol_interest, nuser_activity, nuser_stance, nprivacy_preference = self.get_user_details(self.user_id, issue_id)
        
#         pol_inclination = data[data['id'] == self.user_id]['issue_'+str(issue_id)].values[0]
#         neighbor_inclination = data[data['id'].isin(neighbor_nodes)]
        
#         diff = neighbor_inclination['issue_'+str(issue_id)] - pol_inclination
#         diff = diff.abs()
        
#         selected_neighbors = diff[diff <= se_threshold]
        
        return list(selected_neighbors)
    
    
    def share_post(self):
        """Find friends and share the post with them"""
        
        neighbor_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        if(self.se_flag == True):
            selected_neighbors = self.selective_exposure(neighbor_nodes)
        else:
            selected_neighbors = neighbor_nodes
        
        neighbor_agents = [
            agent
            for agent in self.model.grid.get_cell_list_contents(selected_neighbors)
            if (agent.state == State.NOT_RECEIVED)
        ]
            
        for agent in neighbor_agents:
            self.receiving_agents(agent)
            
        self.model.schedule.remove(self)
    
        
    def step(self):
        
        self.current_status()