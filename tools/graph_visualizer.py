import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

file_path = 'Filtered_Github_Repositories.csv'  # Update this path as needed
data = pd.read_csv(file_path)

G = nx.Graph()

for _, row in data.iterrows():
    G.add_node(row['repo_name'], language=row['language'], stars=row['stars'])

user_repo_dict = defaultdict(list)
for _, row in data.iterrows():
    users = row['star_users'].split('|')
    for user in users:
        user_repo_dict[user].append(row['repo_name'])

for user, repos in user_repo_dict.items():
    for i in range(len(repos)):
        for j in range(i + 1, len(repos)):
            repo1 = repos[i]
            repo2 = repos[j]
            if G.has_edge(repo1, repo2):
                G[repo1][repo2]['weight'] += 1
            else:
                G.add_edge(repo1, repo2, weight=1)

threshold = 100
edges_to_remove = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] < threshold]
G.remove_edges_from(edges_to_remove)

nodes_to_remove = [node for node in G.nodes if G.degree(node) == 0]
G.remove_nodes_from(nodes_to_remove)

languages = pd.unique(data['language'])
color_map = {lang: i for i, lang in enumerate(languages)}
node_colors = [color_map[G.nodes[node]['language']] for node in G.nodes]

node_sizes = [G.nodes[node]['stars'] / 100 for node in G.nodes]

pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

plt.figure(figsize=(20, 15))
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, cmap=plt.cm.tab20, font_size=8)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
plt.title("Filtered GitHub Repositories Graph Based on Common Star Users")
plt.show()
