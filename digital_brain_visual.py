import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
regions = ["Frontal", "Parietal", "Occipital", "Temporal", "Limbic", "Cerebellum"]
G = nx.Graph()
for region in regions:
    G.add_node(region)
np.random.seed(42)
for i in range(len(regions)):
    for j in range(i + 1, len(regions)):
        weight = round(np.random.uniform(0.1, 1.0), 2)
        G.add_edge(regions[i], regions[j], weight=weight)
theta = np.linspace(0, 2 * np.pi, len(regions), endpoint=False)
x = np.cos(theta) * 1.5
y = np.sin(theta)
pos = {regions[i]: (x[i], y[i]) for i in range(len(regions))}
plt.figure(figsize=(8, 6))
plt.title("Digital Brain Twin - Neural Connectivity", fontsize=14, fontweight='bold')
brain_outline = plt.Circle((0, 0), 1.8, color='lightgray', fill=False, linewidth=3)
plt.gca().add_patch(brain_outline)
edges = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edges(G, pos, width=[w * 2 for w in edges.values()], alpha=0.6, edge_color='blue')
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='skyblue', edgecolors='black')
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
for (n1, n2, w) in G.edges(data='weight'):
    x1, y1 = pos[n1]
    x2, y2 = pos[n2]
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    plt.text(mid_x, mid_y, str(w), color='red', fontsize=8, ha='center', va='center')

plt.axis('off')
plt.tight_layout()
plt.show()
