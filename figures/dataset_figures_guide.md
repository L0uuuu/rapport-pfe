# Dataset Figures Guide — Fine-Tuning Section

Three figures are needed for Section 2.7 (Training Data Synthesis) in chapter3.tex.
All should be exported as PNG at 150+ DPI and saved in `figures/`.

---

## Figure 1: Dataset Composition by Type
**File:** `figures/dataset_composition.png`
**Label:** `fig:dataset-composition`
**Placed:** after Table "Dataset Composition by Source and Type" (Section 2.7.2)

### What to show
A horizontal stacked bar chart OR a grouped bar chart showing the full 1,762-example dataset broken down by type.

### Data
| Type | Count |
|---|---|
| Standard Q&A batches | 1,543 |
| Complex scenarios | 20 |
| Darija (dialect) | 77 |
| Real multi-turn conversations | 44 |
| Service routing | 60 |
| Out-of-scope refusals | 38 |

### Recommended design
- **Chart type:** Horizontal grouped bar, two groups (Constructed / Added), bars per type within each group
- Or: two-tier donut chart — outer ring = Constructed vs Added, inner ring = breakdown by type
- **Colors:** use two distinct palettes for Constructed (blues) and Added (greens/oranges)
- **Axis:** count on x-axis (0 to 1,600), types on y-axis
- **Annotations:** show count values at end of each bar
- **Title:** "Training Dataset Composition (Total: 1,762 examples)"

---

## Figure 2: Question Category Distribution
**File:** `figures/question_categories_chart.png`
**Label:** `fig:question-categories`
**Placed:** after Table "Question Categories in the Constructed Dataset" (Section 2.7.4)

### What to show
A horizontal bar chart of the 7 question categories in the constructed dataset, sorted by count descending.

### Data
| Category | Count |
|---|---|
| Direct Q&A | 348 |
| Multi-article synthesis | 214 |
| Principle and exception | 190 |
| In-domain refusal | 158 |
| Procedural | 128 |
| Clarification | 121 |
| Complex scenario | 20 |

### Recommended design
- **Chart type:** Horizontal bar chart, sorted descending
- **Colors:** single color palette (e.g., gradient from dark blue to light blue), or color each bar differently for visual distinction
- **Axis:** count on x-axis (0 to 400), category names on y-axis
- **Annotations:** show count at end of each bar
- **Title:** "Question Category Distribution — Constructed Dataset (1,563 examples)"
- Keep category labels short: use the names as in the table above

---

## Figure 3: Language Distribution
**File:** `figures/language_distribution_chart.png`
**Label:** `fig:language-distribution`
**Placed:** after the language distribution paragraph (Section 2.7.4)

### What to show
A pie chart or donut chart showing the language breakdown across the full dataset (1,762 examples).

### Data (approximate, since routing/out-of-scope have mixed language)
| Language | Count | Notes |
|---|---|---|
| French | ~771 | 10 per standard batch + French share of added data |
| Arabic (MSA) | ~771 | 10 per standard batch + Arabic share of added data |
| Darija (dialect) | 77 | Informal Tunisian Arabic |
| Cross-lingual | ~57 | 2 per standard batch (question and article in different languages) |
| Mixed / unclassified | ~86 | Real conversations + routing examples |

### Recommended design
- **Chart type:** Donut chart with legend
- **Colors:** French = blue, Arabic MSA = green, Darija = orange, Cross-lingual = purple, Mixed = grey
- **Labels:** show percentage AND count for each segment
- **Title:** "Language Distribution — Full Training Dataset (1,762 examples)"

---

## How to Generate These Figures (Python/matplotlib)

```python
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

```

---

## Notes
- All three figures use `[H]` placement in LaTeX and `width=0.85\textwidth` (Figure 1) or `width=0.72\textwidth` (Figures 2 and 3).
- Once the PNG files are saved to `figures/`, the LaTeX references are already in place and will compile immediately.
- The language counts for Figure 3 are approximate — adjust once exact per-language counts are extracted from the JSON files.
