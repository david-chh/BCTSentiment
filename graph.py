#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load graph, rank influential people.

@author: ethanweber
"""

import networkx as nx
import pandas as pd
import random

"""Creates dummy data of 5000 or so names taken from list online"""
names = list(set(list(pd.read_csv('names.csv')['firstname'])))

"""Initializes graph"""
G = nx.Graph()

for i in range(10000):
    """"Creates graph with 10,000 edges""""
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

"""Sorts high to low"""
df.sort_values(['score'], ascending = 0)
