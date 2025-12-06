import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Brain regions
regions = ["Frontal", "Parietal", "Occipital", "Temporal", "Limbic", "Cerebellum"]

# Random 3D coordinates for each region
np.random.seed(42)
coords = np.random.rand(len(regions), 3)

# Random connectivity strengths
connections = np.random.rand(len(regions), len(regions))

# Create 3D figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_title("🧠 Virtual Brain Twin - 3D Neural Connectivity", fontsize=13, fontweight='bold')

# Plot nodes
for i, region in enumerate(regions):
    ax.scatter(coords[i, 0], coords[i, 1], coords[i, 2], s=200, color='skyblue', edgecolor='black')
    ax.text(coords[i, 0], coords[i, 1], coords[i, 2]+0.03, region, fontsize=10, ha='center', fontweight='bold')

# Plot connections
for i in range(len(regions)):
    for j in range(i+1, len(regions)):
        strength = connections[i, j]
        if strength > 0.4:  # show only strong connections
            ax.plot(
                [coords[i, 0], coords[j, 0]],
                [coords[i, 1], coords[j, 1]],
                [coords[i, 2], coords[j, 2]],
                color='purple', alpha=strength, linewidth=2*strength
            )

ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

plt.show()
