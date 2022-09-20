import time, enum, math
import numpy as np
import pandas as pd
import pylab as plt
import sys
import random

import networkx as nx
from sklearn.utils import shuffle
    
class Data:  
    
    def __init__(self, seed):
        
        random.seed(seed)
        np.random.seed(seed)
    
    def creat_social_network(self, edges):

        G = nx.Graph()
        lines = edges.split("\n")
        for e in lines:
            nodes = e.split()
            if(len(nodes) > 1):
                if(nodes[0] not in G):
                    G.add_node(nodes[0])
                if(nodes[1] not in G):
                    G.add_node(nodes[1])

                G.add_edge(nodes[0], nodes[1])

        return G

    def get_fb_network(self, df):

        fb_network = open('../../data/facebook_combined.txt', 'r').read()
        G = self.creat_social_network(fb_network)
        A = nx.adjacency_matrix(G).todense()
        A = np.array(A)
        n = A.shape[0]
        G = nx.from_numpy_matrix(A)

        node_attr = df.set_index('id').to_dict('index')
        nx.set_node_attributes(G, node_attr)

        return G
    
    def normalize(self, values, bounds_dlower, bounds_alower, bounds_dupper, bounds_aupper):
        return [bounds_dlower + (x - bounds_alower) * (bounds_dupper - bounds_dlower) / (bounds_aupper - bounds_alower) for x in values]
    
    def get_agent_pol_inclinations(self, df, n_issues):

        issues = ['issue_' + str(x) for x in range(n_issues)]
        
        pol_inclination = df[issues].mean(axis = 1)
        pol_inclination = pol_inclination.clip(-1, 1)

        if(any(pol_inclination) < -1 or any(pol_inclination) > 1):
            print("Pol inclination exceed 1 or is lowers than -1 \n", df)
            sys.exit()

        return pol_inclination


#     def get_agent_pol_inclinations(self, df, n_issues):

#             dem_fav_topics = ['issue_' + str(x) for x in range(n_issues) if x%2 == 0]
#             rep_fav_topics = ['issue_' + str(x) for x in range(n_issues) if x%2 == 1]
#             mean_rep_support = df[rep_fav_topics].mean(axis = 1)
#             mean_dem_support = df[dem_fav_topics].mean(axis = 1) 

#             pol_inclination = mean_dem_support - mean_rep_support

#             pol_inclination = pol_inclination.clip(-1, 1)

#             if(any(pol_inclination) < -1 or any(pol_inclination) > 1):
#                 print("Pol inclination exceed 1 or is lowers than -1 \n", df)
#                 sys.exit()

#             return pol_inclination
        

    def add_issue_stance(self, df, G, issue_ids, n_issues):
    
        mean_norm = lambda x: np.round((x-x.mean())/(x.max() - x.min()), 6)
        for i in issue_ids:

            dist = mean_norm(np.random.normal(loc=0.0, scale=1.0, size=df.shape[0]))
            dist = 2.*(dist - np.min(dist))/np.ptp(dist)-1

            df['issue_'+str(i)] = dist
        df['pol_inclination'] = self.get_agent_pol_inclinations(df, n_issues)
        
        node_attr = df.set_index('id').to_dict('index')
        nx.set_node_attributes(G, node_attr)

        return G, df


    def get_social_network(self, n_issues):

        G = nx.karate_club_graph()
        # fb_network = open('../data/facebook_combined.txt', 'r').read()
        # G = self.creat_social_network(fb_network)
        A = nx.adjacency_matrix(G).todense()
        A = np.array(A)
        n = A.shape[0]
        G = nx.from_numpy_matrix(A)

        df = pd.DataFrame()
        df['id'] = range(n)

        min_max_norm = lambda x: np.round((x-x.min())/(x.max() - x.min()), 6)
        mean_norm = lambda x: np.round((x-x.mean())/(x.max() - x.min()), 6)

        df['user_activity'] = min_max_norm(np.random.normal(loc=0.5, scale=0.5, size=n))
        df['privacy_preference'] = min_max_norm(np.random.normal(loc=0.5, scale=0.5, size=n))
        df['user_satisfaction'] = [0] * n

        for i in range(n_issues):    
            # df['issue_'+str(i)] = [0] * df.shape[0]
            dist = np.random.normal(loc=0.0, scale=0.25, size=n)
            dist = self.normalize(dist, -1, min(dist), 1, max(dist))
            df['issue_'+str(i)] = dist
            #post_conf = pd.DataFrame(dist1 + dist2, columns = ['stance'])
            
            #df['issue_'+str(i)] = min_max_norm(np.array([round(x,6) if x<1 else 1 for x in np.random.normal(loc=0.5, scale=0.5, size=n)]))
            
        df['pol_inclination'] = self.get_agent_pol_inclinations(df, n_issues)
            
        node_attr = df.set_index('id').to_dict('index')
        nx.set_node_attributes(G, node_attr)

        return G, df

    def generate_posts(self, n_posts, n_issues):
        
        n = int(n_posts/(n_issues*2)) 
        df = pd.DataFrame()
        for i in range(n_issues):

            dist = np.random.normal(loc=0.5, scale=0.25, size=n)
            dist1 = self.normalize(dist, 0, min(dist), 1, max(dist))
            dist2 = self.normalize(dist, 0, min(dist), -1, max(dist))
            post_conf = pd.DataFrame(dist1 + dist2, columns = ['stance'])
            post_conf['issue'] = i
            df = pd.concat((df, post_conf), axis = 0)
            
        df = shuffle(df)
        return df
    
    def generate_skewed_posts(self, n_posts, n_issues, issue_id, proportion):
        
        majClass_n = int(n_posts * proportion)
        minClass_n = int((n_posts - majClass_n)/(2*(n_issues-1)))
        
        #print(n_posts, majClass_n, minClass_n)
        
        df = pd.DataFrame()
        for i in range(n_issues):
            
            if(i == issue_id):
                dist = np.random.normal(loc=0.5, scale=0.25, size=int(majClass_n/2))
            else:
                dist = np.random.normal(loc=0.5, scale=0.25, size=minClass_n)
            dist1 = self.normalize(dist, 0, min(dist), 1, max(dist))
            dist2 = self.normalize(dist, 0, min(dist), -1, max(dist))
            post_conf = pd.DataFrame(dist1 + dist2, columns = ['stance'])
            post_conf['issue'] = i
            df = pd.concat((df, post_conf), axis = 0)
            
        df = shuffle(df)
        return df
    
    def compute_polarization(self, pol_incl):
    
        mu = 0
        pop1 = pol_incl[pol_incl > 0]
        pop2 = pol_incl[pol_incl < 0]
        
        if(pop1.shape[0] != 0 and pop2.shape[0] != 0):
            
            dA = abs(len(pop1) - len(pop2))/pol_incl.shape[0]
            d = abs(pop1.mean() - pop2.mean())/2
            mu = (1-dA) * d

        return mu

    
    