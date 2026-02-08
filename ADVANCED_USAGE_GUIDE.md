# 🚀 Advanced Usage Guide - AAT/FET Data Processing System

**For Researchers Who Value Efficiency, Reproducibility, and Publication Quality**

Author: Dr. Chandrasekar Sivakumar
Lab: NIMS Semiconductor Functional Device Group
Version: 5.1+
Date: February 8, 2026

*This guide reflects 10+ years of semiconductor characterization experience at NIMS*

---

## 📋 Table of Contents

1. [Philosophy: The Research Data Pipeline](#philosophy-the-research-data-pipeline)
2. [Advanced Command Combinations](#advanced-command-combinations)
3. [Batch Processing & Automation](#batch-processing--automation)
4. [Publication Workflows](#publication-workflows)
5. [Data Management Strategies](#data-management-strategies)
6. [Quality Control & Validation](#quality-control--validation)
7. [Advanced Annotation Strategies](#advanced-annotation-strategies)
8. [Shell Scripting for Automation](#shell-scripting-for-automation)
9. [Collaboration & Reproducibility](#collaboration--reproducibility)
10. [Power User Tips](#power-user-tips)
11. [Troubleshooting Complex Scenarios](#troubleshooting-complex-scenarios)

---

## 🎯 Philosophy: The Research Data Pipeline

### The Modern Researcher's Workflow

After years of device characterization, I've learned that **time spent on repetitive tasks is time stolen from research**. This system eliminates script editing and enables:

**The 3-Second Rule:** Any plot customization should take ≤3 seconds to specify

**The Reproducibility Principle:** Every plot should be regeneratable from a single command

**The Batch-First Mindset:** Design workflows assuming you'll process 100 devices, not 1

### Data Flow Architecture

```
Raw Measurement (.txt)
    ↓
Settings Extraction (automatic)
    ↓
Keyword Detection (automatic)
    ↓
Command-Line Customization (you control)
    ↓
High-Quality Plot (publication-ready)
    ↓
Metadata File (reproducibility)
```

**Key insight:** The only manual step should be the command-line arguments.

---

## 🔥 Advanced Command Combinations

### Level 1: Single-Feature Mastery

**Each feature works alone:**
```bash
python 1Plot_MergedAAT_FET_v5.py data/ --format svg
python 1Plot_MergedAAT_FET_v5.py data/ --y-range -8 0
python 1Plot_MergedAAT_FET_v5.py data/ --legend-labels "WSe2" "ReS2"
```

### Level 2: Multi-Feature Combinations

**Real power comes from combining features:**

#### Material Comparison (Legend + Annotation + Format)
```bash
python 1Plot_MergedAAT_FET_v5.py material_study/ \
    --force-merge \
    --label "Fig2_Materials" \
    --legend-labels "WSe2" "ReS2" "MoS2" "BP" \
    --annotate "-5,450,V_d = 1.0 V,red,11" \
    --annotate "0,100,V_d = 0.5 V,blue,11" \
    --format svg \
    --dpi 600 \
    --y-range -8 0 \
    --palette okabe
```

**Result:** Publication-ready comparison figure in ONE command

#### Device Optimization Series (Batch + Fixed Axes)
```bash
# Compare 5 device iterations with identical axes
for device in DV-26-{01..05}; do
    python 1Plot_MergedAAT_FET_v5.py "data/${device}/" \
        --device "${device}" \
        --x-range -10 2 \
        --y-range -5 5 \
        --format svg \
        --label "Device_${device}"
done
```

**Result:** Directly comparable plots for optimization tracking

#### Journal Submission Package (Preset + Customization)
```bash
python 1Plot_MergedAAT_FET_v5.py key_result/ \
    --preset journal \
    --legend-labels "Sample A" "Sample B" "Sample C" \
    --annotate "-4,350,Peak,red,12" \
    --label "Figure_3a" \
    --device DV-26-01
```

**Result:** Nature/Science-ready SVG with custom annotations

### Level 3: Context-Aware Automation

**Different contexts need different defaults:**

```bash
# Quick check during measurement
alias quick='python 1Plot_MergedAAT_FET_v5.py'

# Presentation mode
alias present='python 1Plot_MergedAAT_FET_v5.py --preset presentation --format png'

# Journal mode
alias journal='python 1Plot_MergedAAT_FET_v5.py --preset journal --format svg --dpi 600'

# Usage:
quick latest_data/           # Fast PNG
present meeting_data/        # Vibrant colors
journal final_results/       # Publication quality
```

---

## 🤖 Batch Processing & Automation

### Scenario 1: Daily Measurement Processing

**Problem:** You measure 10-20 devices per day and need standardized plots.

**Solution: Daily Processing Script**

Create `process_today.sh`:
```bash
#!/bin/bash
# Daily measurement processing workflow

DATE=$(date +%Y_%m_%d)
DATA_DIR="${HOME}/Measurements/${DATE}"
OUTPUT_DIR="${HOME}/Plots/${DATE}"

echo "Processing measurements from ${DATE}..."

# Process all subdirectories
for device_dir in "${DATA_DIR}"/*/; do
    device_name=$(basename "${device_dir}")

    echo "  → Processing ${device_name}..."

    python 1Plot_MergedAAT_FET_v5.py "${device_dir}" \
        --output "${OUTPUT_DIR}" \
        --format png \
        --format svg \
        --palette muted \
        --device "${device_name}"
done

echo "✓ Complete! Plots saved to ${OUTPUT_DIR}"
```

**Usage:**
```bash
chmod +x process_today.sh
./process_today.sh
```

**Time saved:** 2-3 hours/day → 5 minutes/day

### Scenario 2: Multi-Material Comparison Study

**Problem:** Compare 5 materials, 3 voltage conditions each, need all plots identical.

**Solution: Parametric Batch Script**

```bash
#!/bin/bash
# Material comparison study - identical formatting

MATERIALS=("WSe2" "ReS2" "MoS2" "BP" "Graphene")
VD_VALUES=(0.5 1.0 1.5)

# Fixed parameters for fair comparison
COMMON_ARGS="--x-range -8 0 --y-range -10 10 --format svg --dpi 600"

for material in "${MATERIALS[@]}"; do
    for vd in "${VD_VALUES[@]}"; do
        data_file="data/${material}/Vd_${vd}V.txt"

        if [ -f "${data_file}" ]; then
            python 1Plot_MergedAAT_FET_v5.py "${data_file}" \
                ${COMMON_ARGS} \
                --label "${material}_Vd${vd}V" \
                --legend-labels "${material}" \
                --annotate "0,8,V_d = ${vd} V,red,11"
        fi
    done
done
```

**Key insight:** Define `COMMON_ARGS` once, ensures consistency across 15 plots

### Scenario 3: Automated Figure Generation for Weekly Reports

**Problem:** Every Friday you need the same 10 plots for group meeting.

**Solution: Report Generator**

```bash
#!/bin/bash
# Weekly report automation

WEEK=$(date +%Y_Week%W)
REPORT_DIR="Weekly_Reports/${WEEK}"
mkdir -p "${REPORT_DIR}"

# Figure 1: All materials comparison
python 1Plot_MergedAAT_FET_v5.py data/all_materials/ \
    --force-merge \
    --label "Fig1_Materials" \
    --legend-labels "WSe2" "ReS2" "MoS2" \
    --format png \
    --output "${REPORT_DIR}"

# Figure 2: Device optimization series
python 1Plot_MergedAAT_FET_v5.py data/optimization/ \
    --label "Fig2_Optimization" \
    --x-range -10 2 \
    --y-range -8 0 \
    --format png \
    --output "${REPORT_DIR}"

# Figure 3-10: Individual device performance
for i in {3..10}; do
    device="DV-26-0${i}"
    python 1Plot_MergedAAT_FET_v5.py "data/${device}/" \
        --device "${device}" \
        --label "Fig${i}_${device}" \
        --format png \
        --output "${REPORT_DIR}"
done

echo "✓ Report figures ready in ${REPORT_DIR}"
open "${REPORT_DIR}"  # Auto-open folder
```

**Usage:** Run every Friday at 4 PM (or set up cron job)

---

## 📄 Publication Workflows

### End-to-End Paper Preparation

**Scenario:** Nature Materials submission requires specific formatting

#### Phase 1: Exploratory Analysis (Week 1-2)
```bash
# Quick PNGs for lab notebook
python 1Plot_MergedAAT_FET_v5.py preliminary_data/ \
    --preset explore \
    --output lab_notebook/
```

#### Phase 2: Figure Draft (Week 3-4)
```bash
# Higher quality for manuscript draft
python 1Plot_MergedAAT_FET_v5.py selected_data/ \
    --preset presentation \
    --format svg \
    --label "Fig2_draft" \
    --output manuscript_draft/
```

#### Phase 3: Final Submission (Week 5)
```bash
# Nature Materials final figures
python 1Plot_MergedAAT_FET_v5.py final_data/figure2/ \
    --preset journal \
    --legend-labels "Sample A (n-type)" "Sample B (p-type)" "Sample C (ambipolar)" \
    --annotate "-4.5,450,V_{peak},red,12" \
    --annotate "0,200,V_g = 0,black,11" \
    --format svg \
    --dpi 600 \
    --y-range -10 10 \
    --x-range -8 0 \
    --label "Figure_2a" \
    --device "Sample_A" \
    --output submission/figures/
```

**Pro tip:** Save the final command in `figure2_generate.sh` for revisions

### Multi-Panel Figure Coordination

**Challenge:** Figure 3 has 4 panels (a-d), all need identical formatting

**Solution:**
```bash
#!/bin/bash
# Figure 3: Four-panel comparison

# Common settings
COMMON="--format svg --dpi 600 --x-range -8 0 --y-range -10 10 --palette okabe"

# Panel (a): WSe2
python 1Plot_MergedAAT_FET_v5.py data/WSe2/ \
    ${COMMON} \
    --label "Fig3a_WSe2" \
    --legend-labels "T=300K" "T=77K" "T=4K" \
    --annotate "-4,8,WSe_2,black,14"

# Panel (b): ReS2
python 1Plot_MergedAAT_FET_v5.py data/ReS2/ \
    ${COMMON} \
    --label "Fig3b_ReS2" \
    --legend-labels "T=300K" "T=77K" "T=4K" \
    --annotate "-4,8,ReS_2,black,14"

# Panel (c): MoS2
python 1Plot_MergedAAT_FET_v5.py data/MoS2/ \
    ${COMMON} \
    --label "Fig3c_MoS2" \
    --legend-labels "T=300K" "T=77K" "T=4K" \
    --annotate "-4,8,MoS_2,black,14"

# Panel (d): BP
python 1Plot_MergedAAT_FET_v5.py data/BP/ \
    ${COMMON} \
    --label "Fig3d_BP" \
    --legend-labels "T=300K" "T=77K" "T=4K" \
    --annotate "-4,8,BP,black,14"
```

**Result:** Perfectly matched panels for publication

---

## 📊 Data Management Strategies

### Directory Structure That Scales

After managing 500+ devices, here's what works:

```
Research_Project/
├── Raw_Data/
│   ├── 2026_02/
│   │   ├── DV-26-01/
│   │   │   ├── Id-Vg_WSe2_Vd1V_2026_02_05.txt
│   │   │   └── Settings_2026_02_05.txt
│   │   └── DV-26-02/
│   └── 2026_03/
├── Plots/
│   ├── Exploratory/        # Quick checks
│   ├── Analysis/           # Intermediate analysis
│   └── Publication/        # Final figures
├── Scripts/
│   ├── daily_process.sh
│   ├── figure1_gen.sh
│   └── batch_analysis.sh
└── Metadata/
    └── processing_log.txt
```

### Processing Log (Reproducibility)

**Create `log_plot.sh` wrapper:**
```bash
#!/bin/bash
# Logging wrapper for reproducibility

LOGFILE="Metadata/processing_log.txt"

# Log the command
echo "$(date): $@" >> "${LOGFILE}"

# Execute the command
python 1Plot_MergedAAT_FET_v5.py "$@"

# Log completion
echo "$(date): Complete" >> "${LOGFILE}"
echo "---" >> "${LOGFILE}"
```

**Usage:**
```bash
./log_plot.sh data/DV-26-01/ --format svg --label "Test1"
```

**Benefit:** 6 months later, you know EXACTLY how you made that plot

### Backup Strategy

```bash
#!/bin/bash
# Smart backup: Only plots + metadata, not raw data

DATE=$(date +%Y%m%d)
BACKUP_DIR="Backups/Plots_${DATE}"

mkdir -p "${BACKUP_DIR}"

# Copy all plots
rsync -av --include='*.svg' --include='*.png' \
          --include='*.txt' --exclude='*' \
          Plots/ "${BACKUP_DIR}/"

# Copy processing scripts
cp Scripts/*.sh "${BACKUP_DIR}/"

echo "Backup complete: ${BACKUP_DIR}"
```

---

## ✅ Quality Control & Validation

### Systematic Plot Review Checklist

**Before sending to collaborators/journals:**

```bash
#!/bin/bash
# QC script: Check all plots meet standards

PLOT_DIR="Publication/"

echo "Quality Control Report"
echo "======================"

# Check 1: File format
echo "Checking SVG files..."
svg_count=$(find "${PLOT_DIR}" -name "*.svg" | wc -l)
echo "  SVG files found: ${svg_count}"

# Check 2: Resolution
echo "Checking DPI..."
for file in "${PLOT_DIR}"/*.png; do
    dpi=$(identify -format '%x' "$file" | cut -d' ' -f1)
    if [ "${dpi%%.*}" -lt 300 ]; then
        echo "  ⚠️  Low DPI: $file (${dpi})"
    fi
done

# Check 3: Consistent naming
echo "Checking naming convention..."
if ls "${PLOT_DIR}"/Fig* 2>/dev/null; then
    echo "  ✓ Figure naming consistent"
else
    echo "  ⚠️  Check figure names"
fi

# Check 4: Metadata files
echo "Checking metadata..."
txt_count=$(find "${PLOT_DIR}" -name "*.txt" | wc -l)
echo "  Metadata files: ${txt_count}"

echo "======================"
echo "QC Complete"
```

### Automated Validation

**Check plots match specifications:**
```bash
# Verify all figures use same axis ranges
grep "xlim" Plots/Publication/*.txt | sort -u

# Verify consistent device IDs
grep "Device ID" Plots/Publication/*.txt | sort
```

---

## 🎨 Advanced Annotation Strategies

### Strategy 1: Parametric Annotation

**Problem:** Need to annotate 10 plots with calculated values

```bash
#!/bin/bash
# Auto-calculate and annotate peak positions

for data_file in data/*.txt; do
    # Extract peak from metadata (example)
    peak_vg=$(grep "Peak" "${data_file}" | awk '{print $3}')
    peak_id=$(grep "Peak" "${data_file}" | awk '{print $5}')

    python 1Plot_MergedAAT_FET_v5.py "${data_file}" \
        --annotate "${peak_vg},${peak_id},Peak,red,11" \
        --label "$(basename ${data_file} .txt)"
done
```

### Strategy 2: Multi-Level Annotations

**Use case:** Show voltage AND temperature AND specification

```bash
python 1Plot_MergedAAT_FET_v5.py device_data/ \
    --legend-labels "300K" "200K" "100K" "77K" \
    --annotate "-6,450,V_d = 1.0 V,red,11" \
    --annotate "0,400,T = 300K,blue,10" \
    --annotate "-2,300,Spec: I_{peak} > 400 nA,green,9" \
    --format svg
```

**Result:** Comprehensive labeling without clutter

### Strategy 3: Color-Coded Regions

```bash
# Mark different operating regions
python 1Plot_MergedAAT_FET_v5.py aat_device/ \
    --annotate "-6,100,OFF,gray,10" \
    --annotate "-3,350,Ambipolar,purple,11" \
    --annotate "0,150,ON,green,10" \
    --legend-labels "Inner" "Outer"
```

---

## 🔧 Shell Scripting for Automation

### Template: Universal Batch Processor

```bash
#!/bin/bash
# Universal batch processing template
# Customize PROCESS_FUNCTION for your needs

PROCESS_FUNCTION() {
    local input_file="$1"
    local output_dir="$2"

    # YOUR CUSTOM PROCESSING HERE
    python 1Plot_MergedAAT_FET_v5.py "${input_file}" \
        --format svg \
        --output "${output_dir}" \
        --palette muted
}

# Main execution
INPUT_DIR="${1:-data/}"
OUTPUT_DIR="${2:-plots/}"

mkdir -p "${OUTPUT_DIR}"

# Process all .txt files
find "${INPUT_DIR}" -name "*.txt" -type f | while read file; do
    echo "Processing: $(basename ${file})"
    PROCESS_FUNCTION "${file}" "${OUTPUT_DIR}"
done

echo "Batch processing complete!"
```

**Usage:**
```bash
./batch_process.sh data/2026_02/ plots/february/
```

### Parallel Processing for Speed

**Process 100 files in parallel:**

```bash
#!/bin/bash
# Parallel processing for multi-core systems

export INPUT_DIR="$1"
export OUTPUT_DIR="$2"

process_file() {
    python 1Plot_MergedAAT_FET_v5.py "$1" \
        --format svg \
        --output "${OUTPUT_DIR}"
}

export -f process_file

# Process 8 files simultaneously
find "${INPUT_DIR}" -name "*.txt" | \
    parallel -j 8 process_file {}

echo "Parallel processing complete!"
```

**Requires:** `gnu-parallel` (`brew install parallel` on Mac)

**Speed gain:** 8x faster on 8-core machine

---

## 🤝 Collaboration & Reproducibility

### Share Exact Commands

**Instead of saying:** "I used default settings with SVG output"

**Say this:**
```bash
# Exact command for Figure 2
python 1Plot_MergedAAT_FET_v5.py \
    ~/Data/Sample_A/Transfer/ \
    --force-merge \
    --label "Figure_2a" \
    --legend-labels "WSe2" "ReS2" "MoS2" \
    --annotate "-4.5,450,V_{peak},red,12" \
    --format svg \
    --dpi 600 \
    --x-range -8 0 \
    --y-range -10 10 \
    --palette okabe \
    --device "Sample_A"
```

**Save in:** `figure_commands.sh` in your repository

### Makefile for Paper Figures

**Ultimate reproducibility:**

```makefile
# Makefile for paper figures

PYTHON=python 1Plot_MergedAAT_FET_v5.py
COMMON_SVG=--format svg --dpi 600 --palette okabe

all: fig1 fig2 fig3 fig4

fig1:
	$(PYTHON) data/overview/ \
		$(COMMON_SVG) \
		--label "Figure_1" \
		--force-merge \
		--output figures/

fig2:
	$(PYTHON) data/material_comparison/ \
		$(COMMON_SVG) \
		--label "Figure_2" \
		--legend-labels "WSe2" "ReS2" "MoS2" \
		--annotate "-4,400,Peak,red,11" \
		--output figures/

fig3:
	./scripts/generate_fig3_panels.sh

fig4:
	$(PYTHON) data/temperature_study/ \
		$(COMMON_SVG) \
		--label "Figure_4" \
		--output figures/

clean:
	rm -f figures/*.svg figures/*.txt

.PHONY: all fig1 fig2 fig3 fig4 clean
```

**Usage:**
```bash
make all          # Generate all figures
make fig2         # Regenerate just Figure 2
make clean        # Remove old figures
```

---

## 💡 Power User Tips

### 1. Environment Variables for Common Settings

```bash
# In ~/.bashrc or ~/.zshrc

export PLOT_OUTPUT="${HOME}/Research/Plots"
export PLOT_FORMAT="svg"
export PLOT_DPI="600"

# Usage
python 1Plot_MergedAAT_FET_v5.py data/ \
    --output "${PLOT_OUTPUT}" \
    --format "${PLOT_FORMAT}" \
    --dpi "${PLOT_DPI}"
```

### 2. Shell Aliases for Frequent Operations

```bash
# Quick aliases
alias plotsvg='python 1Plot_MergedAAT_FET_v5.py --format svg --dpi 600'
alias plotpng='python 1Plot_MergedAAT_FET_v5.py --format png --dpi 300'
alias plotjournal='python 1Plot_MergedAAT_FET_v5.py --preset journal'

# Usage becomes:
plotsvg data/ --label "Test1"
plotjournal final_results/
```

### 3. Tab Completion (Advanced)

Create `~/.plot_completion.sh`:
```bash
_plot_completion() {
    local cur prev opts
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="--format --dpi --label --device --preset --annotate --legend-labels"

    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
}

complete -F _plot_completion python 1Plot_MergedAAT_FET_v5.py
```

Source in `~/.bashrc`: `source ~/.plot_completion.sh`

### 4. Diff Check Before Reprocessing

```bash
# Before reprocessing, check what changed
diff <(ls -1 Plots/) <(ls -1 Plots_backup/)

# Only process changed files
comm -13 <(ls Plots/) <(ls Data/) | while read file; do
    python 1Plot_MergedAAT_FET_v5.py "Data/${file}"
done
```

### 5. Smart File Naming with Timestamps

```bash
#!/bin/bash
# Auto-versioned plots

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

python 1Plot_MergedAAT_FET_v5.py data/ \
    --label "Analysis_${TIMESTAMP}" \
    --format svg

# Result: Analysis_20260208_143022.svg
# Never accidentally overwrite!
```

### 6. Conditional Processing Based on Data Quality

```bash
#!/bin/bash
# Only plot if data meets quality threshold

for file in data/*.txt; do
    # Check number of data points
    points=$(wc -l < "${file}")

    if [ ${points} -gt 100 ]; then
        echo "✓ Processing: ${file} (${points} points)"
        python 1Plot_MergedAAT_FET_v5.py "${file}" --format svg
    else
        echo "⚠️  Skipping: ${file} (too few points: ${points})"
    fi
done
```

### 7. Git Integration for Version Control

```bash
#!/bin/bash
# Auto-commit plots with metadata

python 1Plot_MergedAAT_FET_v5.py "$@"

# Git commit with automatic message
git add Plots/
git commit -m "Generated plots: $(date +%Y-%m-%d %H:%M) - Args: $*"
git push origin main
```

### 8. Notification on Completion (Long Batch Jobs)

```bash
#!/bin/bash
# Send notification when batch processing completes

./batch_process_all.sh && \
    osascript -e 'display notification "Plotting complete!" with title "Research"'

# Or on Linux:
# notify-send "Research" "Plotting complete!"
```

---

## 🔍 Troubleshooting Complex Scenarios

### Scenario: Mixed Data Types in One Directory

**Problem:** Directory has both AAT and FET files, causing errors

**Solution:**
```bash
# Separate by keywords first
mkdir -p sorted/AAT sorted/FET

for file in data/*.txt; do
    if grep -q "inner\|outer" "${file}"; then
        cp "${file}" sorted/AAT/
    elif grep -q "WSe2\|ReS2\|MoS2" "${file}"; then
        cp "${file}" sorted/FET/
    fi
done

# Process separately
python 1Plot_MergedAAT_FET_v5.py sorted/AAT/ --type AAT
python 1Plot_MergedAAT_FET_v5.py sorted/FET/ --type FET
```

### Scenario: Very Large Datasets (>1000 files)

**Problem:** Processing 1000+ files takes hours

**Solution 1: Smart filtering**
```bash
# Only process files from last week
find data/ -name "*.txt" -mtime -7 | while read file; do
    python 1Plot_MergedAAT_FET_v5.py "${file}" --format svg
done
```

**Solution 2: Parallel processing**
```bash
# Use GNU parallel for speed
find data/ -name "*.txt" | \
    parallel -j 8 python 1Plot_MergedAAT_FET_v5.py {} --format svg
```

### Scenario: Annotation Coordinates Unknown

**Problem:** Don't know exact coordinates for annotations

**Solution: Two-pass approach**
```bash
# Pass 1: Generate plot to see axes
python 1Plot_MergedAAT_FET_v5.py data/ --label "preview"

# View plot, note coordinates visually
open Plots/preview.png

# Pass 2: Add annotations with found coordinates
python 1Plot_MergedAAT_FET_v5.py data/ \
    --label "final" \
    --annotate "-4.5,420,Peak" \
    --annotate "0,200,Reference"
```

### Scenario: Legend Labels Don't Match Number of Curves

**Problem:** Provided 3 labels but plot has 4 curves

**Solution: Check first**
```bash
# Count sweeps in data
grep "Vd" data/*.txt | wc -l

# Provide exact number of labels
python 1Plot_MergedAAT_FET_v5.py data/ \
    --legend-labels "Sweep1" "Sweep2" "Sweep3" "Sweep4"
```

---

## 🎓 Lessons from 10+ Years of Device Characterization

### 1. **Consistency > Perfection**
One mediocre script used consistently beats ten perfect scripts used inconsistently.

### 2. **Automate Early**
If you do something 3 times, automate it. Future you will thank present you.

### 3. **Document Everything**
Command history is documentation. Use `history > commands_feb2026.txt`

### 4. **Version Your Plots**
Never overwrite. Use timestamps or version numbers.

### 5. **Back Up Smartly**
Back up plots + scripts + metadata. Raw data goes on lab server.

### 6. **Collaborate Explicitly**
Share exact commands, not "I used default settings"

### 7. **Think in Batches**
Design your workflow assuming you'll have 100x more data tomorrow

### 8. **Validate Systematically**
QC checklist before every collaborator meeting/submission

### 9. **Optimize for Iteration**
Research means redoing plots 10 times. Make iteration fast.

### 10. **Keep It Simple**
Complex automation breaks. Simple automation lasts years.

---

## 🎯 Summary: Your Advanced Workflow

**Daily routine:**
```bash
# Morning: Process overnight measurements
./scripts/daily_process.sh

# Afternoon: Generate analysis plots
plotsvg interesting_results/ --label "Analysis_$(date +%Y%m%d)"

# Before meeting: Regenerate all figures
make all
```

**For publication:**
```bash
# Save exact commands
echo "$(history | tail -1)" >> figure_commands.sh

# Version control
git add figures/ figure_commands.sh
git commit -m "Final figures for submission"
```

**For collaboration:**
```bash
# Package everything
tar czf plots_and_scripts.tar.gz \
    Plots/ Scripts/ figure_commands.sh
```

---

**Remember:** The best tool is the one you'll actually use. Start simple, automate incrementally.

**Questions or suggestions?** Update this guide based on what you learn!

---

**Last Updated:** February 8, 2026
**Version:** 5.1+
**Next Review:** When v6.0 is released

*"Time spent on automation is time invested in future research"*
*— Dr. Chandrasekar Sivakumar, NIMS 2026*
