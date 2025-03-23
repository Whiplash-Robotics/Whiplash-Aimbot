import matplotlib.pyplot as plt
import numpy as np
import json
from adjustText import adjust_text

with open('benchmarks.json', 'r') as f:
    data = json.load(f)

# Formula: (mAP * accuracy_weight) / (speed * speed_weight)
accuracy_weight = 0.3
speed_weight = 0.7

for model in data:
    for variant in data[model]:
        speed = data[model][variant]["speed"]
        mAP = data[model][variant]["mAP"]
        data[model][variant]["score"] = (mAP * accuracy_weight) / (speed * speed_weight)

model_names = []
speeds = []
mAPs = []
scores = []
sizes = []

for model, variants in data.items():
    for variant, metrics in variants.items():
        model_names.append(f"{model}-{variant}")
        speeds.append(metrics["speed"])
        mAPs.append(metrics["mAP"])
        scores.append(metrics["score"])
        sizes.append(metrics["score"] ** 3)

plt.figure(figsize=(10, 6))

scatter = plt.scatter(speeds, mAPs, s=sizes, alpha=0.7, c=scores, cmap='viridis')

cbar = plt.colorbar(scatter)
cbar.set_label('Efficiency Score (higher is better)')

texts = []
for i, txt in enumerate(model_names):
    texts.append(plt.text(speeds[i], mAPs[i], txt, fontsize=12))

adjust_text(texts, arrowprops=dict(arrowstyle='->', color='red', lw=0.5))

plt.xlabel("Latency (ms)")
plt.ylabel("mAP (%)")
plt.title("YOLO Model Performance: Latency vs. mAP")
plt.grid(True, linestyle='--', alpha=0.7)

def pareto_frontier(xs, ys):
    """Find the pareto frontier (points that are not dominated by any other point)"""
    sorted_points = sorted([[xs[i], ys[i]] for i in range(len(xs))], key=lambda x: x[0])
    pareto_points = [sorted_points[0]]
    
    for point in sorted_points[1:]:
        if point[1] > pareto_points[-1][1]:
            pareto_points.append(point)
    
    return [point[0] for point in pareto_points], [point[1] for point in pareto_points]

x_pareto, y_pareto = pareto_frontier(speeds, mAPs)
plt.plot(x_pareto, y_pareto, '--', color='gray', alpha=0.7, label='Efficiency Frontier')

top_indices = np.argsort(scores)[-5:]
top_models = [model_names[i] for i in top_indices[::-1]]
top_scores = [scores[i] for i in top_indices[::-1]]

table_data = []
for i in range(5):
    table_data.append([top_models[i], f"{top_scores[i]:.2f}"])

table = plt.table(cellText=table_data, 
                  colLabels=['Model', 'Score'],
                  loc='lower right',
                  bbox=[0.7, 0.02, 0.25, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.2)

plt.tight_layout()
plt.show()