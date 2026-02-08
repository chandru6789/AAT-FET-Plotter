#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INDIVIDUAL FILE PLOTTER v5.0 - With Command-Line Arguments
===========================================================

Author: Dr. Chandrasekar Sivakumar
Email: chandru.sekar6789@gmail.com
Affiliation: NIMS Semiconductor Functional Device Group
License: MIT License (see LICENSE.txt)

Copyright (c) 2026 Dr. Chandrasekar Sivakumar

This software is free to use, modify, and distribute.
If you use this in your research, please acknowledge the author.

===========================================================
One plot per file with full command-line control

NEW IN V5.0:
- Full argparse support for all parameters
- Preset configurations (explore/presentation/journal)
- Automatic Device ID extraction from settings files
- No script editing required!

Version: 5.0
Date: 2026-02-07
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from pathlib import Path
from aat_data_loader_multisweep import AATDataLoader
from filename_generator_robust import generate_filename_safe
import sys
import re
import argparse

# ========== VERSION INFO ==========
__version__ = "5.0"
__author__ = "Dr. Chandrasekar Sivakumar"
__lab__ = "NIMS Semiconductor Functional Device Group"

# ========== SCRIPT LOCATION ==========
SCRIPT_DIR = Path(__file__).parent.resolve()

# ========== COLOR PALETTES ==========
COLORS_OKABE_ITO = [
    '#E69F00', '#56B4E9', '#009E73', '#F0E442',
    '#0072B2', '#D55E00', '#CC79A7', '#000000'
]

COLORS_TOL_MUTED = [
    '#CC6677', '#332288', '#DDCC77', '#117733', '#88CCEE',
    '#882255', '#44AA99', '#999933', '#AA4499', '#DDDDDD'
]

COLORS_TOL_BRIGHT = [
    '#4477AA', '#EE6677', '#228833', '#CCBB44',
    '#66CCEE', '#AA3377', '#BBBBBB'
]

COLORS_TOL_VIBRANT = [
    '#EE7733', '#0077BB', '#33BBEE', '#EE3377',
    '#CC3311', '#009988', '#BBBBBB'
]

COLORS_IBM_ACCESSIBLE = [
    '#002D9C', '#EE538B', '#B28600', '#009D9A', '#9F1853', '#198038',
    '#A56EFF', '#FA4D56', '#08BDBA', '#BAE6FF', '#D4BBFF', '#FF7EB6',
    '#D2A106', '#6929C4'
]

# Palette dictionary
PALETTE_MAP = {
    'okabe': COLORS_OKABE_ITO,
    'muted': COLORS_TOL_MUTED,
    'bright': COLORS_TOL_BRIGHT,
    'vibrant': COLORS_TOL_VIBRANT,
    'ibm': COLORS_IBM_ACCESSIBLE
}

# ========== PRESET CONFIGURATIONS ==========
PRESETS = {
    'explore': {
        'description': 'Quick exploratory analysis',
        'format': 'png',
        'dpi': 300,
        'palette': 'muted',
        'x_range': None,
        'y_range': None,
        'grid_major': 0.2,
        'grid_minor': 0.1,
        'n_major_ticks': 8,
        'n_minor_ticks': 2
    },
    'presentation': {
        'description': 'High-quality plots for presentations',
        'format': 'png',
        'dpi': 300,
        'palette': 'vibrant',
        'x_range': None,
        'y_range': None,
        'grid_major': 0.3,
        'grid_minor': 0.15,
        'n_major_ticks': 6,
        'n_minor_ticks': 1
    },
    'journal': {
        'description': 'Publication-ready plots',
        'format': 'svg',
        'dpi': 600,
        'palette': 'okabe',
        'x_range': None,
        'y_range': None,
        'grid_major': 0.2,
        'grid_minor': 0.1,
        'n_major_ticks': 8,
        'n_minor_ticks': 2
    }
}

# ========== ARGUMENT PARSER ==========
def create_parser():
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        description='Plot individual measurement files with full customization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (plots each file separately)
  python 2Plot_singleAAT_FET_v5.py measurement.txt

  # Journal submission (SVG, Okabe-Ito colors)
  python 2Plot_singleAAT_FET_v5.py data.txt --preset journal

  # Custom format and axis ranges
  python 2Plot_singleAAT_FET_v5.py data.txt --format svg --y-range -8 0

  # Full customization
  python 2Plot_singleAAT_FET_v5.py data/ --format pdf --dpi 600 --device DV-26-01 \\
      --x-range -10 2 --y-range -8 0 --palette bright

