# 🎉 What's New in v5.1 - Complete Overview

**Version 5.1 Release Notes**

Date: February 8, 2026
Author: Dr. Chandrasekar Sivakumar
Lab: NIMS Semiconductor Functional Device Group

---

## 🚀 Major Features Added

### 1. **Smart Fallback System** ⭐⭐⭐

**Problem Solved:** "No plots were generated" error when files don't have keywords!

**How it works:**
- If keywords (ReS2, WSe2, inner, outer) found → Groups by category
- If NO keywords found → **Automatically merges all files into single plot**
- No more errors, no more manual editing!

**Example:**
```bash
# Your files: Id-Vg [Vd-1V; 2026_02_05].txt (no keywords)
python 1Plot_MergedAAT_FET_v5.py 'Transfer Plots/' --label "Outer_AAT" --type AAT

# Result: ✅ All files merged into single plot with custom label!
```

---

### 2. **Force Merge Mode** ⭐

Override keyword-based grouping to create single comparison plots.

**New Argument:** `--force-merge`

**Use cases:**
- Compare multiple materials in one plot
- Create device comparison figures
- Override automatic grouping

**Example:**
```bash
# Even if files have WSe2, ReS2 keywords, force into one plot
python 1Plot_MergedAAT_FET_v5.py data/ --force-merge --label "All_Materials"
```

---

### 3. **Custom Plot Labeling** ⭐

Name your plots exactly what you want!

**New Argument:** `--label "Your_Name"`

**Example:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ --label "Outer_Electrode_Test_1"
```

---

### 4. **Measurement Type Control** ⭐

Specify whether data is AAT or FET for correct Y-axis units.

**New Argument:** `--type AAT|FET|auto`

- `AAT` → Y-axis in nA (nanoamps)
- `FET` → Y-axis in µA (microamps)
- `auto` → Auto-detect from current magnitude (default)

**Example:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ --type AAT --label "Test_Device"
```

---

### 5. **Interactive Mode** ⭐

Get prompted for label and type when you need guidance!

**Enhanced Argument:** `--interactive`

**How it works:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ --interactive

# Prompts:
# 📝 Enter plot label (e.g., 'Outer_AAT', 'Device_Test'): [you type]
# 🔬 Measurement type:
#    1) AAT (Anti-ambipolar, nA scale)
#    2) FET (Field-effect, µA scale)
#    3) Auto (detect from current magnitude)
# Select [1/2/3, default=3]: [you choose]
```

---

### 6. **Extensible Keyword System** ⭐⭐

**Easy to add new materials and electrode types!**

**Location:** Edit `KEYWORD_CATEGORIES` section (line ~76) in script

**Currently Supported:**

**FET Materials:**
- ReS2, WSe2, MoS2, MoSe2, Graphene, hBN

**AAT Electrode Types:**
- inner, outer, middle, top, bottom

**How to add new keywords:**
```python
KEYWORD_CATEGORIES = {
    'FET': {
        'ReS2': ['res2', 'ReS2', 'RES2'],
        'WSe2': ['wse2', 'WSe2', 'WSE2'],
        'BP': ['bp', 'BP', 'black_phosphorus'],  # ← Add this!
    },
    'AAT': {
        'inner': ['inner', 'Inner', 'INNER'],
        'outer': ['outer', 'Outer', 'OUTER'],
        'diagonal': ['diagonal', 'diag'],         # ← Add this!
    }
}
```

**See:** `KEYWORDS_GUIDE.md` for complete instructions

---

## 📊 Decision Tree: How the Plotter Works Now

```
┌─────────────────────────────────┐
│   Load measurement files        │
└───────────┬─────────────────────┘
            │
            ▼
┌─────────────────────────────────┐
│   --force-merge specified?      │
├─────────────────────────────────┤
│  YES → Plot all together        │────┐
│  NO → Continue                  │    │
└───────────┬─────────────────────┘    │
            │                          │
            ▼                          │
┌─────────────────────────────────┐    │
│  Check for keywords in files    │    │
├─────────────────────────────────┤    │
│  Keywords found?                │    │
│  YES → Group by category        │    │
│  NO → Fallback merge ───────────┼────┤
└─────────────────────────────────┘    │
                                       │
                ┌──────────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  Get label & type               │
├─────────────────────────────────┤
│  --label specified? Use it      │
│  --interactive? Prompt user     │
│  Otherwise: Use default         │
└───────────┬─────────────────────┘
            │
            ▼
┌─────────────────────────────────┐
│  Create merged plot             │
│  ✅ All files in single plot!   │
└─────────────────────────────────┘
```

---

## 💡 Real-World Usage Scenarios

### Scenario 1: Your Original Problem

**Problem:** Files without keywords → "No plots generated"

**Before v5.1:**
```bash
python 1Plot_MergedAAT_FET_v5.py 'Transfer Plots/'
# ❌ Error: No plots were generated
```

**After v5.1:**
```bash
python 1Plot_MergedAAT_FET_v5.py 'Transfer Plots/' --label "Outer_AAT" --type AAT
# ✅ Success: All files merged into "Outer_AAT" plot!
```

---

### Scenario 2: Quick Comparison Study

**Want:** Compare 3 different device batches in single plot

```bash
python 1Plot_MergedAAT_FET_v5.py batch_A_B_C/ --force-merge \
    --label "Device_Comparison" --format svg --y-range -8 0
