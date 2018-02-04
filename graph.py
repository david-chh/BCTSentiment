#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load graph, rank influential people.

@author: ethanweber
"""

import networkx as nx
import pandas as pd
import random

names = list(pd.read_csv('ripple.csv')['author'])

"""Initializes graph"""
G = nx.Graph()

for i in range(len(names)*300):
    G.add_edge(names[random.randint(0,len(names)-1)], names[random.randint(0,len(names)-1)])
    
"""implements pagerank"""
ranks = nx.pagerank(G)

df = pd.DataFrame()

"""puts those ranks in a dataframe"""
df['names'] =  list(ranks.keys())
def get_rank(name, rank_dict):
    try:
        return rank_dict[name]
    except:
        return 0
    
df['score'] = list(map(lambda x: get_rank(x, ranks), list(df.names)))
df.score = df.score*100
df.sort_values(['score'], ascending = 0)
