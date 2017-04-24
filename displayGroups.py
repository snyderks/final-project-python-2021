"""DisplayGroups takes a list of reposts and organizes them into a graph."""

import networkx as nx
import json
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout
# import plotly.plotly as py
# from plotly.graph_objs import *

G = nx.DiGraph()

f = open("links-groups.json", "r")

dupes = json.load(f)

subreddits = {}

attr = "created"

i = 0

# iterate through all duplicate groups
for key, value in dupes.items():
    if i > 500:
        break
    if len(value) > 2:
        # iterate through each submission
        for i in range(len(value)-1):
            G.add_edge(value[i][attr], value[i+1][attr])
            if value[i][attr] not in subreddits:
                subreddits[value[i][attr]] = hash(value[i][attr])
        if value[-1][attr] not in subreddits:
            subreddits[value[-1][attr]] = hash(value[-1][attr])
        i += 1

print("Built graph")

print(G.number_of_nodes(), "nodes")

hashed = subreddits.values()

vir = plt.get_cmap("viridis")
cNorm = colors.Normalize(vmin=min(hashed), vmax=max(hashed))
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=vir)

allColors = []

for node in G.nodes():
    strHash = subreddits[node]
    colorVal = scalarMap.to_rgba(strHash)
    allColors.append(colorVal)

print("Built colors")

nx.draw(G, pos=graphviz_layout(G), node_size=25, arrows=True, width=0.25, node_color=allColors)

print("Drawing graph...")

plt.show()
