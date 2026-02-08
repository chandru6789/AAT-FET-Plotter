# 🎨 Plot Customization Guide

**Complete guide to customizing your AAT/FET plots**

Version: 1.1 (Added command-line annotations & custom legends)
Date: 2026-02-08
Author: Dr. Chandrasekar Sivakumar

---

## 📑 Table of Contents

1. [Quick Start](#quick-start)
2. [Color Palettes](#color-palettes)
3. [Axis Labels & Formatting](#axis-labels--formatting)
4. [Axis Ranges](#axis-ranges)
5. [Tick Marks](#tick-marks)
6. [Grid Customization](#grid-customization)
7. [Legend & Annotations](#legend--annotations)
8. [Plot Size & DPI](#plot-size--dpi)
9. [Output Formats](#output-formats)
10. [Advanced Customizations](#advanced-customizations)

---

## Quick Start

All customization options are located at the **top of the plotting scripts** in clearly marked sections:

### Files to Edit:
- **`plot_aat_bulletproof.py`** - For grouped AAT/FET plots
- **`plot_individual_files.py`** - For individual file plots

### Configuration Sections:
```python
# ========== PLOT STYLING ==========          # Line ~52
# ========== COLOR PALETTES ==========        # Line ~78
# ========== AXIS RANGE ==========            # Line ~158
# ========== TICK MARKS ==========            # Line ~165
# ========== GRID ==========                  # Line ~172
```

---

## Color Palettes

### Available Palettes

All palettes are **scientifically validated** for color-blind accessibility!

#### 1. **Okabe-Ito Palette** (8 colors)
Nature Methods standard - Your original palette
```python
COLORS = COLORS_OKABE_ITO
```
**Colors:** Orange, Sky Blue, Bluish Green, Yellow, Blue, Vermillion, Reddish Purple, Black

#### 2. **Paul Tol's Muted Palette** (10 colors) ⭐ **DEFAULT**
Best for publications, overlapping lines, grayscale printing
```python
COLORS = COLORS_TOL_MUTED  # Currently active
```
**Colors:** Rose, Indigo, Sand, Green, Cyan, Wine, Teal, Olive, Purple, Grey

#### 3. **Paul Tol's Bright Palette** (7 colors)
Vibrant and clear
```python
COLORS = COLORS_TOL_BRIGHT
```
**Colors:** Blue, Red, Green, Yellow, Cyan, Purple, Grey

#### 4. **Paul Tol's Vibrant Palette** (7 colors)
High contrast
```python
COLORS = COLORS_TOL_VIBRANT
```
**Colors:** Orange, Blue, Cyan, Magenta, Red, Teal, Grey

#### 5. **IBM Carbon Accessible** (14 colors)
Maximum variety for many curves
```python
COLORS = COLORS_IBM_ACCESSIBLE
```

### Custom Colors

To create your own palette:
```python
COLORS_CUSTOM = [
    '#FF0000',  # Red
    '#00FF00',  # Green
    '#0000FF',  # Blue
    # Add more colors as needed
]
COLORS = COLORS_CUSTOM
```

**Pro Tip:** Test your custom colors at [colorbrewer2.org](https://colorbrewer2.org) for color-blind safety!

---

## Axis Labels & Formatting

### Subscript Notation

Current implementation uses LaTeX notation for professional subscripts:

```python
ax.set_xlabel('$V_g$ (V)')  # Displays as V subscript g
ax.set_ylabel('$I_d$ (nA)') # Displays as I subscript d
```

### Customization Options

#### Change Label Text:
```python
# In the plotting functions (around line 197 for AAT, line 121 for individual):
ax.set_xlabel('$V_{gate}$ (V)')           # More descriptive
ax.set_ylabel('$I_{drain}$ (μA)')         # Different unit

# Without subscripts:
ax.set_xlabel('Gate Voltage (V)')
ax.set_ylabel('Drain Current (nA)')
```

#### Font Properties:
```python
# Already in plt.rcParams (line ~52):
'axes.labelsize': 14,        # Label font size
'axes.labelweight': 'bold',  # Label weight
'font.weight': 'bold',       # Overall font weight
```

To change:
```python
ax.set_xlabel('$V_g$ (V)', fontsize=16, fontweight='normal')
```

---

## Axis Ranges

### Configuration Location
Lines ~158-164 in both scripts:

```python
# ========== AXIS RANGE CUSTOMIZATION ==========
X_AXIS_RANGE = None  # Auto range
Y_AXIS_RANGE = None  # Auto range
```

### Fixed Range Examples

#### For Transfer Characteristics (Id-Vg):
```python
# Typical AAT measurement
X_AXIS_RANGE = [-8, 0]      # Vg from -8V to 0V
Y_AXIS_RANGE = [-100, 500]  # Id from -100nA to 500nA

# Typical FET measurement
X_AXIS_RANGE = [-10, 2]     # Vg from -10V to 2V
Y_AXIS_RANGE = [0, 100]     # Id from 0μA to 100μA
```

#### Symmetric Ranges:
```python
X_AXIS_RANGE = [-10, 10]    # Symmetric around 0
Y_AXIS_RANGE = [-500, 500]  # Symmetric for ambipolar behavior
```

#### Zoom In on Region:
```python
X_AXIS_RANGE = [-5, -2]     # Focus on specific Vg range
Y_AXIS_RANGE = [0, 50]      # Focus on low current region
```

### Auto Range with Padding

Keep `None` for automatic, but add padding:
```python
X_AXIS_RANGE = None
Y_AXIS_RANGE = None

# Then in the plotting function, add:
ax.margins(x=0.05, y=0.05)  # 5% padding on each side
```

---

## Tick Marks

### Configuration Location
Lines ~165-171 in both scripts:

```python
# ========== TICK MARK CUSTOMIZATION ==========
N_MAJOR_TICKS_X = 8  # Number of major ticks on x-axis
N_MAJOR_TICKS_Y = 8  # Number of major ticks on y-axis
N_MINOR_TICKS_X = 2  # Subdivisions between major ticks
N_MINOR_TICKS_Y = 2  # Subdivisions between major ticks
```

### Examples

#### More Ticks (Detailed):
```python
N_MAJOR_TICKS_X = 12  # More tick marks
N_MAJOR_TICKS_Y = 10
N_MINOR_TICKS_X = 5   # 4 minor ticks between majors
N_MINOR_TICKS_Y = 5
```

#### Fewer Ticks (Clean):
```python
N_MAJOR_TICKS_X = 5   # Fewer, cleaner
N_MAJOR_TICKS_Y = 5
N_MINOR_TICKS_X = 2   # Just 1 minor tick between majors
N_MINOR_TICKS_Y = 2
```

#### No Minor Ticks:
```python
N_MINOR_TICKS_X = 1   # No subdivisions
N_MINOR_TICKS_Y = 1
```

### Tick Label Formatting

Current setup (in plotting functions):
```python
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight('bold')
```

Change tick label size:
```python
ax.tick_params(axis='both', which='major', labelsize=12)
ax.tick_params(axis='both', which='minor', labelsize=10)
```

### Tick Length & Width

Add to plotting functions:
```python
ax.tick_params(axis='both', which='major',
               length=6, width=1.5, direction='in')  # Inward ticks
ax.tick_params(axis='both', which='minor',
               length=3, width=1, direction='in')
```

---

## Grid Customization

### Configuration Location
Lines ~172-177 in both scripts:

```python
# ========== GRID CUSTOMIZATION ==========
GRID_MAJOR_ALPHA = 0.2      # Transparency (0=invisible, 1=solid)
GRID_MINOR_ALPHA = 0.1
GRID_MAJOR_WIDTH = 1.0      # Line width
GRID_MINOR_WIDTH = 0.5
GRID_STYLE = ':'            # Line style
```

### Grid Styles

```python
GRID_STYLE = ':'   # Dotted (default, subtle)
GRID_STYLE = '--'  # Dashed (more visible)
GRID_STYLE = '-'   # Solid (most visible)
```

### Grid Visibility Examples

#### Bold Grid:
```python
GRID_MAJOR_ALPHA = 0.5      # More visible
GRID_MINOR_ALPHA = 0.2
GRID_MAJOR_WIDTH = 1.5      # Thicker lines
GRID_STYLE = '--'           # Dashed
```

#### Subtle Grid:
```python
GRID_MAJOR_ALPHA = 0.1      # Very faint
GRID_MINOR_ALPHA = 0.05
GRID_MAJOR_WIDTH = 0.5      # Thin lines
GRID_STYLE = ':'            # Dotted
```

#### No Grid:
```python
# In plotting function, comment out:
# ax.grid(True, ...)
```

---

## Legend & Annotations

### 🆕 Command-Line Customization (v5.1+) ⭐ RECOMMENDED

**No script editing needed!** Control legends and annotations from command line.

#### Custom Legend Labels (`--legend-labels`)

Replace automatic "Vd = 1.0 V" labels with custom text (material names, device IDs, etc.)

**Basic usage:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ \
    --legend-labels "Label1" "Label2" "Label3"
```

**Material comparison:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ \
    --force-merge \
    --label "Material_Study" \
    --legend-labels "WSe2" "ReS2" "MoS2"
```

**Device comparison:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ \
    --legend-labels "Device_A" "Device_B" "Device_C" \
    --format svg
```

**Important:** Provide one label per sweep in your data. Order matters!

#### Text Annotations (`--annotate`)

Add text labels to mark features, show voltage values, or add notes.

**Format:**
```bash
--annotate "x,y,text"                    # Simple (black, size 10)
--annotate "x,y,text,color,fontsize"     # Full control
```

**Single annotation:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ \
    --label "Test" \
    --annotate "-5,400,Peak"
```

**Multiple annotations:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ \
    --annotate "-5,400,Vd=1V,red,10" \
    --annotate "2,200,Vd=0.5V,blue,10" \
    --annotate "0,300,Peak,black,12"
```

**Combined: Custom legends + annotations:**
```bash
python 1Plot_MergedAAT_FET_v5.py material_study/ \
    --force-merge \
    --label "Material_Comparison" \
    --legend-labels "WSe2" "ReS2" "MoS2" \
    --annotate "-5,400,Vd=1.0V,red,11" \
    --annotate "0,300,Peak Region,black,12" \
    --format svg \
    --preset journal
```

**Result:**
- Legend: Material names (WSe2, ReS2, MoS2) instead of voltage values
- Annotations: Voltage conditions and feature labels
- Perfect for publication figures! 📊

#### Available Colors

Common colors: `black`, `red`, `blue`, `green`, `orange`, `purple`, `brown`, `pink`, `gray`, `cyan`, `magenta`

#### Use Cases

**When to use `--legend-labels`:**
- ✅ Material comparisons (show material names)
- ✅ Device comparisons (show device IDs)
- ✅ Electrode types (inner, outer, middle)
- ✅ Sample batches (Batch A, Batch B, Batch C)

**When to use `--annotate`:**
- ✅ Mark peaks, valleys, thresholds
- ✅ Show voltage conditions (Vd = 1V)
- ✅ Label important features
- ✅ Add notes or specifications

**Pro tip:** Use annotations for voltage values when legend shows material names!

### Script-Based Legend Customization (Advanced)

For advanced legend customization not available via command line, edit the plotting functions.

**Legend position:**
```python
ax.legend(loc='upper left')   # Fixed position
ax.legend(loc='best')         # Auto-position (default)
```

**Legend styling:**
```python
ax.legend(
    loc='best',
    frameon=True,           # Show frame
    framealpha=0.9,         # Frame transparency
    fontsize=11,            # Text size
    ncol=2,                 # Two columns
    fancybox=True,          # Rounded corners
    shadow=True,            # Drop shadow
    title='Sweep Voltages'  # Legend title
)
```

**No legend:**
```python
# Comment out the legend line
# ax.legend(...)
```

### Script-Based Annotations (Advanced)

For precise control or complex annotations, edit the plotting functions directly.

**Location:** Add after all `ax.plot()` calls, before `plt.tight_layout()`

**Basic annotation:**
```python
ax.text(x_position, y_position, 'Text here',
        fontsize=12, fontweight='bold',
        ha='center', va='center')
```

**Example with color:**
```python
ax.text(-5, 400, 'Peak', fontsize=10, color='red',
        fontweight='bold', ha='center')
```

**Arrow annotation:**
```python
ax.annotate('Peak Current',
            xy=(-5, 400),          # Point to label
            xytext=(-3, 350),      # Text position
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=11, color='red')
```

**Multiple annotations with loop:**
```python
features = [
    (-5, 400, 'Peak', 'red'),
    (2, 200, 'Valley', 'blue'),
    (0, 300, 'Threshold', 'green')
]

for x, y, text, color in features:
    ax.text(x, y, text, fontsize=10, color=color,
            fontweight='bold', ha='center')
```

---

## Plot Size & DPI

### Figure Size

Default:
```python
fig, ax = plt.subplots(1, 1, figsize=(8, 6))  # Width, Height in inches
```

Customization:
```python
# Larger plot
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Wide plot (for presentations)
fig, ax = plt.subplots(1, 1, figsize=(10, 5))

# Square plot
fig, ax = plt.subplots(1, 1, figsize=(8, 8))

# Publication column width (typically 3.5 inches)
fig, ax = plt.subplots(1, 1, figsize=(3.5, 3))
```

### Resolution (DPI)

Current (in plt.rcParams):
```python
'savefig.dpi': 300,  # High quality for publications
```

Options:
```python
'savefig.dpi': 150,  # Screen viewing
'savefig.dpi': 300,  # Standard print quality
'savefig.dpi': 600,  # High-end journal requirement
'savefig.dpi': 1200, # Ultra-high resolution (large file!)
```

---

## Output Formats

### Default Format
```python
plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')  # PNG
```

### Vector Formats (Recommended for Publications)

#### SVG (Editable):
```python
# Option 1: Change default in filename_generator_robust.py
extension=".svg"

# Option 2: Save multiple formats
plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')  # PNG
plt.savefig(save_path.with_suffix('.svg'), bbox_inches='tight')          # SVG
plt.savefig(save_path.with_suffix('.pdf'), bbox_inches='tight')          # PDF
```

#### Format Comparison:

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| **PNG** | General use, web | Universal, good quality | Fixed resolution |
| **SVG** | Editing, journals | Editable, scalable | Some compatibility issues |
| **PDF** | LaTeX, publications | Scalable, widely supported | Not editable |
| **EPS** | Traditional journals | Vector, publication standard | Large files |

---

## Advanced Customizations

### Line Styles & Markers

Current:
```python
# Forward sweep
ax.plot(Vg_fwd, Id_fwd * 1e9, '-', color=color, linewidth=2.5,
        label=label, alpha=1.0, marker='o', markersize=3, markevery=5)

# Backward sweep
ax.plot(Vg_bwd, Id_bwd * 1e9, '--', color=color, linewidth=2,
        alpha=0.4, marker='s', markersize=3, markevery=5)
```

Customization options:
```python
# Line styles
linestyle='-'   # Solid
linestyle='--'  # Dashed
linestyle='-.'  # Dash-dot
linestyle=':'   # Dotted

# Line width
linewidth=1.0   # Thin
linewidth=2.5   # Default
linewidth=4.0   # Thick

# Markers
marker='o'      # Circle
marker='s'      # Square
marker='^'      # Triangle up
marker='v'      # Triangle down
marker='D'      # Diamond
marker='*'      # Star
marker='None'   # No markers

# Marker size
markersize=3    # Small
markersize=6    # Medium
markersize=10   # Large

# Show marker every N points
markevery=5     # Every 5th point
markevery=10    # Every 10th point
markevery=1     # Every point

# Transparency
alpha=1.0       # Fully opaque
alpha=0.5       # 50% transparent
alpha=0.2       # Very transparent
```

### Font Families

Add to plt.rcParams:
```python
'font.family': 'sans-serif',           # Font family
'font.sans-serif': ['Arial'],          # Specific font
# 'font.sans-serif': ['Helvetica'],    # Alternative
# 'font.serif': ['Times New Roman'],   # Serif option
```

### Axis Lines & Spines

Make axes bolder or remove them:
```python
# Current setting
'axes.linewidth': 1.5,  # Axis line width

# Make axes thicker
ax.spines['left'].set_linewidth(2.0)
ax.spines['bottom'].set_linewidth(2.0)
ax.spines['top'].set_linewidth(2.0)
ax.spines['right'].set_linewidth(2.0)

# Remove top and right spines (cleaner look)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### Background Color

```python
# White background (default)
'figure.facecolor': 'white',
'axes.facecolor': 'white',

# Transparent background
'figure.facecolor': 'none',
'savefig.transparent': True,

# Light grey background
'axes.facecolor': '#f0f0f0',
```

### Error Bars / Uncertainty

Add error bars to data:
```python
ax.errorbar(Vg, Id, yerr=error_values,
            fmt='o-', capsize=3, capthick=1,
            label=label, color=color)
```

### Multiple Y-Axes

Plot two different quantities:
```python
fig, ax1 = plt.subplots()

# First y-axis (Id)
ax1.plot(Vg, Id, 'b-', label='Id')
ax1.set_xlabel('$V_g$ (V)')
ax1.set_ylabel('$I_d$ (nA)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Second y-axis (Ig)
ax2 = ax1.twinx()
ax2.plot(Vg, Ig, 'r-', label='Ig')
ax2.set_ylabel('$I_g$ (pA)', color='r')
ax2.tick_params(axis='y', labelcolor='r')
```

---

## Quick Reference Table

| Setting | Location | Default | Common Values |
|---------|----------|---------|---------------|
| **Color Palette** | Line ~150 | `COLORS_TOL_MUTED` | See [Color Palettes](#color-palettes) |
| **X-Axis Range** | Line ~160 | `None` (auto) | `[-10, 2]`, `[-8, 0]` |
| **Y-Axis Range** | Line ~163 | `None` (auto) | `[0, 500]`, `[-100, 500]` |
| **Major Ticks X** | Line ~167 | `8` | `5-12` |
| **Major Ticks Y** | Line ~168 | `8` | `5-12` |
| **Minor Ticks** | Line ~171-172 | `2` | `1-5` |
| **Grid Major α** | Line ~175 | `0.2` | `0.1-0.5` |
| **Grid Style** | Line ~179 | `':'` | `':'`, `'--'`, `'-'` |
| **DPI** | Line ~72 | `300` | `150-1200` |
| **Figure Size** | In function | `(8, 6)` | `(3.5, 3)` to `(12, 8)` |

---

## Example Configurations

### For Journal Publication (Compact)
```python
# Figure size for single column
fig, ax = plt.subplots(1, 1, figsize=(3.5, 3))

# High DPI
'savefig.dpi': 600

# Clean palette
COLORS = COLORS_TOL_MUTED

# Subtle grid
GRID_MAJOR_ALPHA = 0.15
GRID_STYLE = ':'

# PDF output
extension = ".pdf"
```

### For Presentation Slides
```python
# Large figure
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

# Vibrant colors
COLORS = COLORS_TOL_VIBRANT

# Bold grid
GRID_MAJOR_ALPHA = 0.3
GRID_STYLE = '--'

# Large fonts
'axes.labelsize': 18
'legend.fontsize': 14
```

### For Data Analysis (Many Details)
```python
# Many ticks
N_MAJOR_TICKS_X = 12
N_MINOR_TICKS_X = 5

# Visible grid
GRID_MAJOR_ALPHA = 0.3
GRID_MINOR_ALPHA = 0.15

# Show all markers
markevery = 1
```

---

## Tips & Best Practices

1. **Start with defaults** - Modify incrementally
2. **Test with your data** - Different data needs different settings
3. **Save originals** - Keep backup before major changes
4. **Consistency** - Use same settings for related plots
5. **Color-blind safe** - Always use provided palettes
6. **Vector formats** - Use SVG/PDF for scalability
7. **DPI matters** - 300+ for print, 150 for screen
8. **Grid subtlety** - Less is more for publications
9. **Font sizes** - Readable at intended display size
10. **Documentation** - Comment your customizations!

---

## Troubleshooting

### Issue: Axis labels cut off
**Solution:** Use `bbox_inches='tight'` (already in code)

### Issue: Legend overlaps data
**Solution:** Change legend position or use `bbox_to_anchor`:
```python
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
```

### Issue: Too many minor ticks
**Solution:** Reduce `N_MINOR_TICKS_X/Y` to 2 or 1

### Issue: Grid too visible
**Solution:** Lower `GRID_MAJOR_ALPHA` to 0.1 or less

### Issue: Colors don't distinguish
**Solution:** Try different palette or increase `alpha` values

---

## Quick Edit Checklist

Before generating final plots:

- [ ] Color palette selected
- [ ] Axis ranges appropriate
- [ ] Tick marks readable
- [ ] Grid not distracting
- [ ] Legend positioned well
- [ ] Labels have subscripts
- [ ] DPI suitable for purpose
- [ ] Output format chosen
- [ ] Figure size correct
- [ ] All text readable

---

**Questions?** Check main `README.md` or scripts for examples!

**Version History:**
- v1.0 (2026-02-07): Initial comprehensive guide

---

**Happy Customizing! 🎨✨**
