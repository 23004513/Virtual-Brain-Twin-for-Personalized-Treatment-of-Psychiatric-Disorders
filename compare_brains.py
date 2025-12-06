import numpy as np
import matplotlib.pyplot as plt

time = np.linspace(0, 10, 1000)
healthy_activity = np.sin(2 * np.pi * 1.5 * time) + np.random.normal(0, 0.1, len(time))
psychiatric_activity = np.sin(2 * np.pi * 1.5 * time) + np.random.normal(0, 0.4, len(time))
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(time, healthy_activity, color='green')
plt.title(" Healthy Brain Activity")
plt.ylabel("Signal Strength")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(time, psychiatric_activity, color='red')
plt.title(" Psychiatric Brain Activity")
plt.xlabel("Time (s)")
plt.ylabel("Signal Strength")
plt.grid(True)

plt.tight_layout()
plt.show()
