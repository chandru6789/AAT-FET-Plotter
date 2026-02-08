# 🔑 Keyword Configuration Guide - v5.1

**Easily add custom materials and electrode types!**

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [How Keyword Matching Works](#how-it-works)
3. [Adding New Keywords](#adding-keywords)
4. [Examples](#examples)
5. [Fallback Behavior](#fallback)
6. [Best Practices](#best-practices)

---

## Overview

The keyword system allows the plotter to automatically categorize and group your measurements based on filename patterns. This is perfect for:

- **FET measurements** with different materials (ReS2, WSe2, MoS2, etc.)
- **AAT measurements** with different electrode types (inner, outer, middle, etc.)

**NEW in v5.1:** If no keywords match, the system automatically **falls back to merged plotting** - no more "No plots generated" errors!

---

## How It Works

### 1. **Keyword Matching**

The plotter scans filenames for keywords and groups measurements:

```
Id-Vg__WSe2_FET___2026_02_07.txt  →  Groups as "WSe2 FET"
Id-Vg__inner_electrode__2026.txt  →  Groups as "inner AAT"
Id-Vg__data__2026_02_07.txt       →  No keywords → Fallback merge
```

### 2. **Priority System**

1. **Keyword-based grouping** (if keywords found)
2. **`--force-merge`** (override grouping)
3. **Fallback merge** (if no keywords found)
4. **`--label` and `--type`** (manual control)

---

## Adding New Keywords

### Step-by-Step

**1. Open the script:**
```bash
nano 1Plot_MergedAAT_FET_v5.py
# or use your favorite editor
```

**2. Find the `KEYWORD_CATEGORIES` section:**
Located near **line 76**:

```python
# ========== KEYWORD CONFIGURATION (Extensible!) ==========
KEYWORD_CATEGORIES = {
    'FET': {
        'ReS2': ['res2', 'ReS2', 'RES2'],
        'WSe2': ['wse2', 'WSe2', 'WSE2'],
        'MoS2': ['mos2', 'MoS2', 'MOS2'],
        # Add more here...
    },
    'AAT': {
        'inner': ['inner', 'Inner', 'INNER', 'inner_electrode'],
        'outer': ['outer', 'Outer', 'OUTER', 'outer_electrode'],
        # Add more here...
    }
}
```

**3. Add your keywords:**

```python
'FET': {
    'ReS2': ['res2', 'ReS2', 'RES2'],
    'WSe2': ['wse2', 'WSe2', 'WSE2'],
    'YourMaterial': ['keyword1', 'keyword2', 'KEYWORD1'],  # ← NEW!
}
```

**4. Save and run!**

That's it! The plotter now recognizes your keywords.

---

## Examples

### Example 1: Add Black Phosphorus (BP)

```python
'FET': {
    'ReS2': ['res2', 'ReS2', 'RES2'],
    'WSe2': ['wse2', 'WSe2', 'WSE2'],
    'BP': ['bp', 'BP', 'Black_Phosphorus', 'BlackP'],  # ← NEW!
}
```

**Now files with these patterns work:**
- `Id-Vg__BP_FET__2026.txt` ✅
- `Transfer_BlackP_data.txt` ✅
- `FET_black_phosphorus.txt` ✅

### Example 2: Add New Electrode Configuration

```python
'AAT': {
    'inner': ['inner', 'Inner', 'INNER'],
    'outer': ['outer', 'Outer', 'OUTER'],
    'diagonal': ['diagonal', 'Diagonal', 'diag'],  # ← NEW!
}
```

**Now files with these patterns work:**
- `Id-Vg__diagonal_electrode.txt` ✅
- `AAT_diag_measurement.txt` ✅

### Example 3: Multiple Variations

Add multiple ways to identify the same material:

```python
'FET': {
    'MoTe2': [
        'mote2', 'MoTe2', 'MOTE2',           # Standard
        'molybdenum_telluride', 'Mo-Te2',    # Descriptive
        'mt2', 'MT2'                          # Abbreviations
    ],
}
```

**Very flexible pattern matching!**

### Example 4: Add Your Custom Device Types

```python
'AAT': {
    'inner': ['inner', 'Inner'],
    'outer': ['outer', 'Outer'],
    'device_A': ['devA', 'device_A', 'A'],    # ← Custom!
    'device_B': ['devB', 'device_B', 'B'],    # ← Custom!
    'control': ['control', 'ctrl', 'ref'],     # ← Custom!
}
```

---

## Fallback Behavior

### What happens when no keywords match?

**v5.1 introduces smart fallback:**

```bash
# Your files: data1.txt, data2.txt, data3.txt (no keywords)

# Option 1: Auto-merge with default label
python 1Plot_MergedAAT_FET_v5.py data/
# → Creates: "Merged_Plot" with all files

# Option 2: Custom label
python 1Plot_MergedAAT_FET_v5.py data/ --label "Test_Batch_A"
# → Creates: "Test_Batch_A" plot

# Option 3: Interactive
python 1Plot_MergedAAT_FET_v5.py data/ --interactive
# → Prompts: "Enter plot label: " [you type: My_Experiment]
# → Prompts: "Measurement type (1=AAT/2=FET/3=Auto): " [you choose]
```

**No more "No plots generated" error!** 🎉

---

## Best Practices

### ✅ Do's

1. **Use descriptive category names:**
   - ✅ `'ReS2'` - Clear and specific
   - ❌ `'mat1'` - Confusing

2. **Include multiple variations:**
   ```python
   'WSe2': ['wse2', 'WSe2', 'WSE2', 'tungsten_diselenide']
   ```

3. **Keep it organized:**
   - Group by material family
   - Add comments for clarity

4. **Test your keywords:**
   ```bash
   python 1Plot_MergedAAT_FET_v5.py test_file_with_new_keyword.txt
   ```

### ❌ Don'ts

1. **Don't use overlapping keywords:**
   ```python
   # BAD:
   'MoS2': ['mos2', 'mo'],
   'MoSe2': ['mose2', 'mo'],  # "mo" conflicts!
   ```

2. **Don't use common words:**
   ```python
   # BAD:
   'Material': ['data', 'test', 'id']  # Too generic!
   ```

3. **Don't forget case variations:**
   ```python
   # GOOD:
   'Graphene': ['graphene', 'Graphene', 'GRAPHENE', 'gr', 'GR']

   # Less ideal (misses uppercase):
   'Graphene': ['graphene', 'gr']
   ```

---

## Currently Supported Keywords

### FET Materials (Out of the box)

- **ReS2**: Rhenium disulfide
- **WSe2**: Tungsten diselenide
- **MoS2**: Molybdenum disulfide
- **MoSe2**: Molybdenum diselenide
- **Graphene**: Carbon monolayer
- **hBN**: Hexagonal boron nitride

### AAT Electrode Types (Out of the box)

- **inner**: Inner electrode pair
- **outer**: Outer electrode pair
- **middle**: Middle electrode configuration
- **top**: Top electrode
- **bottom**: Bottom electrode

---

## Advanced: Override with Command Line

**Don't want to edit the script?**

Use the force-merge and label options:

```bash
# Force everything together, ignore keywords
python 1Plot_MergedAAT_FET_v5.py data/ --force-merge --label "CustomName"

# Specify type manually
python 1Plot_MergedAAT_FET_v5.py data/ --label "Test" --type AAT
```

---

## Quick Reference Card

| Scenario | Command |
|----------|---------|
| **Files with keywords** | Auto-groups by material/type |
| **Files without keywords** | Auto-merge with default label |
| **Custom label needed** | `--label "Your_Name"` |
| **Force single plot** | `--force-merge` |
| **Need guidance** | `--interactive` |
| **Add new keyword** | Edit `KEYWORD_CATEGORIES` |

---

## Troubleshooting

### Q: My files aren't being grouped correctly

**A:** Check that your filenames contain the keywords:
```bash
# Check what's in your filenames:
ls data/*.txt

# If no keywords match, add them to KEYWORD_CATEGORIES
# OR use --label to manually specify
```

### Q: Can I have multiple materials in one plot?

**A:** Yes! Use `--force-merge`:
```bash
python 1Plot_MergedAAT_FET_v5.py data/ --force-merge --label "All_Materials"
```

### Q: How do I see what keywords are recognized?

**A:** Open the script and look at `KEYWORD_CATEGORIES` section (line ~76)

### Q: Can I use regex patterns?

**A:** Currently no - uses simple substring matching. But you can add multiple variations!

---

## Summary

✅ **Easy to extend** - Just edit one section
✅ **Smart fallback** - No more empty outputs
✅ **Flexible control** - Keywords OR manual labels
✅ **Case-insensitive** - Works with any capitalization
✅ **No limits** - Add as many keywords as you need

**Happy plotting with custom keywords!** 🎉🔑

---

**Last Updated:** February 8, 2026
**Version:** 5.1
