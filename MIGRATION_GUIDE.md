# 🚀 Migration Guide: v4.0 → v5.0

## Quick Summary

**v4.0 (Scripts_v10):** Manual script editing for every change
**v5.0 (Scripts_v11):** Command-line control, zero editing! ⭐

---

## Key Improvements in v5.0

| Feature | v4.0 | v5.0 |
|---------|------|------|
| **Device ID** | Manual editing | Auto-extracted from settings |
| **Output format** | Edit script & uncomment lines | `--format svg` |
| **Axis ranges** | Edit configuration variables | `--x-range -10 2 --y-range -8 0` |
| **Color palette** | Edit COLORS variable | `--palette bright` |
| **DPI** | Edit rcParams | `--dpi 600` |
| **Grid transparency** | Edit variables | `--grid-major 0.3` |
| **Presets** | Not available | `--preset journal` |

---

## Side-by-Side Comparison

### Example 1: Change Output Format to SVG

#### v4.0 (Old Way)
```python
# 1. Open plot_aat_bulletproof.py in editor
# 2. Find lines 242 and 347
# 3. Uncomment SVG lines:
#plt.savefig(save_path.with_suffix('.svg'), bbox_inches='tight')  # ← Uncomment

# 4. Save file
# 5. Run script
python plot_aat_bulletproof.py measurement.txt
```

#### v5.0 (New Way)
```bash
python plot_aat_bulletproof.py measurement.txt --format svg
```

**Time saved:** 2 minutes → 5 seconds ⚡

---

### Example 2: Change Device ID

#### v4.0 (Old Way)
```python
# 1. Open plot_aat_bulletproof.py
# 2. Find line 40
# 3. Edit:
DEVICE_ID = "DV-25-07"  # Change this

# 4. Save file
# 5. Run script
python plot_aat_bulletproof.py measurement.txt
```

#### v5.0 (New Way)
```bash
# Option 1: Settings file auto-extraction (automatic!)
python plot_aat_bulletproof.py measurement.txt

# Option 2: Manual override if needed
python plot_aat_bulletproof.py measurement.txt --device DV-25-07
```

**Device ID now comes from settings file automatically!** 🎉

---

### Example 3: Fixed Y-Axis Range

#### v4.0 (Old Way)
```python
# 1. Open plot_aat_bulletproof.py
# 2. Find line ~167
# 3. Edit:
Y_AXIS_RANGE = [-8, 0]  # Change from None to [-8, 0]

# 4. Save file
# 5. Run script
python plot_aat_bulletproof.py measurement.txt

# 6. Remember to change back to None for next measurement!
```

#### v5.0 (New Way)
```bash
python plot_aat_bulletproof.py measurement.txt --y-range -8 0
```

**No need to change back - it's per-command!**

---

### Example 4: Journal Submission (SVG, 600 DPI, Okabe-Ito)

#### v4.0 (Old Way)
```python
# 1. Open plot_aat_bulletproof.py
# 2. Change DPI (line ~48):
'savefig.dpi': 600,  # Change from 300

# 3. Change palette (line ~150):
COLORS = COLORS_OKABE_ITO  # Change from COLORS_TOL_MUTED

# 4. Uncomment SVG export (lines 242, 347)
#plt.savefig(save_path.with_suffix('.svg'), bbox_inches='tight')

# 5. Save file
# 6. Run script
python plot_aat_bulletproof.py measurement.txt

# 7. Remember to change everything back!
```

#### v5.0 (New Way)
```bash
python plot_aat_bulletproof.py measurement.txt --preset journal
```

**One command replaces 7 editing steps!** 🎯

---

### Example 5: Multiple Devices with Different Settings

#### v4.0 (Old Way)
```python
# Device A (DV-25-06, -8 to 0 range, PNG)
# Edit script: DEVICE_ID="DV-25-06", Y_AXIS_RANGE=[-8,0]
python plot_aat_bulletproof.py device_A.txt

# Device B (DV-25-07, -10 to 2 range, SVG)
# Edit script: DEVICE_ID="DV-25-07", Y_AXIS_RANGE=[-10,2], uncomment SVG
python plot_aat_bulletproof.py device_B.txt

# Device C (DV-25-08, auto range, PDF)
# Edit script: DEVICE_ID="DV-25-08", Y_AXIS_RANGE=None, uncomment PDF
python plot_aat_bulletproof.py device_C.txt

# 3 × (open, edit, save, run, revert) = ~15 minutes
```

#### v5.0 (New Way)
```bash
python plot_aat_bulletproof.py device_A.txt --device DV-25-06 --y-range -8 0
python plot_aat_bulletproof.py device_B.txt --device DV-25-07 --y-range -10 2 --format svg
python plot_aat_bulletproof.py device_C.txt --device DV-25-08 --format pdf

# 3 commands, ~30 seconds total
```

**30x faster!** ⚡⚡⚡

---

## Common Tasks Migration

### Task: Process directory with custom settings

#### v4.0
```python
# Edit script with settings
# Then run:
python plot_aat_bulletproof.py /data/2026_02_07/
```

#### v5.0
```bash
python plot_aat_bulletproof.py /data/2026_02_07/ --preset presentation
# Or with custom settings:
python plot_aat_bulletproof.py /data/2026_02_07/ --format svg --palette bright
```

---

### Task: Generate plots for paper figures

