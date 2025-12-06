
import networkx as nx
import matplotlib.pyplot as plt
import random
brain = nx.Graph()
regions = ["Frontal", "Parietal", "Temporal", "Occipital", "Cerebellum", "Limbic"]
brain.add_nodes_from(regions)
for i in range(len(regions)):
    for j in range(i + 1, len(regions)):
        weight = round(random.uniform(0.1, 1.0), 2)  # random connection strength
        brain.add_edge(regions[i], regions[j], weight=weight)
pos = nx.spring_layout(brain, seed=42)  # layout for visualization
weights = nx.get_edge_attributes(brain, 'weight')
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(brain, pos, node_size=1500, node_color='lightblue')
nx.draw_networkx_labels(brain, pos, font_size=10, font_weight='bold')
nx.draw_networkx_edges(brain, pos, width=2, edge_color='gray')
nx.draw_networkx_edge_labels(brain, pos, edge_labels=weights, font_color='red')
plt.title("Digital Brain Model – Virtual Brain Twin", fontsize=14, fontweight='bold')
plt.axis('off')
plt.savefig("digital_brain_model.png")
plt.show()
print("Digital brain model created successfully!")
print("Connections (Region1 → Region2 = Coupling Strength):")
for u, v, w in brain.edges(data=True):
    print(f"  {u} ↔ {v} = {w['weight']}")