```

**Result:** Single SVG with all measurements, custom Y-axis

---

### Scenario 3: Don't Know What to Name It?

**Solution:** Use interactive mode!

```bash
python 1Plot_MergedAAT_FET_v5.py data/ --interactive

# System prompts you:
# 📝 Enter plot label: [you decide based on data]
# 🔬 Measurement type: [system helps you choose]
```

---

### Scenario 4: Adding New Material

**Want:** Plot BP (Black Phosphorus) FET measurements

1. Edit script, add to `KEYWORD_CATEGORIES`:
   ```python
   'BP': ['bp', 'BP', 'black_phosphorus']
   ```

2. Run:
   ```bash
   python 1Plot_MergedAAT_FET_v5.py BP_data/
   ```

3. ✅ Automatically groups all BP measurements!

---

## 📋 Complete New Arguments Reference

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--force-merge` | flag | False | Force all files into single plot |
| `--label` / `-l` | string | "Merged_Plot" | Custom plot label |
| `--type` / `-t` | choice | auto | Measurement type (AAT/FET/auto) |
| `--interactive` | flag | False | Prompted mode for guidance |

---

## 📚 Documentation Updates

**New Files:**
- ✅ `KEYWORDS_GUIDE.md` - Complete guide for adding custom keywords
- ✅ `WHATS_NEW_v5.1.md` - This file!

**Updated Files:**
- ✅ `README.md` - Added v5.1 features, merge control section, extensible keywords section
- ✅ `QUICK_START.md` - Updated with v5.1 examples and commands
- ✅ `1Plot_MergedAAT_FET_v5.py` - Script header updated to v5.1

---

## 🔄 Migration from v5.0 to v5.1

### Backward Compatibility

**Good news:** 100% backward compatible!

All v5.0 commands still work:
```bash
# These still work exactly as before:
python 1Plot_MergedAAT_FET_v5.py measurement.txt
python 1Plot_MergedAAT_FET_v5.py data/ --preset journal
python 1Plot_MergedAAT_FET_v5.py data/ --format svg --y-range -8 0
```

### What Changed?

**Only additions, no breaking changes:**
- ✅ Added fallback behavior (helps when no keywords found)
- ✅ Added new optional arguments (--force-merge, --label, --type)
- ✅ Enhanced --interactive mode
- ✅ Extensible keyword system (easy to add materials)

**Nothing removed, nothing changed in existing behavior!**

---

## ⚡ Quick Command Reference

```bash
# 1. Auto-detect everything (keyword-based or fallback)
python 1Plot_MergedAAT_FET_v5.py data/

# 2. Custom merge with label
python 1Plot_MergedAAT_FET_v5.py data/ --label "Test_1" --type AAT

# 3. Force merge (ignore keywords)
python 1Plot_MergedAAT_FET_v5.py data/ --force-merge --label "All"

# 4. Interactive (get prompted)
python 1Plot_MergedAAT_FET_v5.py data/ --interactive

# 5. Journal ready + custom label
python 1Plot_MergedAAT_FET_v5.py data/ --preset journal --label "Fig1"

# 6. Full control
python 1Plot_MergedAAT_FET_v5.py data/ --format svg --dpi 600 \
    --label "Device_Test" --type AAT --y-range -8 0 --device DV-26-01
```

---

## ✅ Testing Checklist

Test your v5.1 installation:

- [ ] **Files with keywords:** Should auto-group by material/electrode
  ```bash
  python 1Plot_MergedAAT_FET_v5.py data_with_WSe2_files/
  ```

- [ ] **Files without keywords:** Should auto-merge
  ```bash
  python 1Plot_MergedAAT_FET_v5.py generic_data/ --label "Test"
  ```

- [ ] **Force merge:** Should combine all into one
  ```bash
  python 1Plot_MergedAAT_FET_v5.py data/ --force-merge
  ```

- [ ] **Interactive mode:** Should prompt for input
  ```bash
  python 1Plot_MergedAAT_FET_v5.py data/ --interactive
  ```

- [ ] **Help menu:** Should show new arguments
  ```bash
  python 1Plot_MergedAAT_FET_v5.py --help
  ```

---

## 🎓 Summary

**v5.1 makes the plotter:**
- ✅ **More robust** - No more "No plots generated" errors
- ✅ **More flexible** - Work with ANY files, not just keyword-matched
- ✅ **More customizable** - Easy to add new materials/electrodes
- ✅ **More user-friendly** - Interactive mode for guidance
- ✅ **More powerful** - Force-merge for comparison studies

**Best of all:** Still 100% backward compatible with v5.0!

---

## 📞 Need Help?

- **Quick Start:** See `QUICK_START.md`
- **Full Reference:** See `README.md`
- **Keyword System:** See `KEYWORDS_GUIDE.md`
- **Help Command:** `python 1Plot_MergedAAT_FET_v5.py --help`

---

**Enjoy your smarter, more flexible plotting system!** 🎉📊✨

**Version:** 5.1
**Date:** February 8, 2026
**Author:** Dr. Chandrasekar Sivakumar
**Lab:** NIMS Semiconductor Functional Device Group
