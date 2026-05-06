import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('figures', exist_ok=True)

# --- Figure 1: Dataset Composition (grouped horizontal bar) ---
constructed_labels = ['Standard Q&A', 'Darija (dialect)', 'Complex scenarios']
constructed_counts = [1543, 77, 20]
added_labels = ['Service routing', 'Real multi-turn', 'Out-of-scope refusals']
added_counts = [60, 44, 38]

fig, ax = plt.subplots(figsize=(10, 5))

y_constructed = np.arange(len(constructed_labels))
y_added = np.arange(len(added_labels)) + len(constructed_labels) + 0.5

bars_c = ax.barh(y_constructed, constructed_counts, color='#4C72B0', label='Constructed')
bars_a = ax.barh(y_added, added_counts, color='#55A868', label='Added')

ax.bar_label(bars_c, padding=4, fontsize=9)
ax.bar_label(bars_a, padding=4, fontsize=9)

all_labels = constructed_labels + [''] + added_labels
all_y = list(y_constructed) + [len(constructed_labels)] + list(y_added)
ax.set_yticks(list(y_constructed) + list(y_added))
ax.set_yticklabels(constructed_labels + added_labels)

ax.set_xlabel('Number of examples')
ax.set_title('Training Dataset Composition (Total: 1,762 examples)')
ax.legend(loc='lower right')
ax.set_xlim(0, 1750)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('figures/dataset_composition.png', dpi=150)
plt.close()

# --- Figure 2: Question Category Distribution ---
categories = ['Direct Q&A', 'Multi-article synthesis', 'Principle and exception',
              'In-domain refusal', 'Procedural', 'Clarification', 'Complex scenario']
counts = [348, 214, 190, 158, 128, 121, 20]

colors_gradient = ['#1f4e79', '#2e6da4', '#3a87c8', '#5ba3d9', '#82beea', '#aad4f5', '#d0e9fb']

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(categories, counts, color=colors_gradient)
ax.bar_label(bars, padding=4, fontsize=9)
ax.set_xlabel('Number of examples')
ax.set_title('Question Category Distribution — Constructed Dataset (1,563 examples)')
ax.set_xlim(0, 420)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('figures/question_categories_chart.png', dpi=150)
plt.close()

# --- Figure 3: Language Distribution (donut chart) ---
labels = ['French', 'Arabic (MSA)', 'Darija', 'Cross-lingual', 'Mixed / unclassified']
sizes = [771, 771, 77, 57, 86]
colors = ['#4C72B0', '#55A868', '#DD8452', '#8172B3', '#BBBBBB']

fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=None,
    colors=colors,
    autopct=lambda p: f'{p:.1f}%\n({int(round(p * sum(sizes) / 100))})',
    startangle=140,
    wedgeprops=dict(width=0.5),
    pctdistance=0.75
)
for at in autotexts:
    at.set_fontsize(8.5)

ax.legend(wedges, labels, loc='lower center', bbox_to_anchor=(0.5, -0.12),
          ncol=3, fontsize=9)
ax.set_title('Language Distribution — Full Training Dataset (1,762 examples)', pad=16)
plt.tight_layout()
plt.savefig('figures/language_distribution_chart.png', dpi=150)
plt.close()

print("All three figures saved to figures/")
