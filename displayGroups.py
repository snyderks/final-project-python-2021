"""DisplayGroups takes a list of reposts and organizes them into a graph."""

import networkx as nx
import json
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

G = nx.DiGraph()

f = open("links-groups.json", "r")

dupes = json.load(f)

subreddits = {}

# iterate through all duplicate groups
for key, value in dupes.items():
    # iterate through each submission
    for i in range(len(value)-1):
        G.add_edge(value[i]["subreddit"], value[i+1]["subreddit"])
        if value[i]["subreddit"] not in subreddits:
            subreddits[value[i]["subreddit"]] = hash(value[i]["subreddit"])
    if value[-1]["subreddit"] not in subreddits:
        subreddits[value[-1]["subreddit"]] = hash(value[-1]["subreddit"])

hashed = subreddits.values()

vir = plt.get_cmap("viridis")
cNorm = colors.Normalize(vmin=min(hashed), vmax=max(hashed))
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=vir)

allColors = []

for node in G.nodes():
    strHash = subreddits[node]
    colorVal = scalarMap.to_rgba(strHash)
    allColors.append(colorVal)

nx.draw_spring(G, node_size=25, arrows=True, width=0.25, node_color=allColors)

plt.show()
