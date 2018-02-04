#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:36:30 2018

@author: ethanweber
"""

import networkx as nx
import pandas as pd
import random
names = list(set(list(pd.read_csv('names.csv')['firstname'])))

G = nx.Graph()

for i in range(10000):
    G.add_edge(names[random.randint(0,len(names)-1)], names[random.randint(0,len(names)-1)])

ranks = nx.pagerank(G)

df = pd.DataFrame()

df['names'] =  list(ranks.keys())
def get_rank(name, rank_dict):
    try:
        return rank_dict[name]
    except:
        return 0
    
df['score'] = list(map(lambda x: get_rank(x, ranks), list(df.names)))

df.sort_values(['score'], ascending = 0)
