# ⚡ Quick Start - Scripts v5.1

**Get plotting in 30 seconds! Works with ANY files!**

---

## 🎯 Most Common Commands

### 1. Plot files (auto-detect everything)
```bash
python 1Plot_MergedAAT_FET_v5.py measurement.txt
```
**Auto-groups by keywords OR merges all if no keywords found!**

### 2. Files without keywords? No problem! ⭐ NEW!
```bash
python 1Plot_MergedAAT_FET_v5.py data/ --label "Outer_AAT" --type AAT
```
**Custom naming + automatic merge!**

### 3. Force merge everything
```bash
python 1Plot_MergedAAT_FET_v5.py data/ --force-merge --label "All_Devices"
```

### 4. Journal submission (SVG, 600 DPI, Nature colors)
```bash
python 1Plot_MergedAAT_FET_v5.py measurement.txt --preset journal
```

### 5. Custom Y-axis range
```bash
python 1Plot_MergedAAT_FET_v5.py measurement.txt --y-range -8 0
```

### 6. Interactive mode (guided)
```bash
python 1Plot_MergedAAT_FET_v5.py data/ --interactive
```
**Prompts you for label and type!**

### 7. Custom legends & annotations ⭐ NEW!
```bash
python 1Plot_MergedAAT_FET_v5.py data/ \
    --force-merge \
    --legend-labels "WSe2" "ReS2" "MoS2" \
    --annotate "-5,400,Vd=1V,red,10" \
    --annotate "0,300,Peak,black,12"
```
**Show material names in legend + add voltage/feature annotations!**

---

## 📖 See All Options

```bash
python plot_aat_bulletproof.py --help
```

---

## 🆕 What's New in v5.1?

**Smart Fallback + Extensible Keywords!**

### NEW Features:
- ✅ **Works with ANY files** - No more "No plots generated" errors!
- ✅ **`--label "Custom_Name"`** - Name your plots
- ✅ **`--type AAT|FET`** - Specify measurement type
- ✅ **`--force-merge`** - Force all files into single plot
- ✅ **`--interactive`** - Prompted mode for guidance
- ✅ **`--annotate`** - Add text annotations to plots (NEW!)
- ✅ **`--legend-labels`** - Custom legend text (NEW!)
- ✅ **Extensible keywords** - Easy to add new materials

### V5.0 Features:
**No more script editing!** Control everything from command line:

| Old Way (v4.0) | New Way (v5.0/v5.1) |
|----------------|---------------------|
| Edit `DEVICE_ID = "..."` | Auto-detected from settings! |
| Edit axis ranges in script | `--y-range -8 0` |
| Uncomment SVG lines | `--format svg` |
| Change color palette variable | `--palette bright` |
| Edit DPI setting | `--dpi 600` |
| Can't plot without keywords | **Auto-merge fallback!** ⭐ |

---

## 🎨 Presets (One-Command Configurations)

```bash
# Exploration (default: PNG, muted colors)
python plot_aat_bulletproof.py data.txt --preset explore

# Presentation (vibrant colors, good for slides)
python plot_aat_bulletproof.py data.txt --preset presentation

# Journal (SVG, 600 DPI, Okabe-Ito colors)
python plot_aat_bulletproof.py data.txt --preset journal
```

---

## 🔬 Device ID

**Automatic extraction from settings files!**

```bash
# Auto-detect (recommended)
python plot_aat_bulletproof.py measurement.txt

# Override if needed
python plot_aat_bulletproof.py measurement.txt --device DV-26-01
```

---

## 🎯 Complete Example

```bash
# Journal figure with custom Y-axis
python plot_aat_bulletproof.py fig1_data.txt \
    --preset journal \
    --y-range -8 0

# Result: SVG, 600 DPI, Okabe-Ito colors, Y-axis from -8 to 0
```

---

## 📚 Full Documentation

| File | Purpose |
|------|---------|
| **QUICK_START.md** | This file - get started in 30 sec |
| **README.md** | Complete reference |
| **MIGRATION_GUIDE.md** | Moving from v4.0 to v5.0 |
| **ADVANCED_USAGE_GUIDE.md** | Power user tips |
| **PLOT_CUSTOMIZATION_GUIDE.md** | Deep customization |

---

## ✅ You're Ready!

Start plotting with zero configuration:
```bash
python plot_aat_bulletproof.py your_measurement.txt
```

**Happy plotting! 🚀📊**