Presets available: explore, presentation, journal
        """
    )

    # Positional argument
    parser.add_argument('input', type=str,
                       help='Data file or directory to process')

    # Output format
    parser.add_argument('--format', '-f', choices=['png', 'svg', 'pdf', 'eps'],
                       default=None,
                       help='Output format (default: png)')

    parser.add_argument('--dpi', type=int, default=None,
                       help='Resolution in DPI (default: 300)')

    # Device ID
    parser.add_argument('--device', '-d', type=str, default=None,
                       help='Device ID (default: auto-detect from settings file, fallback to DV-26-XX)')

    # Axis ranges
    parser.add_argument('--x-range', nargs=2, type=float, metavar=('MIN', 'MAX'),
                       default=None,
                       help='X-axis (Vg) range in volts')

    parser.add_argument('--y-range', nargs=2, type=float, metavar=('MIN', 'MAX'),
                       default=None,
                       help='Y-axis (Id) range')

    # Color palette
    parser.add_argument('--palette', '-p', choices=['okabe', 'muted', 'bright', 'vibrant', 'ibm'],
                       default=None,
                       help='Color palette (default: muted)')

    # Grid customization
    parser.add_argument('--grid-major', type=float, default=None,
                       help='Major grid transparency (0-1, default: 0.2)')

    parser.add_argument('--grid-minor', type=float, default=None,
                       help='Minor grid transparency (0-1, default: 0.1)')

    # Tick customization
    parser.add_argument('--n-major-ticks', type=int, default=None,
                       help='Number of major ticks (default: 8)')

    parser.add_argument('--n-minor-ticks', type=int, default=None,
                       help='Number of minor tick subdivisions (default: 2)')

    # Output directory
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output directory (default: input_dir/individual_plots_output)')

    # Preset
    parser.add_argument('--preset', choices=['explore', 'presentation', 'journal'],
                       default=None,
                       help='Use preset configuration')

    # Version
    parser.add_argument('--version', action='version',
                       version=f'Individual File Plotter v{__version__}')

    return parser

def apply_preset(args, preset_name):
    """Apply preset configuration, allowing command-line overrides"""
    preset = PRESETS[preset_name].copy()

    # Apply preset values only if not specified on command line
    if args.format is None:
        args.format = preset['format']
    if args.dpi is None:
        args.dpi = preset['dpi']
    if args.palette is None:
        args.palette = preset['palette']
    if args.x_range is None:
        args.x_range = preset['x_range']
    if args.y_range is None:
        args.y_range = preset['y_range']
    if args.grid_major is None:
        args.grid_major = preset['grid_major']
    if args.grid_minor is None:
        args.grid_minor = preset['grid_minor']
    if args.n_major_ticks is None:
        args.n_major_ticks = preset['n_major_ticks']
    if args.n_minor_ticks is None:
        args.n_minor_ticks = preset['n_minor_ticks']

    return args

def apply_defaults(args):
    """Apply default values for any unspecified parameters"""
    if args.format is None:
        args.format = 'png'
    if args.dpi is None:
        args.dpi = 300
    if args.palette is None:
        args.palette = 'muted'
    if args.grid_major is None:
        args.grid_major = 0.2
    if args.grid_minor is None:
        args.grid_minor = 0.1
    if args.n_major_ticks is None:
        args.n_major_ticks = 8
    if args.n_minor_ticks is None:
        args.n_minor_ticks = 2

    return args

# ========== PLOT STYLING SETUP ==========
def setup_plot_style(args):
    """Configure matplotlib with user settings"""
    plt.rcParams.update({
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'axes.grid': False,
        'axes.linewidth': 1.5,
        'axes.labelweight': 'bold',
        'axes.labelsize': 14,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'font.weight': 'bold',
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.fontsize': 11,
        'savefig.dpi': args.dpi,
        'savefig.bbox': 'tight',
    })

def get_extension(format_name):
    """Convert format name to file extension"""
    return f".{format_name}"

def extract_timestamp(filepath):
    """Extract time portion from measurement filename for disambiguation.
    e.g., 'Id-Vg [ ; 2026_02_05 10_15_57].txt' → '101557'
    """
    match = re.search(r'(\d{2})_(\d{2})_(\d{2})\]', filepath.name)
    if match:
        return f"{match.group(1)}{match.group(2)}{match.group(3)}"
    return None

def deduplicate_filename(filename, used_filenames, filepath):
    """Ensure unique output filename by appending timestamp or counter."""
    if filename not in used_filenames:
        used_filenames[filename] = 1
        return filename

    # Try appending source file timestamp first
    stem = Path(filename).stem
    ext = Path(filename).suffix
    timestamp = extract_timestamp(filepath)

    if timestamp:
        new_name = f"{stem}_t{timestamp}{ext}"
        if new_name not in used_filenames:
            used_filenames[new_name] = 1
            # Also retroactively rename the first file that used this name
            return new_name

    # Fallback: append counter
    used_filenames[filename] += 1
    counter = used_filenames[filename]
    new_name = f"{stem}_{counter}{ext}"
    while new_name in used_filenames:
        counter += 1
        new_name = f"{stem}_{counter}{ext}"
    used_filenames[new_name] = 1
    return new_name

def plot_single_file(measurements, filepath, device_id, output_dir, args, used_filenames):
    """Plot a single file's data"""
    if not measurements:
        print(f"  ⚠️  No data to plot")
        return None

    try:
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))

        # Get color palette
        colors = PALETTE_MAP[args.palette]

        print(f"\n📊 Plotting: {filepath.name}")
        print(f"   Sweeps: {len(measurements)}")

        # Determine subtype from filename or metadata
        filename_lower = filepath.stem.lower()

        if 'res2' in filename_lower:
            subtype = 'ReS2'
            meas_type = 'FET'
        elif 'wse2' in filename_lower:
            subtype = 'WSe2'
            meas_type = 'FET'
        elif 'inner' in filename_lower:
            subtype = 'Inner'
            meas_type = 'AAT'
        elif 'outer' in filename_lower:
            subtype = 'Outer'
            meas_type = 'AAT'
        else:
            subtype = filepath.stem.split('[')[1].split(';')[0].strip() if '[' in filepath.stem else 'Unknown'
            meas_type = 'FET'  # Default

        # Plot each sweep
        for idx, meas in enumerate(measurements):
            color = colors[idx % len(colors)]
            Vd = meas['Vd']

            # Forward sweep
            Vg_fwd = meas['forward']['Vg']
            Id_fwd = meas['forward']['Id']

            label = f"Vd = {Vd:.1f} V"
            ax.plot(Vg_fwd, Id_fwd * 1e9, '-', color=color, linewidth=2.5,
                   label=label, alpha=1.0, marker='o', markersize=3, markevery=5)

            # Backward sweep (if exists)
            if meas['backward']:
                Vg_bwd = meas['backward']['Vg']
                Id_bwd = meas['backward']['Id']
                ax.plot(Vg_bwd, Id_bwd * 1e9, '--', color=color, linewidth=2,
                       alpha=0.4, marker='s', markersize=3, markevery=5)

        # Styling with subscripts
        ax.set_xlabel('$V_g$ (V)', fontsize=14, fontweight='bold')
        ax.set_ylabel('$I_d$ (nA)', fontsize=14, fontweight='bold')
        ax.set_title(f'{subtype} - {filepath.stem}', fontsize=13, fontweight='bold', pad=15)

        # Fine-tune tick marks
        ax.xaxis.set_major_locator(MaxNLocator(nbins=args.n_major_ticks, prune=None))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=args.n_major_ticks, prune=None))
        ax.xaxis.set_minor_locator(AutoMinorLocator(args.n_minor_ticks))
        ax.yaxis.set_minor_locator(AutoMinorLocator(args.n_minor_ticks))

        # Set axis ranges (if specified)
        if args.x_range is not None:
            ax.set_xlim(args.x_range)
        if args.y_range is not None:
            ax.set_ylim(args.y_range)

        ax.legend(loc='best', frameon=False, fontsize=11)
        # No grid lines (clean background)
        ax.grid(False)

        # Bold tick labels
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight('bold')

        plt.tight_layout()

        # Generate filename
        extension = get_extension(args.format)
        filename = generate_filename_safe(
            measurements,
            measurement_type=meas_type,
            subtype=subtype,
            device_id=device_id,
            extension=extension,
            interactive=False,
            verbose=False
        )

        if filename is None:
            # Fallback to original filename
            filename = filepath.stem + extension

        # Check for duplicate filenames and disambiguate
        original_filename = filename
        filename = deduplicate_filename(filename, used_filenames, filepath)

        # If this is the first duplicate detected, retroactively rename the earlier file
        if filename != original_filename and used_filenames.get(original_filename) == 1:
            first_path = output_dir / original_filename
            if first_path.exists():
                first_timestamp = None
                # Find which source file produced the first output
                for src, out in used_filenames.get('_source_map', {}).items():
                    if out == original_filename:
                        first_timestamp = extract_timestamp(Path(src))
                        break
                if first_timestamp:
                    stem = Path(original_filename).stem
                    ext_part = Path(original_filename).suffix
                    renamed = f"{stem}_t{first_timestamp}{ext_part}"
                    renamed_path = output_dir / renamed
                    first_path.rename(renamed_path)
                    used_filenames[renamed] = 1
                    print(f"   ℹ️  Renamed earlier file: {original_filename} → {renamed}")

        # Track source file → output filename mapping
        if '_source_map' not in used_filenames:
            used_filenames['_source_map'] = {}
        used_filenames['_source_map'][str(filepath)] = filename

        save_path = output_dir / filename

        # Save
        plt.savefig(save_path, dpi=args.dpi, bbox_inches='tight', facecolor='white')
        print(f"   ✓ Saved: {filename}")

        plt.close(fig)
        return save_path

    except Exception as e:
        print(f"   ❌ Error plotting {filepath.name}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main execution"""
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Apply preset if specified
    if args.preset:
        print(f"\n🎨 Applying preset: {args.preset}")
        print(f"   {PRESETS[args.preset]['description']}")
        args = apply_preset(args, args.preset)

    # Apply defaults
    args = apply_defaults(args)

    # Setup plotting style
    setup_plot_style(args)

    # Print banner
    print("\n" + "="*70)
    print(f"INDIVIDUAL FILE PLOTTER v{__version__}")
    print("="*70)
    print("One plot per data file (no grouping)")

    # Get input path
    data_path = Path(args.input)

    # Validate input path exists
    if not data_path.exists():
        print(f"\n❌ Path not found: {data_path}")
        return

    # Set output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        if data_path.is_file():
            output_dir = data_path.parent / "individual_plots_output"
        else:
            output_dir = data_path / "individual_plots_output"

    print(f"\n📂 Input: {data_path}")
    print(f"💾 Output: {output_dir}")
    print(f"🎨 Format: {args.format.upper()} ({args.dpi} DPI)")
    print(f"🎨 Palette: {args.palette}")
    if args.x_range:
        print(f"📏 X-axis range: {args.x_range[0]} to {args.x_range[1]} V")
    if args.y_range:
        print(f"📏 Y-axis range: {args.y_range[0]} to {args.y_range[1]}")
    if args.device:
        print(f"🔬 Device ID (override): {args.device}")
    else:
        print(f"🔬 Device ID: Auto-detect from settings file")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory ready")

    # Load data
    print("\n" + "="*70)
    print("PROCESSING FILES")
    print("="*70)

    loader = AATDataLoader()

    # Get list of files
    if data_path.is_file():
        files = [data_path]
    elif data_path.is_dir():
        files = sorted([f for f in data_path.glob("*.txt")
                       if not f.stem.endswith('-s') and
                       'diagnostic' not in f.stem.lower()])
    else:
        print("❌ Invalid path")
        return

    print(f"\nFound {len(files)} data file(s)\n")

    # Process each file individually
    successful = 0
    failed = 0
    used_filenames = {}  # Track output filenames to prevent overwrites

    for filepath in files:
        try:
            # Load this file only
            measurements = loader.load_measurement(filepath)

            if not measurements:
                print(f"⚠️  {filepath.name}: No data loaded")
                failed += 1
                continue

            # Get device ID - Priority: command line > settings file > default
            if args.device:
                device_id = args.device
            elif measurements[0]['metadata'].get('device_id'):
                device_id = measurements[0]['metadata']['device_id']
            else:
                device_id = "DV-26-XX"  # Default fallback (DV=Device, 26=2026, XX=ID number)

            # Plot this file
            result = plot_single_file(measurements, filepath, device_id, output_dir, args, used_filenames)

            if result:
                successful += 1
            else:
                failed += 1

        except Exception as e:
            print(f"❌ Error processing {filepath.name}: {e}")
            failed += 1

    # Summary
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print(f"\n✅ Successfully plotted: {successful} file(s)")
    if failed > 0:
        print(f"❌ Failed: {failed} file(s)")
    print(f"\n📁 Output directory: {output_dir}")
    print("="*70)

if __name__ == "__main__":
    main()
