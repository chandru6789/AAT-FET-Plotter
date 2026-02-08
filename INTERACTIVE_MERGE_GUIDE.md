# Interactive Data Merge Tool - Complete Usage Guide

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [How Input Works in VS Code](#2-how-input-works-in-vs-code)
3. [Command Reference](#3-command-reference)
4. [Workflow 1: Extract Single Sweep from Multi-Sweep File](#4-workflow-1-extract-single-sweep-from-multi-sweep-file)
5. [Workflow 2: Extract Multiple Sweeps](#5-workflow-2-extract-multiple-sweeps)
6. [Workflow 3: Merge Sweeps from Different Files](#6-workflow-3-merge-sweeps-from-different-files)
7. [Workflow 4: Compare Different Materials (FET)](#7-workflow-4-compare-different-materials-fet)
8. [Workflow 5: Compare FET vs AAT Data](#8-workflow-5-compare-fet-vs-aat-data)
9. [Workflow 6: Side-by-Side Comparison Plots](#9-workflow-6-side-by-side-comparison-plots)
10. [Cleaning Options Explained](#10-cleaning-options-explained)
11. [Plot Customization (tune)](#11-plot-customization-tune)
12. [Exporting Data & Plots](#12-exporting-data--plots)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Getting Started

### Requirements
- Python 3.7+ with `numpy` and `matplotlib`
- Jupyter Notebook (VS Code or browser-based)
- The notebook must be in the same folder as `aat_data_loader_multisweep.py`

### Running the Notebook

1. Open `Interactive_Data_Merge.ipynb`
2. **Select kernel**: Click "Select Kernel" (top right) and choose the Python
   environment that has numpy/matplotlib (e.g., `miniconda3`)
3. **Run Cell 1** (Shift+Enter): You should see `Setup complete! Run the next cell to start.`
4. **Run Cell 2** (Shift+Enter): The interactive menu starts

---

## 2. How Input Works in VS Code

**IMPORTANT**: In VS Code, the `input()` prompt does NOT appear in the cell
output. Instead, it appears as a **small text input box at the very top center
of your VS Code window**.

```
+------------------------------------------------------------------+
|  File  Edit  View  ...   [ Type your command here ]   ...        |  <-- INPUT BOX IS HERE
+------------------------------------------------------------------+
|                                                                  |
|  Cell output shows here...                                       |
|  ==================================================              |
|    INTERACTIVE DATA MERGE TOOL                                   |
|  ==================================================              |
|                                                                  |
|  Commands:                                                       |
|    load       Load a data file                                   |
|    status     Show loaded files                                  |
|    ...                                                           |
+------------------------------------------------------------------+
```

Every time you see the cell appear to be "running" (spinner next to the cell),
look at the **top of VS Code** for the input box.

**Alternative**: Run `jupyter notebook` in Terminal for a browser-based
experience where input appears inline in the cell.

---

## 3. Command Reference

| Command   | What It Does                                          |
|-----------|-------------------------------------------------------|
| `load`    | Load a data file (.txt) or directory                  |
| `status`  | Show all loaded files and their cleaning status       |
| `preview` | Plot all sweeps of a single file (before/after clean) |
| `clean`   | Select sweeps, remove retrace, trim voltage range     |
| `undo`    | Revert a file back to its raw (uncleaned) state       |
| `merge`   | Combine selected files into one dataset and plot      |
| `plot`    | Re-draw the merged plot (after tuning settings)       |
| `tune`    | Adjust title, axes, colors, annotations, legends      |
| `export`  | Save plot as image (PNG/SVG/PDF) + data file (.txt)   |
| `save`    | Save merged data as Keysight-compatible .txt file     |
| `remove`  | Remove a loaded file from the session                 |
| `help`    | Show command list                                     |
| `quit`    | Exit the interactive tool                             |

You can also type just the first few letters (e.g., `lo` for `load`,
`cl` for `clean`, `me` for `merge`).

---

## 4. Workflow 1: Extract Single Sweep from Multi-Sweep File

**Goal**: You have a file with 5 Vd sweeps (-1V, -0.5V, 0V, 0.5V, 1V) and
you want to save only the Vd = -1V sweep as a separate file.

### Step-by-step:

```
>> load
  File path: /path/to/Id-Vg [ ; 2026_02_05 10_15_57].txt
  Label: WSe2_FET

  Output:
    Loaded "WSe2_FET": 5 sweep(s)
      Sweep 0: Vd=-1.00V | Vg=[0.0 to -8.0]V | Retrace=No | Points=101
      Sweep 1: Vd=-0.50V | Vg=[0.0 to -8.0]V | Retrace=No | Points=101
      Sweep 2: Vd=0.00V  | Vg=[0.0 to -8.0]V | Retrace=No | Points=101
      Sweep 3: Vd=0.50V  | Vg=[0.0 to -8.0]V | Retrace=No | Points=101
      Sweep 4: Vd=1.00V  | Vg=[0.0 to -8.0]V | Retrace=No | Points=101

>> clean
  Select file: 1  (or type "WSe2_FET")
  Keep which sweeps? 0           <-- only sweep 0 (Vd=-1V)
  Keep retrace? y
  Trim Vg range? n
  Show comparison? y             <-- see before/after plot

>> merge
  Merge which files? all
  Custom legends? (Enter for auto)
  Plot title? WSe2 FET Vd=-1V
  Scale? nA
  Show retrace? y

>> save
  Filename: WSe2_FET_Vd-1V
  Output directory: .

  Output:
    Data saved: WSe2_FET_Vd-1V.txt
    Format: Keysight B2912A compatible (4-column tab-separated)
    Compatible with: diagnose_multisweep.py, merged plotter, single plotter
```

The saved file `WSe2_FET_Vd-1V.txt` can now be loaded by any of your plotting
scripts directly.

---

## 5. Workflow 2: Extract Multiple Sweeps

**Goal**: Keep only sweeps 0 and 4 (Vd = -1V and 1V), discard the rest.

```
>> load
  File path: /path/to/data.txt
  Label: MyData

>> clean
  Select file: 1
  Keep which sweeps? 0,4         <-- comma-separated sweep indices
  Keep retrace? n                <-- remove backward sweeps
  Trim Vg range? y
    Vg min: -6                   <-- trim to -6V to 0V range
    Vg max: 0
  Show comparison? y

>> merge
  Merge which files? all
  ...

>> save
  Filename: MyData_selected_sweeps
```

---

## 6. Workflow 3: Merge Sweeps from Different Files

**Goal**: Take Vd=-1V from File A and Vd=0.5V from File B, merge into one plot.

```
>> load
  File path: /path/to/file_A.txt
  Label: FileA

>> load
  File path: /path/to/file_B.txt
  Label: FileB

>> status
  ============================================================
  Label           Sweeps     Status          Retrace
  ------------------------------------------------------------
  FileA           5          Raw             No
  FileB           3          Raw             Yes
  ============================================================

>> clean
  Select file: 1  (FileA)
  Keep which sweeps? 0           <-- only Vd=-1V from FileA
  Keep retrace? y
  Trim Vg range? n

>> clean
  Select file: 2  (FileB)
  Keep which sweeps? 1           <-- only one sweep from FileB
  Keep retrace? n                <-- remove retrace for this one
  Trim Vg range? n

>> merge
  Merge which files? all
  Custom legends? FileA Vd=-1V, FileB Vd=0.5V
  Plot title? Merged Comparison
  Scale? nA
  Show retrace? y

>> export
  Filename: merged_comparison
  Output directory: ./output
  Image format: png
  DPI: 300
  Also save data file? y
```

---

## 7. Workflow 4: Compare Different Materials (FET)

**Goal**: Compare WSe2 FET and ReS2 FET data on the same plot.

```
>> load
  File path: /path/to/WSe2_FET_data.txt
  Label: WSe2

>> load
  File path: /path/to/ReS2_FET_data.txt
  Label: ReS2

>> clean
  Select file: 1  (WSe2)
  Keep which sweeps? 0,1,2       <-- keep first 3 sweeps
  Keep retrace? n
  Trim Vg range? n

>> clean
  Select file: 2  (ReS2)
  Keep which sweeps? 0,1,2
  Keep retrace? n
  Trim Vg range? y
    Vg min: -5
    Vg max: 5                    <-- different range for ReS2

>> merge
  Merge which files? all
  Custom legends? WSe2 -1V, WSe2 -0.5V, WSe2 0V, ReS2 -1V, ReS2 -0.5V, ReS2 0V
  Plot title? WSe2 vs ReS2 FET Comparison
  Scale? nA

>> tune
  Choice: 6                      <-- change palette
  Palette: vibrant               <-- brighter colors for contrast
  Choice: 0                      <-- re-plot

>> export
  Filename: WSe2_vs_ReS2_FET
  Format: svg
  DPI: 600
```

---

## 8. Workflow 5: Compare FET vs AAT Data

**Goal**: Plot FET and AAT measurements together for the same device.

```
>> load
  File path: /path/to/FET_inner_data.txt
  Label: FET_inner

>> load
  File path: /path/to/AAT_inner_data.txt
  Label: AAT_inner

>> clean
  Select file: 1  (FET_inner)
  Keep which sweeps? all
  Keep retrace? n
  Trim Vg range? n

>> clean
  Select file: 2  (AAT_inner)
  Keep which sweeps? all
  Keep retrace? n
  Trim Vg range? n

>> merge
  Merge which files? all
  Custom legends? FET Vd=-1V, FET Vd=-0.5V, AAT Vd=-1V, AAT Vd=-0.5V
  Plot title? FET vs AAT - Inner Electrodes

>> tune
  Choice: 4                      <-- add annotation
    X: -3
    Y: 200
    Text: FET region
    Color: blue
    Size: 12
  Choice: 4                      <-- another annotation
    X: -6
    Y: -100
    Text: AAT region
    Color: red
    Size: 12
  Choice: 0                      <-- re-plot with annotations

>> export
```

---

## 9. Workflow 6: Side-by-Side Comparison Plots

**Goal**: Create side-by-side subplots for visual comparison.

**Note**: The current interactive tool creates single merged plots. For
side-by-side subplots, use the merged plotter script directly:

### Method: Using the Merged Plotter Script

After extracting/saving individual data files using the notebook, use the
command-line scripts for side-by-side plotting:

```bash
# Step 1: Extract data using notebook (see Workflows 1-2 above)
# This creates separate .txt files for each dataset

# Step 2: Plot individual files
python 2Plot_singleAAT_FET_v5.py WSe2_sweep.txt ReS2_sweep.txt AAT_sweep.txt

# Step 3: Or merge specific files
python 1Plot_MergedAAT_FET_v5.py WSe2_sweep.txt ReS2_sweep.txt --legend-labels "WSe2" "ReS2"
```

### Method: Manual Subplot in Jupyter (Advanced)

After merging data with the notebook, you can create subplots manually in a
new cell:

```python
# Run this in a NEW cell after using the merge tool

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
colors = merger._colors()
sf = merger._scale_factor()

# Left plot: first N sweeps
for i, m in enumerate(merger.merged[:3]):  # first 3 sweeps
    c = colors[i % len(colors)]
    ax1.plot(m['forward']['Vg'], m['forward']['Id']*sf, '-', color=c,
             linewidth=2.5, label=f'Vd={m["Vd"]:.1f}V')
ax1.set_title('Material A (FET)', fontweight='bold')
ax1.set_xlabel('$V_g$ (V)'); ax1.set_ylabel(f'$I_d$ ({merger._unit()})')
ax1.legend()

# Right plot: remaining sweeps
for i, m in enumerate(merger.merged[3:]):  # remaining sweeps
    c = colors[(i+3) % len(colors)]
    ax2.plot(m['forward']['Vg'], m['forward']['Id']*sf, '-', color=c,
             linewidth=2.5, label=f'Vd={m["Vd"]:.1f}V')
ax2.set_title('Material B (AAT)', fontweight='bold')
ax2.set_xlabel('$V_g$ (V)'); ax2.set_ylabel(f'$I_d$ ({merger._unit()})')
ax2.legend()

plt.tight_layout()
plt.savefig('side_by_side.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## 10. Cleaning Options Explained

When you type `clean`, you get three options:

### Option 1: Sweep Selection

```
Keep which sweeps? (e.g. 0,2,4 or "all") [all]:
```

- Type `all` to keep everything
- Type `0` to keep only the first sweep
- Type `0,2,4` to keep sweeps 0, 2, and 4
- Type `1,3` to keep sweeps 1 and 3

**How to know which sweep is which?** Use `preview` first to see all sweeps
plotted with their indices, or check the sweep table printed after `load`.

### Option 2: Retrace (Backward Sweep)

```
Keep retrace (backward sweep)? [Y/n]:
```

- `y` (default): Keep both forward and backward sweeps (hysteresis visible)
- `n`: Remove backward sweep, keep only forward

Bidirectional sweeps go: Vg start -> Vg stop -> Vg start. Forward is the
first half, backward is the return. Remove retrace for cleaner plots.

### Option 3: Voltage Trim

```
Trim Vg range? [y/N]:
```

- `n` (default): Keep full voltage range
- `y`: Enter Vg min and max to crop the data

Example: If your sweep goes 0V to -8V but you only want -6V to 0V:
```
Vg min: -6
Vg max: 0
```

---

## 11. Plot Customization (tune)

After merging, type `tune` to access these options:

| # | Option              | Example                           |
|---|---------------------|-----------------------------------|
| 1 | Change title        | "WSe2 FET Id-Vg Characteristics"  |
| 2 | Set X axis range    | Xmin=-8, Xmax=0                   |
| 3 | Set Y axis range    | Ymin=-100, Ymax=500               |
| 4 | Add text annotation | Position, text, color, size       |
| 5 | Clear annotations   | Remove all annotations            |
| 6 | Change color palette| `muted`, `okabe`, or `vibrant`    |
| 7 | Change current scale| `nA` or `uA`                      |
| 8 | Toggle retrace      | Show/hide backward sweeps         |
| 9 | Change legend labels| Comma-separated new labels        |
| 0 | Done & re-plot      | Apply changes and redraw          |

You can make multiple changes before pressing `0` to re-plot.

### Color Palettes

- **muted** (default): Soft academic colors, good for publications
- **okabe**: Colorblind-friendly (Okabe-Ito palette)
- **vibrant**: Bright, high-contrast colors for presentations

---

## 12. Exporting Data & Plots

### Save Data Only (`save` command)

Saves the merged data in **Keysight B2912A compatible format**:
- 4 columns: V2 (Vg), I1 (Id), I2 (Ig), V1 (Vd)
- Tab-separated, raw Amperes
- Directly loadable by all your plotting scripts

```
>> save
  Filename: my_merged_data
  Output directory: .
```

Creates: `my_merged_data.txt`

### Export Plot + Data (`export` command)

Saves both the plot image and data file:

```
>> export
  Filename: my_result
  Output directory: ./results
  Image format: png              <-- png, svg, pdf, or eps
  DPI: 300                       <-- 300 for screen, 600 for print
  Also save data file? y
```

Creates:
- `./results/my_result.png` (plot image)
- `./results/my_result.txt` (Keysight-compatible data)

### Output File Compatibility

The saved `.txt` files work directly with:
- `python 1Plot_MergedAAT_FET_v5.py my_merged_data.txt`
- `python 2Plot_singleAAT_FET_v5.py my_merged_data.txt`
- `python diagnose_multisweep.py my_merged_data.txt`
- Any software that reads tab-separated data (Excel, Origin, etc.)

---

## 13. Troubleshooting

### "Cell appears stuck / nothing happens"
The `input()` box is at the **top of VS Code window**. Look up!

### "ModuleNotFoundError: No module named 'numpy'"
Select the correct Python kernel (top right of notebook). Use miniconda3 or
any environment with numpy and matplotlib installed.

### "File not found"
- Drag & drop the file into the input box (VS Code supports this)
- Or paste the full path
- Remove any surrounding quotes if double-quoted

### "No plots generated after merge"
Make sure you:
1. Loaded at least one file (`load`)
2. Merged the data (`merge`)
Then use `plot` to redraw.

### "Want to start over"
- Use `undo` to revert cleaning on a specific file
- Use `remove` to delete a loaded file
- Or restart: Kernel > Restart, then re-run both cells

### "Plots look different from the script output"
The notebook uses `%matplotlib inline` which renders at screen resolution.
Use `export` with DPI=600 for publication-quality output.

### "Slow performance"
- Large files (>10,000 points) may take a moment to plot
- Close other notebooks to free memory
- Use `%matplotlib agg` instead of `inline` for faster non-interactive rendering

---

## Quick Reference Card

```
TYPICAL WORKFLOW:
  load -> load -> clean -> clean -> merge -> tune -> export

EXTRACT SINGLE SWEEP:
  load -> clean (keep 1 sweep) -> merge -> save

COMPARE MATERIALS:
  load Material_A -> load Material_B -> clean both -> merge -> export

KEY SHORTCUTS:
  lo = load    cl = clean    me = merge    ex = export
  st = status  pr = preview  tu = tune     sa = save
  q  = quit    un = undo     re = remove   pl = plot
```
