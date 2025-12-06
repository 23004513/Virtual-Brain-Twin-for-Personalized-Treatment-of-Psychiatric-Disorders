
from tvb.simulator.lab import *
import numpy as np
import os
import ast
import re
import matplotlib.pyplot as plt

SIMULATION_LENGTH = 50000.0
COUPLING_STEPS = 20

BASE_PATH = 'C:/Users/admin/Downloads/tvb_data/tvb_data/connectivity/connectivity_96/'
WEIGHTS_FILE = BASE_PATH + 'weights.txt'
TRACT_LENGTHS_FILE = BASE_PATH + 'tract_lengths.txt'
CENTRES_FILE = BASE_PATH + 'centres.txt'
AREAS_FILE = BASE_PATH + 'areas.txt'
INFO_FILE = BASE_PATH + 'info.txt'


def custom_converter(s):
    return float(s.strip())

def extract_region_labels_final(file_path, expected_count=None):
    def clean_label(s):
        return s.strip().strip('"').strip("'").strip()
    for enc in ['utf-8', 'latin-1']:
        try:
            with open(file_path, 'r', encoding=enc, errors='ignore') as f:
                raw = f.read()
            break
        except Exception:
            raw = ""
    try:
        parsed = ast.literal_eval(raw.strip())
        if isinstance(parsed, (list, tuple)):
            labels = [clean_label(x) for x in parsed if str(x).strip()]
            if len(labels) > 1:
                return np.array(labels)
    except Exception:
        pass
    quoted = re.findall(r"""['"]([^'"]+)['"]""", raw)
    if len(quoted) > 1:
        return np.array([clean_label(x) for x in quoted])
    raw_clean = raw.strip().replace('[', '').replace(']', '')
    parts = [clean_label(p) for p in raw_clean.split(',') if clean_label(p)]
    if len(parts) > 1:
        return np.array(parts)
    lines = [clean_label(line) for line in raw.splitlines() if clean_label(line)]
    if len(lines) > 1:
        return np.array(lines)
    print("⚠️ Could not parse info.txt properly. File preview:\n", raw[:500])
    return np.array([])

try:
    with open(WEIGHTS_FILE, 'r') as f:
        first_line = f.readline()
        num_fields = len(first_line.strip().split())
    converters_num = {i: custom_converter for i in range(num_fields)}
    weights = np.loadtxt(WEIGHTS_FILE, converters=converters_num)
    tract_lengths = np.loadtxt(TRACT_LENGTHS_FILE, converters=converters_num)
    centres = np.genfromtxt(CENTRES_FILE, dtype=float).reshape(-1, 3)
    areas = np.genfromtxt(AREAS_FILE, dtype=float).flatten()
    num_regions = weights.shape[0]
    region_labels = extract_region_labels_final(INFO_FILE, expected_count=num_regions)
    if len(region_labels) != num_regions:
        print(f"Warning: Found {len(region_labels)} labels, expected {num_regions}. Auto-filling missing names.")
        region_labels = np.array([f"Region_{i+1}" for i in range(num_regions)])
    conn_temp = connectivity.Connectivity(
        weights=weights,
        tract_lengths=tract_lengths,
        centres=centres,
        areas=areas,
        region_labels=region_labels,
        number_of_regions=num_regions
    )
    conn_temp.configure()
    print(f"Success: Loaded ALL 5 structural components and configured connectivity with {num_regions} regions.")
except Exception as e:
    print(f" CRITICAL ERROR: Could not load data after all file fixes.\nOriginal Error: {e}")
    exit()

np.random.seed(42)
target_fc = np.random.rand(num_regions, num_regions)
target_fc = (target_fc + target_fc.T) / 2.0
np.fill_diagonal(target_fc, 1.0)
print(f"Target FC defined for {num_regions} regions.")


oscillator = models.Generic2dOscillator(I=np.array([3.0]), a=np.array([1.0]), tau=np.array([10.0]))
white_matter = conn_temp
coupling_function = coupling.Linear(a=np.array([0.0]))
heunint = integrators.HeunStochastic(dt=0.1, noise=noise.Additive(nsig=np.array([0.01])))
mon = (monitors.Bold(period=1000.0),)
sim = simulator.Simulator(model=oscillator, connectivity=white_matter,
                          coupling=coupling_function, integrator=heunint, monitors=mon).configure()


best_corr = -1.0
optimal_coupling_a = 0.0
coupling_range = np.linspace(0.005, 0.05, COUPLING_STEPS)

print(f"\nStarting Parameter Exploration (Fitting {COUPLING_STEPS} models)...")
for current_a in coupling_range:
    sim.coupling.a = np.array([current_a])
    sim.configure()
    data_out = sim.run(simulation_length=10000.0)
    bold_time_series = data_out[0][1].squeeze().T
    current_simulated_fc = np.corrcoef(bold_time_series)
    upper_triangle_indices = np.triu_indices(num_regions, 1)
    sim_flat = current_simulated_fc[upper_triangle_indices]
    target_flat = target_fc[upper_triangle_indices]
    correlation = np.corrcoef(sim_flat, target_flat)[0, 1]
    if correlation > best_corr:
        best_corr = correlation
        optimal_coupling_a = current_a
    print(f"  Testing a={current_a:.4f}, Correlation: {correlation:.4f}")


sim.coupling.a = np.array([optimal_coupling_a])
sim.configure()
print("\n------------------------------------------------------------")
print("--- Virtual Brain Twin is READY for Personalized Treatment ---")
print("------------------------------------------------------------")
print(f"Optimal Coupling (The Twin's Parameter): a={optimal_coupling_a:.4f}")
print(f"Best Correlation Achieved: {best_corr:.4f}")


print("\nVisualizing brain activity...")
result = sim.run()
bold_data = np.array(result[0][0])

bold_data = np.squeeze(bold_data)
if bold_data.ndim == 1:
    bold_data = bold_data[:, np.newaxis]
print("Bold data shape:", bold_data.shape)

num_regions_to_plot = min(5, bold_data.shape[1])
plt.figure(figsize=(10, 5))
for i in range(num_regions_to_plot):
    plt.plot(bold_data[:1000, i], label=f"Region {i+1}")

plt.title("Simulated Brain Activity (First 5 Regions)")
plt.xlabel("Time")
plt.ylabel("Activity")
plt.legend()
plt.tight_layout()
plt.savefig("brain_activity_plot.png")
plt.show()
