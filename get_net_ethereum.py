#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get authors, get followers, analyze as network using networkx.

This system can be scaled through implementation with scrapy and neo4j.

Beautiful soup and networkx used to push a prototype.

@author: ethanweber
"""

import urllib3
from bs4 import BeautifulSoup
import random
import os
import pprint
import re
import pandas as pd
import networkx as nx


#driver = webdriver.Chrome('/chromedriver') 

"""static file used for reproducability"""
file = 'ethereum_data.htm'
soup = BeautifulSoup(open(file), "html.parser")

def parse_for_author(html_thing, number):
    try:
        author = html_thing.find_all(attrs="author")[number].a['href'].split("/@",1)[1]
        return author
    except:
        return "escape"
    
def parse_for_url(html_thing, number):
    try:
        url = soup.find_all(attrs="articles__h2 entry-title")[number].a['href']
        return url
    except:
        return ""
    
parse_for_url(soup, 5)

def get_authors(soup):
    author_list = {}
    author_no = 0
    author = ""
    while author != 'escape':
        author = parse_for_author(soup, author_no)
        url = parse_for_url(soup, author_no)
        author_no += 1
        author_list[author] = url
    return author_list



authors_dict = get_authors(soup)
df = pd.DataFrame()
df['coin'] = ['ripple']*len(list(authors_dict.keys()))
df['author'] = pd.Series(list(authors_dict.keys()))
df['url'] =  pd.Series(list(map(lambda x: authors_dict[x], authors_dict.keys())))
authors = list((authors_dict.keys()))

"""Hacked dummy data - problem with ajax request & selenium"""
connections = []
for i in range(len(authors)):
    connections.append(random.sample(authors, random.sample(range(len(authors)- 100), 1)[0]))
df['follows'] = pd.Series(connections)

"""Initializes graph"""
G = nx.Graph()

for i in range(len(df.author)):
    for j in range(len(df.iloc[i].follows)):
            G.add_edge(df.author[i], df.iloc[i].follows[j])

ranks = nx.pagerank(G)

def get_rank(name, rank_dict):
    try:
        return rank_dict[name]
    except:
        return 0

df['score'] = list(map(lambda x: get_rank(x, ranks), list(df.author)))
df.score = df.score*20000

df = df.sort_values(['score'], ascending = 0)

df.loc[:,['coin', 'author', 'score', 'url']].to_csv('ethereum_rankings.csv')

