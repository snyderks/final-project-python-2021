"""DisplayGroups takes a list of reposts and organizes them into a graph."""

import networkx as nx
import json
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# import matplotlib.cm as cmx
# import pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout
import plotly.offline as py
from plotly.graph_objs import XAxis, YAxis, Layout, Scatter, Marker, Figure, Data, Line

G = nx.DiGraph()

f = open("links-groups.json", "r")

dupes = json.load(f)

subreddits = {}

# all the items included in the graph, indexed by name
addedDupes = {}

# a list of url portions that we don't want included, since it results in
# series of reposts that aren't related but have the same base url.
blacklistQueries = ["p=", "article=", "articolo=", "search_query=",
                    "all_comments=", "id=", "page=", "Id=", "slug=",
                    "?v=", "item=", "?i=", "mediafire", "google.com/url?",
                    "view=", "search="]

# the attribute of each post to use as the key.
# names for posts are unique IDs.
attr = "name"

# string to mark a deleted user
deleted = "[deleted]"

# counter for the number of chains to have
i = 0

# iterate through all duplicate groups
for key, value in dupes.items():
    # have no more than 40 chains
    if i > 40:
        break

    # whether the url matches any of the blacklisted portions
    containsQueries = True in [(x in value[0]["url"]) for x in blacklistQueries]
    # not explicit content, chain length is between 10 and 50, doesn't contain blacklist
    if len(value) > 10 and len(value) < 50 and value[0]["over_18"] is False and not containsQueries:
        allHaveAuthor = False not in [("author" in x) for x in value]
        # iterate through each submission
        for i in range(len(value)-1):
            # build the edge
            G.add_edge(value[i][attr], value[i+1][attr])
            # hash the date, add the item to the record of what was added to the graph
            if value[i][attr] not in subreddits:
                subreddits[value[i][attr]] = hash(value[i]["created"])
                addedDupes[value[i][attr]] = value[i]
            # and now add edges between posts with the same author
            # but only if they all have an author
            if allHaveAuthor and value[i]["author"] != deleted:
                for x in [x[attr] for x in value if x["author"] == value[i]["author"]]:
                    G.add_edge(value[i][attr], x)
        # include the last item
        if value[-1][attr] not in subreddits:
            subreddits[value[-1][attr]] = hash(value[-1]["created"])
            addedDupes[value[-1][attr]] = value[-1]
        i += 1

print("Built graph")

print(G.number_of_nodes(), "nodes")

hashed = subreddits.values()

# lay out the nodes of the graph using graphviz
pos=graphviz_layout(G)

# add the generated positions to the nodes as an attribute
for node in G.nodes():
    G.node[node]["pos"] = pos[node]

# create a list of edges
edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.8,color='#888'),
    hoverinfo='none',
    mode='lines')

# populate the edges with the locations for each node they connect to
for edge in G.edges():
    x0, y0 = G.node[edge[0]]['pos']
    x1, y1 = G.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

# build the nodes
# Marker signifies the color and textbox attributes for the node
node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=False,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        line=dict(width=1)))

# add the label text to each node
for node in G.nodes():
    # get some info about the node
    nodeData = addedDupes[node]

    node_info = "Subreddit: " + nodeData["subreddit"] + "<br>"
    node_info += " Upvotes: " + str(nodeData["ups"]) + "<br>"
    node_info += " Title: " + nodeData["title"][0:min(50, len(nodeData["title"]))] + "<br>"
    # not all posts have author data
    if "author" in nodeData:
        node_info += " User: " + nodeData["author"] + "<br>"
    node_info += " URL: " + nodeData["url"][0:min(50, len(nodeData["url"]))]
    node_trace['text'].append(node_info)

    node_trace['marker']['color'].append(hash(node))

# build the figure
fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                width=1000,
                height=1000,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

for node in G.nodes():
    x, y = G.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

print("Built colors")

py.plot(fig)

print("Drawing graph...")
