# 🚀 AAT/FET Data Processing System v5.1

**Smart Merge + Extensible Keywords! Works with ANY data files!**

Complete Python system for processing and plotting Keysight B2912A measurement data for anti-ambipolar transistors (AAT) and field-effect transistors (FET).

**Author:** Dr. Chandrasekar Sivakumar
**Email:** chandru.sekar6789@gmail.com
**Lab:** NIMS Semiconductor Functional Device Group
**Date:** February 8, 2026
**Version:** 5.1 (Smart Merge & Extensible Keywords)
**License:** MIT License (see [LICENSE.txt](LICENSE.txt))

> 📢 **Free & Open Source** - Use freely in your research!
> If you find this useful, please acknowledge the author in your publications.
> See [License & Acknowledgements](#license--acknowledgements) for details.

---

## 🆕 What's NEW in v5.1

### **Smart Fallback System** ⭐⭐⭐
- **No more "No plots generated" errors!**
- If keywords not found → Automatically merges all files into single plot
- `--label "Custom_Name"` - Name your plots
- `--type AAT|FET` - Specify measurement type (affects Y-axis units)
- `--interactive` - Prompted mode when you need guidance

### **Force Merge Mode** ⭐
- `--force-merge` - Override keyword grouping
- Plot ALL files together even if keywords exist
- Perfect for device comparisons across materials

### **Extensible Keywords** ⭐
- **Easy to add new materials!** Edit `KEYWORD_CATEGORIES` at top of script
- Currently supports: ReS2, WSe2, MoS2, MoSe2, Graphene, hBN
- Currently supports: inner, outer, middle, top, bottom electrodes
- Add your custom keywords in seconds!

### **V5.0 Features Still Included:**
- Full command-line control (no script editing)
- Preset configurations (explore/presentation/journal)
- Automatic Device ID extraction from settings files

### **Professional Workflow**
```bash
# Quick exploration
python plot_aat_bulletproof.py measurement.txt

# Journal submission (one command!)
python plot_aat_bulletproof.py data.txt --preset journal

# Full customization without editing
python plot_aat_bulletproof.py data.txt --format svg --y-range -8 0 --device DV-25-07
```

---

## ⚡ Quick Start

### 1. Basic Usage (Auto-detect everything!)
```bash
python plot_aat_bulletproof.py measurement.txt
```
**Automatically:**
- ✅ Detects Device ID from settings file
- ✅ Detects sweep type
- ✅ Extracts all metadata
- ✅ Creates PNG plots (300 DPI)

### 2. Journal Submission (SVG, 600 DPI, Okabe-Ito colors)
```bash
python plot_aat_bulletproof.py measurement.txt --preset journal
```

### 3. Custom Parameters (No script editing!)
```bash
python plot_aat_bulletproof.py measurement.txt --format svg --y-range -8 0 --dpi 600
```

### 4. Complete Control
```bash
python plot_aat_bulletproof.py data/ --format pdf --dpi 600 --device DV-25-07 \
    --x-range -10 2 --y-range -8 0 --palette bright --grid-major 0.3
```

---

## 📋 Command-Line Options

### Essential Options

| Option | Description | Example |
|--------|-------------|---------|
| `input` | File or directory to process | `measurement.txt` or `.` |
| `--format` | Output format: png/svg/pdf/eps | `--format svg` |
| `--dpi` | Resolution (default: 300) | `--dpi 600` |
| `--device` | Device ID (auto-detected) | `--device DV-26-01` |
| `--preset` | Use preset: explore/presentation/journal | `--preset journal` |

### Merge Control (NEW in v5.1!) ⭐

| Option | Description | Example |
|--------|-------------|---------|
| `--force-merge` | Force all files into single plot | `--force-merge` |
| `--label` | Custom label for merged plot | `--label "Outer_AAT"` |
| `--type` | Measurement type: AAT/FET/auto | `--type AAT` |
| `--interactive` | Prompted mode for label/type | `--interactive` |

**When to use:**
- Files without keywords (ReS2, WSe2, inner, outer) → Automatically uses merge
- Want single comparison plot → Use `--force-merge`
- Custom naming needed → Use `--label`

### Axis Control

| Option | Description | Example |
|--------|-------------|---------|
| `--x-range` | X-axis (Vg) range | `--x-range -10 2` |
| `--y-range` | Y-axis (Id) range | `--y-range -8 0` |
| `--n-major-ticks` | Number of major ticks | `--n-major-ticks 10` |
| `--n-minor-ticks` | Minor tick subdivisions | `--n-minor-ticks 2` |

### Appearance

| Option | Description | Example |
|--------|-------------|---------|
| `--palette` | Color palette: okabe/muted/bright/vibrant/ibm | `--palette bright` |
| `--grid-major` | Major grid transparency (0-1) | `--grid-major 0.3` |
| `--grid-minor` | Minor grid transparency (0-1) | `--grid-minor 0.15` |

### Plot Customization (NEW!) ⭐

| Option | Description | Example |
|--------|-------------|---------|
| `--annotate` | Add text annotation(s) to plot | `--annotate "-5,400,Peak,red,10"` |
| `--legend-labels` | Custom legend labels (replaces Vd values) | `--legend-labels "WSe2" "ReS2" "MoS2"` |

**Annotation Format:** `"x,y,text"` or `"x,y,text,color,fontsize"`
- Can use `--annotate` multiple times for multiple annotations
- Default color: black, default fontsize: 10

**Legend Labels:**
- Provide one label per sweep/curve in the plot
- Useful for material comparisons instead of showing Vd values

### Advanced

| Option | Description | Example |
|--------|-------------|---------|
| `--output` | Output directory | `--output ~/plots` |
| `--interactive` | Interactive filename confirmation | `--interactive` |
| `--version` | Show version information | `--version` |

---

## 🎨 Preset Configurations

### 1. **explore** (Default)
Quick exploratory analysis with sensible defaults
```bash
python plot_aat_bulletproof.py data.txt --preset explore
```
- **Format:** PNG (300 DPI)
- **Palette:** Paul Tol's Muted (grayscale-friendly)
- **Axis:** Auto-range
- **Use for:** Initial data exploration, lab notebooks

### 2. **presentation**
High-quality plots for group meetings and conferences
```bash
python plot_aat_bulletproof.py data.txt --preset presentation
```
- **Format:** PNG (300 DPI)
- **Palette:** Paul Tol's Vibrant (high contrast)
- **Grid:** More prominent (0.3/0.15)
- **Use for:** PowerPoint, Keynote, conference posters

### 3. **journal**
Publication-ready plots for journal submission
```bash
python plot_aat_bulletproof.py data.txt --preset journal
```
- **Format:** SVG (600 DPI, vector graphics)
- **Palette:** Okabe-Ito (Nature Methods standard)
- **Axis:** Optimized tick marks
- **Use for:** Nature, Science, ACS journals

---

## 💡 Real-World Examples

### Example 1: Quick Check After Measurement
```bash
# Just finished measurement, want to see the data
python plot_aat_bulletproof.py Id-Vg__WSe2_FET___2026_02_07_14_30_00_.txt
```
**Output:** WSe2_FET_Id-Vg_1sweep_Vd1.0V_Vg-4to0V_DV-25-06_2026-02-07.png

**Device ID automatically extracted from settings file!**

### Example 2: Journal Submission (Nature Materials)
```bash
# Need SVG with Okabe-Ito colors
python plot_aat_bulletproof.py measurement.txt --preset journal

# Or customize further:
python plot_aat_bulletproof.py measurement.txt --preset journal --y-range -10 10
```
**Output:** Vector SVG, 600 DPI, Nature-compliant colors

### Example 3: Group Meeting Presentation
```bash
# Need vibrant colors for slides
python plot_aat_bulletproof.py data_directory/ --preset presentation
```
**Output:** High-contrast PNG plots for all files

### Example 4: Files Without Keywords (NEW in v5.1!)
```bash
# Your files don't have ReS2/WSe2/inner/outer keywords?
# No problem! Auto-fallback to merged plot
python 1Plot_MergedAAT_FET_v5.py 'Transfer Plots/' --label "Outer_AAT" --type AAT --x-range -8 0
```
**Output:** All files merged into single plot with custom label
**No more "No plots generated" error!** ✅

### Example 5: Force Merge for Comparison
```bash
# Have multiple materials but want single comparison plot
python 1Plot_MergedAAT_FET_v5.py data/ --force-merge --label "All_Materials" --format svg
```
**Output:** Single plot with all measurements, ignoring keyword grouping

### Example 6: Interactive Mode (Guided)
```bash
# Not sure what label/type to use? Let it ask you!
python 1Plot_MergedAAT_FET_v5.py data/ --interactive
# → Prompt: "Enter plot label: " [you type: Outer_Electrode]
# → Prompt: "Measurement type (1=AAT/2=FET/3=Auto): " [you type: 1]
```
**Perfect for quick analysis when you want guidance!**

### Example 7: Device Comparison Study
```bash
# Fixed axis ranges for fair comparison
python plot_aat_bulletproof.py device_A.txt --format svg --x-range -10 2 --y-range -5 5
python plot_aat_bulletproof.py device_B.txt --format svg --x-range -10 2 --y-range -5 5
python plot_aat_bulletproof.py device_C.txt --format svg --x-range -10 2 --y-range -5 5
```
**All plots have identical axis ranges for comparison!**

### Example 8: Material Comparison with Custom Legends & Annotations (NEW!) ⭐
```bash
# Plot multiple materials with custom legend labels and voltage annotations
python 1Plot_MergedAAT_FET_v5.py data/ \
    --force-merge \
    --label "Material_Comparison" \
    --legend-labels "WSe2" "ReS2" "MoS2" \
    --annotate "-5,400,Vd=1V,red,10" \
    --annotate "2,200,Vd=0.5V,blue,10" \
    --annotate "0,300,Peak,black,12" \
    --format svg \
    --y-range -8 0
```
**Output:** Single SVG plot with:
- ✅ Legend showing material names (WSe2, ReS2, MoS2) instead of "Vd = 1.0V"
- ✅ Three text annotations showing voltage conditions and peak location
- ✅ Custom colors and font sizes for each annotation
**Perfect for publication-ready comparison figures!** 📊✨

### Example 9: Custom Device ID Override
```bash
# Settings file missing or wrong, override manually
python plot_aat_bulletproof.py measurement.txt --device DV-26-01
```

---

## 📊 Output Formats

| Format | Use Case | Advantages |
|--------|----------|------------|
| **PNG** | Default, quick viewing | Universal, good quality, moderate size |
| **SVG** | Journal submission | Vector, editable, scalable, text searchable |
| **PDF** | LaTeX documents | Vector, consistent rendering, widely supported |
| **EPS** | Traditional publishers | Legacy format, still required by some journals |

### Format Examples
```bash
# PNG (default)
python plot_aat_bulletproof.py data.txt

# SVG (recommended for journals)
python plot_aat_bulletproof.py data.txt --format svg

# PDF (for LaTeX)
python plot_aat_bulletproof.py data.txt --format pdf

# EPS (legacy publishers)
python plot_aat_bulletproof.py data.txt --format eps
```

---

## 🎯 Color Palettes

All palettes are scientifically validated for color-blind accessibility!

### **okabe** - Nature Methods Standard (8 colors)
Best for: Nature, Science journals
```bash
python plot_aat_bulletproof.py data.txt --palette okabe
```

### **muted** - Paul Tol's Muted (10 colors) ⭐ DEFAULT
Best for: General publications, grayscale printing
```bash
python plot_aat_bulletproof.py data.txt --palette muted
```

### **bright** - Paul Tol's Bright (7 colors)
Best for: Clear distinction, fewer curves
```bash
python plot_aat_bulletproof.py data.txt --palette bright
```

### **vibrant** - Paul Tol's Vibrant (7 colors)
Best for: Presentations, high contrast
```bash
python plot_aat_bulletproof.py data.txt --palette vibrant
```

### **ibm** - IBM Carbon Accessible (14 colors)
Best for: Many curves (>10 sweeps)
```bash
python plot_aat_bulletproof.py data.txt --palette ibm
```

---

## 🔧 System Requirements

- **Python:** 3.7+
- **Required packages:**
  ```bash
  pip install numpy matplotlib
  ```

---

## 📚 Complete Documentation

| Document | Purpose |
|----------|---------|
| **README.md** (this file) | Quick start & command reference |
| **ADVANCED_USAGE_GUIDE.md** | Power user workflows & automation |
| **PLOT_CUSTOMIZATION_GUIDE.md** | Detailed customization (v10 legacy) |

---

## 🎓 Typical Workflows

### Workflow 1: Daily Measurement Routine
```bash
# Morning measurements
cd ~/data/2026_02_07/
python /path/to/Scripts_v11/plot_aat_bulletproof.py .

# Automatically processes all files, extracts Device IDs
# Output: aat_plots_output/ with all plots
```

### Workflow 2: Paper Figure Preparation
```bash
# Generate journal-ready figures
python plot_aat_bulletproof.py fig1_data.txt --preset journal
python plot_aat_bulletproof.py fig2_data.txt --preset journal --y-range -8 0
python plot_aat_bulletproof.py fig3_data.txt --preset journal --palette bright

# All figures in SVG, 600 DPI, publication-ready!
```

### Workflow 3: Batch Processing with Shell Script
```bash
#!/bin/bash
# process_all_devices.sh

for device in DV-25-06 DV-25-07 DV-25-08; do
    echo "Processing $device..."
    python plot_aat_bulletproof.py data_${device}/ \
        --format svg --device $device --y-range -10 10
done
```

---

## 🔍 Metadata Priority System

The system automatically extracts metadata in this priority order:

```
1. Command-line arguments (--device, --format, etc.)
   ↓ Highest priority
2. Settings file (-s.txt)
   ↓ Instrument-generated, 100% reliable
3. Filename parsing
   ↓ Pattern matching
4. Default values
   ↓ Fallback
```

**Example:**
```bash
python plot_aat_bulletproof.py measurement.txt --device DV-26-01
```
Uses DV-26-01 (command line) **even if** settings file says DV-25-06

---

## 🔧 Adding Custom Keywords (Extensible System)

**Want to add new materials or electrode types?** Easy! Just edit the script.

### How to Add New Keywords

1. **Open** `1Plot_MergedAAT_FET_v5.py`
2. **Find** the `KEYWORD_CATEGORIES` section (near line 76)
3. **Add your keywords:**

```python
KEYWORD_CATEGORIES = {
    'FET': {
        'ReS2': ['res2', 'ReS2', 'RES2'],
        'WSe2': ['wse2', 'WSe2', 'WSE2'],
        'MoS2': ['mos2', 'MoS2', 'MOS2'],        # Already included!
        'YourMaterial': ['keyword1', 'keyword2'],  # ← Add here!
    },
    'AAT': {
        'inner': ['inner', 'Inner', 'INNER'],
        'outer': ['outer', 'Outer', 'OUTER'],
        'middle': ['middle', 'Middle', 'MIDDLE'],  # Already included!
        'YourElectrode': ['keyword1', 'keyword2'],  # ← Add here!
    }
}
```

4. **Save** and run - your keywords now work!

### Currently Supported Keywords

**FET Materials:**
- ReS2, WSe2, MoS2, MoSe2, Graphene, hBN

**AAT Electrode Types:**
- inner, outer, middle, top, bottom

**Case-insensitive** matching supported!

### Example: Adding BP (Black Phosphorus)

```python
'FET': {
    'ReS2': ['res2', 'ReS2', 'RES2'],
    'WSe2': ['wse2', 'WSe2', 'WSE2'],
    'BP': ['bp', 'BP', 'black_phosphorus'],  # ← New material!
}
```

Now files with "BP" in filename will auto-group as Black Phosphorus FET! 🎉

---

## 🐛 Troubleshooting

### Device ID Not Detected?
**Solution:**
```bash
# Override manually
python plot_aat_bulletproof.py data.txt --device YOUR-DEVICE-ID
```

### Wrong Output Format?
**Solution:**
```bash
# Specify format explicitly
python plot_aat_bulletproof.py data.txt --format svg
```

### Need Different Axis Range?
**Solution:**
```bash
# Set ranges on command line
python plot_aat_bulletproof.py data.txt --x-range -10 2 --y-range -8 0
```

### Preset Not Working?
**Solution:**
```bash
# Check available presets
python plot_aat_bulletproof.py --help

# Valid presets: explore, presentation, journal
```

---

## 📈 Version History

| Version | Date | Key Features |
|---------|------|--------------|
| **5.0** | 2026-02-07 | ⭐ **Command-line arguments**, **Auto Device ID**, **Presets** |
| 4.0 | 2026-02-06 | Settings file parser |
| 3.0 | 2026-02-05 | Multi-sweep support |
| 2.0 | 2026-02-04 | Auto-detection features |
| 1.0 | 2026-02-03 | Initial release |

---

## 🚀 Migration from v4.0 to v5.0

### Old Way (v4.0): Editing Scripts
```python
# Had to edit plot_aat_bulletproof.py every time:
DEVICE_ID = "DV-25-07"  # Line 40
Y_AXIS_RANGE = [-8, 0]   # Line 167
# Uncomment SVG export       # Lines 242, 347
```

### New Way (v5.0): Command Line
```bash
python plot_aat_bulletproof.py data.txt --device DV-25-07 --y-range -8 0 --format svg
```

**Time saved:** ~2 minutes per plot, **no errors**, **no git conflicts**!

---

## 💪 Advanced Features

### Combining Preset with Overrides
```bash
# Start with journal preset, but change one thing
python plot_aat_bulletproof.py data.txt --preset journal --y-range -8 0
```
**Result:** SVG, 600 DPI, Okabe-Ito colors, **custom Y-range**

### Custom Output Directory
```bash
# Save to specific location
python plot_aat_bulletproof.py data.txt --output ~/paper_figures/
```

### Help System
```bash
# See all options
python plot_aat_bulletproof.py --help

# Examples included!
```

---

## 📞 Getting Help

**Questions? Issues?**

1. Check the help: `python plot_aat_bulletproof.py --help`
2. Read **ADVANCED_USAGE_GUIDE.md** for power user tips
3. Check example commands in this README
4. Contact: Dr. Chandrasekar Sivakumar (NIMS Wakayama Group)

---

## 🙏 Acknowledgments

**Research Group:**
- Prof. Wakayama (Supervisor)
- NIMS Semiconductor Functional Device Group

**Project:**
- Ternary logic-in-memory devices
- 2D material heterostructures
- Anti-ambipolar transistor development

---

## 🎯 Quick Command Reference

```bash
# Most common commands:

# 1. Basic plot
python plot_aat_bulletproof.py measurement.txt

# 2. Journal submission
python plot_aat_bulletproof.py measurement.txt --preset journal

# 3. Custom Y-axis
python plot_aat_bulletproof.py measurement.txt --y-range -8 0

# 4. SVG output
python plot_aat_bulletproof.py measurement.txt --format svg

# 5. Different device
python plot_aat_bulletproof.py measurement.txt --device DV-26-01

# 6. Process directory
python plot_aat_bulletproof.py data_folder/ --preset presentation

# 7. Full customization
python plot_aat_bulletproof.py measurement.txt --format pdf --dpi 600 \
    --x-range -10 2 --y-range -8 0 --palette bright --device DV-25-07
```

---

## 📜 License & Acknowledgements

### License

This software is released under the **MIT License** - free to use, modify, and distribute.

**Copyright (c) 2026 Dr. Chandrasekar Sivakumar**

See [LICENSE.txt](LICENSE.txt) for full license text.

### Author

**Dr. Chandrasekar Sivakumar**
- Email: chandru.sekar6789@gmail.com
- Affiliation: National Institute for Materials Science (NIMS), Japan
- Lab: Semiconductor Functional Device Group

### Acknowledgements

If you use this software in your research or publications, please acknowledge:

```
AAT/FET Data Processing System v5.1+
Developed by Dr. Chandrasekar Sivakumar
NIMS Semiconductor Functional Device Group
```

**Suggested Citation:**
```
Sivakumar, C. (2026). AAT/FET Data Processing System v5.1+.
GitHub repository: https://github.com/chandru6789/AAT-FET-Plotter
```

### Contributing

Contributions, bug reports, and feature requests are welcome!
Feel free to fork and customize for your research needs.

---

**Status:** ✅ **PRODUCTION READY**

**Last Updated:** February 8, 2026

**Ready for:**
- ✅ Daily measurements
- ✅ Group meetings
- ✅ Journal submissions
- ✅ Conference presentations
- ✅ Thesis figures

**Happy plotting without editing! 🚀📊✨**

**Made with ❤️ for the semiconductor research community**