#### v4.0
```python
# Fig 1: Edit for SVG, Okabe-Ito, 600 DPI
# Save, run, revert
python plot_aat_bulletproof.py fig1.txt

# Fig 2: Edit for SVG, Okabe-Ito, custom range
# Save, run, revert
python plot_aat_bulletproof.py fig2.txt

# Fig 3: Edit for PDF, bright colors
# Save, run, revert
python plot_aat_bulletproof.py fig3.txt

# Total time: ~10-15 minutes
```

#### v5.0
```bash
python plot_aat_bulletproof.py fig1.txt --preset journal
python plot_aat_bulletproof.py fig2.txt --preset journal --y-range -8 0
python plot_aat_bulletproof.py fig3.txt --format pdf --palette bright

# Total time: ~1 minute
```

---

## Backward Compatibility

**Good news:** Your v4.0 data files work perfectly with v5.0!

- ✅ Settings files still auto-detected
- ✅ Filename parsing still works
- ✅ All metadata extraction unchanged
- ✅ Output file naming identical (when using defaults)

**Only difference:** How you control the plotting (command line vs editing)

---

## Should You Migrate?

### Stay on v4.0 if:
- ❌ You never change plot settings
- ❌ You only plot once per device
- ❌ You don't mind editing scripts

### Migrate to v5.0 if:
- ✅ You frequently change plot settings
- ✅ You process multiple devices
- ✅ You prepare plots for different purposes (lab/presentation/journal)
- ✅ You want automation scripts
- ✅ You work with multiple Device IDs
- ✅ You value time savings

**Recommendation:** **Migrate!** v5.0 is objectively better for 95% of use cases.

---

## Migration Checklist

### Step 1: Backup (Optional but recommended)
```bash
cp -r Scripts_v10 Scripts_v10_backup
```

### Step 2: Use v5.0 (Scripts_v11)
```bash
cd Scripts_v11
python plot_aat_bulletproof.py --help  # See all options
```

### Step 3: Test with one file
```bash
python plot_aat_bulletproof.py ~/data/test_measurement.txt
```

### Step 4: Verify output
- Check Device ID was auto-detected
- Check plot looks correct
- Check filename is as expected

### Step 5: Full adoption
Start using v5.0 for all new plots!

---

## Common Questions

### Q: Can I use both v4.0 and v5.0?
**A:** Yes! They're in separate directories and don't interfere.

### Q: Will my old commands still work?
**A:** Yes! Basic usage is identical:
```bash
# This works in both:
python plot_aat_bulletproof.py measurement.txt
```

### Q: What if I need the v4.0 behavior?
**A:** v5.0 defaults match v4.0. Use v5.0 with no arguments for same behavior.

### Q: Are the output files different?
**A:** No! Same filenames, same plot quality (when using equivalent settings).

### Q: Do I need to reinstall Python packages?
**A:** No! Same dependencies (numpy, matplotlib).

---

## Feature Comparison Table

| Feature | v4.0 | v5.0 | Winner |
|---------|------|------|--------|
| Device ID auto-extraction | ❌ Manual | ✅ Automatic | v5.0 |
| Command-line arguments | ❌ No | ✅ Full support | v5.0 |
| Preset configurations | ❌ No | ✅ 3 presets | v5.0 |
| Output format change | 🔨 Edit script | ✅ `--format` | v5.0 |
| Axis range control | 🔨 Edit script | ✅ `--x-range`, `--y-range` | v5.0 |
| Color palette switch | 🔨 Edit script | ✅ `--palette` | v5.0 |
| DPI control | 🔨 Edit script | ✅ `--dpi` | v5.0 |
| Grid customization | 🔨 Edit script | ✅ `--grid-major`, `--grid-minor` | v5.0 |
| Batch processing | ✅ Yes | ✅ Yes | Tie |
| Settings file parsing | ✅ Yes | ✅ Yes | Tie |
| Multi-sweep support | ✅ Yes | ✅ Yes | Tie |
| Plot quality | ✅ Excellent | ✅ Excellent | Tie |
| Learning curve | Easy | Easy | Tie |
| **Time to change settings** | **2-5 min** | **5 sec** | **v5.0!** |

---

## Real User Testimonials (Imagined)

> "v5.0 saved me 2 hours per week. No more editing scripts!"
> — Future You, probably

> "The preset system is genius. `--preset journal` does exactly what I need."
> — Your colleague after you show them v5.0

> "Auto Device ID detection? Finally! I was so tired of editing that."
> — Your past self reading this

---

## Getting Started with v5.0

### 1. Read the README
```bash
cd Scripts_v11
cat README.md  # Or open in editor
```

### 2. Try the examples
```bash
# Basic
python plot_aat_bulletproof.py sample_data.txt

# With preset
python plot_aat_bulletproof.py sample_data.txt --preset journal

# Custom
python plot_aat_bulletproof.py sample_data.txt --format svg --y-range -8 0
```

### 3. Explore the help
```bash
python plot_aat_bulletproof.py --help
```

### 4. Start using it!
Replace your v4.0 commands with v5.0 commands. You'll never go back!

---

## Summary

**v5.0 is v4.0 + Command-Line Superpowers**

- ✅ All v4.0 features intact
- ✅ Zero script editing needed
- ✅ Automatic Device ID extraction
- ✅ Preset configurations
- ✅ Command-line control for everything
- ✅ 30x faster workflow
- ✅ No learning curve (if you want, just use defaults!)

**Migration difficulty:** Easy (5 minutes)
**Time savings:** Huge (hours per week)
**Regret level:** Zero!

---

**Ready to upgrade? Jump to Scripts_v11 and never edit a plotting script again!** 🚀

**Last Updated:** February 7, 2026
