#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AAT/FET Plotting System v5.1 - Smart Merge & Extensible Keywords
=================================================================

Author: Dr. Chandrasekar Sivakumar
Email: chandru.sekar6789@gmail.com
Affiliation: NIMS Semiconductor Functional Device Group
License: MIT License (see LICENSE.txt)

Copyright (c) 2026 Dr. Chandrasekar Sivakumar

This software is free to use, modify, and distribute.
If you use this in your research, please acknowledge the author.

=================================================================
Professional plotting with full command-line control

NEW IN V5.1:
- Smart fallback: Auto-merge when no keywords found
- --force-merge: Force all files into single plot
- --label: Custom plot naming
- --type: Specify AAT/FET for proper Y-axis units
- --interactive: Prompted mode for label/type
- Extensible keyword system (easy to add new materials)

V5.0 Features:
- Full argparse support for all parameters
- Preset configurations (explore/presentation/journal)
- Automatic Device ID extraction from settings files
- No script editing required!

Author: Chandrasekar Sivakumar
Lab: NIMS Semiconductor Functional Device Group
Date: 2026-02-08
Version: 5.1 (Smart merge + extensible keywords!)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MaxNLocator
from pathlib import Path
from aat_data_loader_multisweep import AATDataLoader
from filename_generator_robust import generate_filename_safe, generate_filename_compact, generate_filename_detailed
import sys
import argparse
import json

# ========== VERSION INFO ==========
__version__ = "5.1"
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

# ========== KEYWORD CONFIGURATION (Extensible!) ==========
# Add new materials or electrode types here as needed
KEYWORD_CATEGORIES = {
    'FET': {
        'ReS2': ['res2', 'ReS2', 'RES2'],
        'WSe2': ['wse2', 'WSe2', 'WSE2'],
        'MoS2': ['mos2', 'MoS2', 'MOS2'],
        'MoSe2': ['mose2', 'MoSe2', 'MOSE2'],
        'Graphene': ['graphene', 'Graphene', 'gr', 'GR'],
        'hBN': ['hbn', 'hBN', 'HBN'],
        # Add more FET materials here as needed
    },
    'AAT': {
        'inner': ['inner', 'Inner', 'INNER', 'inner_electrode'],
        'outer': ['outer', 'Outer', 'OUTER', 'outer_electrode'],
        'middle': ['middle', 'Middle', 'MIDDLE', 'mid'],
        'top': ['top', 'Top', 'TOP'],
        'bottom': ['bottom', 'Bottom', 'BOTTOM'],
        # Add more AAT electrode types here as needed
    }
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
        description='Plot AAT/FET measurement data with full customization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (auto-detects keywords and groups)
  python 1Plot_MergedAAT_FET_v5.py measurement.txt

  # Merge all files with custom label (no keyword grouping)
  python 1Plot_MergedAAT_FET_v5.py data/ --label "Outer_AAT" --type AAT

  # Force merge even if keywords exist
  python 1Plot_MergedAAT_FET_v5.py data/ --force-merge --label "All_Devices"

  # Interactive mode (prompts for label/type)
  python 1Plot_MergedAAT_FET_v5.py data/ --interactive

  # Journal submission
  python 1Plot_MergedAAT_FET_v5.py data.txt --preset journal

  # Full customization
  python 1Plot_MergedAAT_FET_v5.py data/ --format svg --y-range -8 0 \\
      --label "Test" --type AAT --device DV-26-01

Presets available: explore, presentation, journal
        """
    )

    # Positional argument(s)
    parser.add_argument('input', type=str, nargs='+',
                       help='Data file(s) or directory to process. Pass multiple files to merge them.')

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
                       help='Output directory (default: input_dir/merged_plots_output)')

    # Preset
    parser.add_argument('--preset', choices=['explore', 'presentation', 'journal'],
                       default=None,
                       help='Use preset configuration')

    # Merge control (NEW in v5.1)
    parser.add_argument('--force-merge', action='store_true',
                       help='Force all measurements into single plot (ignore keyword grouping)')

    parser.add_argument('--label', '-l', type=str, default=None,
                       help='Custom label for merged plot (e.g., "Outer_AAT", "Device_Comparison")')

    parser.add_argument('--type', '-t', choices=['AAT', 'FET', 'auto'],
                       default='auto',
                       help='Measurement type for merged plot (affects Y-axis units)')

    # Interactive mode
    parser.add_argument('--interactive', action='store_true',
                       help='Enable interactive mode (prompts for label/type if needed)')

    # Plot customization (NEW in v5.1+)
    parser.add_argument('--annotate', action='append', default=None,
                       help='Add text annotation (format: "x,y,text" or "x,y,text,color,fontsize"). Can be used multiple times.')

    parser.add_argument('--legend-labels', nargs='+', type=str, default=None,
                       help='Custom legend labels (e.g., "WSe2" "ReS2" "MoS2"). Replaces auto-generated Vd labels.')

    # Version
    parser.add_argument('--version', action='version',
                       version=f'AAT/FET Plotting System v{__version__}')

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
        'savefig.facecolor': 'white',
        'savefig.transparent': False,
    })

# ========== HELPER FUNCTIONS ==========
def get_extension(format_name):
    """Convert format name to file extension"""
    return f".{format_name}"

def save_metadata(metadata, filepath):
    """Save measurement metadata to text file"""
    try:
        with open(filepath, 'w') as f:
            f.write("="*70 + "\n")
            f.write("MEASUREMENT METADATA\n")
            f.write("="*70 + "\n\n")

            f.write(f"Device ID: {metadata.get('device_id', 'Unknown')}\n")
            f.write(f"Measurement Type: {metadata['measurement_type']}\n")

            if metadata['measurement_type'] == 'FET':
                f.write(f"Material: {metadata['material']}\n")
            elif metadata['measurement_type'] == 'AAT':
                f.write(f"Electrode Type: {metadata['electrode_type']}\n")

            f.write(f"\nNumber of sweeps: {len(metadata['measurements'])}\n\n")

            for idx, meas in enumerate(metadata['measurements'], 1):
                f.write(f"Sweep {idx}:\n")
                f.write(f"  Vd = {meas['Vd']:.3f} V\n")
                f.write(f"  Vg range: {meas['Vg_min']:.2f} to {meas['Vg_max']:.2f} V\n")
                f.write(f"  Id range: {meas['Id_min']:.3e} to {meas['Id_max']:.3e} A\n")
                f.write(f"  Data points: {meas['num_points']}\n")

                if 'peak' in meas:
                    if meas['peak']:
                        f.write(f"  Peak current: {meas['peak']['Ipeak']:.3e} A\n")
                        f.write(f"  Peak position: {meas['peak']['Vpeak']:.2f} V\n")

            f.write("\n" + "="*70 + "\n")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not save metadata: {e}")
        return False

def parse_annotations(annotation_strings):
    """
    Parse annotation strings into list of annotation dictionaries

    Args:
        annotation_strings: List of strings in format "x,y,text" or "x,y,text,color,fontsize"

    Returns:
        List of dicts with keys: x, y, text, color, fontsize
    """
    if not annotation_strings:
        return []

    annotations = []
    for ann_str in annotation_strings:
        parts = [p.strip() for p in ann_str.split(',')]

        if len(parts) < 3:
            print(f"⚠️  Warning: Invalid annotation format '{ann_str}'. Need at least x,y,text")
            continue

        try:
            x = float(parts[0])
            y = float(parts[1])
            text = parts[2]
            color = parts[3] if len(parts) > 3 else 'black'
            fontsize = int(parts[4]) if len(parts) > 4 else 10

            annotations.append({
                'x': x,
                'y': y,
                'text': text,
                'color': color,
                'fontsize': fontsize
            })
        except (ValueError, IndexError) as e:
            print(f"⚠️  Warning: Could not parse annotation '{ann_str}': {e}")
            continue

    return annotations

def apply_annotations(ax, annotations):
    """
    Apply text annotations to a matplotlib axes

    Args:
        ax: Matplotlib axes object
        annotations: List of annotation dicts from parse_annotations()
    """
    if not annotations:
        return

    print(f"\n✏️  Adding {len(annotations)} annotation(s)...")
    for ann in annotations:
        ax.text(
            ann['x'],
            ann['y'],
            ann['text'],
            fontsize=ann['fontsize'],
            color=ann['color'],
            fontweight='bold',
            ha='center',
            va='center'
        )
        print(f"   • '{ann['text']}' at ({ann['x']}, {ann['y']})")

def plot_fet_clean(measurements, material, device_id, output_dir, args, sweep_type="Id-Vg"):
    """Plot FET characteristics"""
    if not measurements:
        print("⚠️  No FET measurements to plot")
        return None, None

    try:
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))

        # Get color palette
        colors = PALETTE_MAP[args.palette]

        metadata = {
            'device_id': device_id,
            'measurement_type': 'FET',
            'material': material,
            'measurements': []
        }

        # Plot each sweep
        for idx, meas in enumerate(measurements):
            color = colors[idx % len(colors)]
            Vd = meas['Vd']
            Vg_fwd = meas['forward']['Vg']
            Id_fwd = meas['forward']['Id']

            # Use custom legend label if provided, otherwise use default
            if args.legend_labels and idx < len(args.legend_labels):
                label = args.legend_labels[idx]
            else:
                label = f"Vd = {Vd:.1f} V"

            ax.plot(Vg_fwd, Id_fwd * 1e6, '-', color=color, linewidth=2.5,
                   label=label, alpha=1.0, marker='o', markersize=3, markevery=5)

            if meas['backward']:
                Vg_bwd = meas['backward']['Vg']
                Id_bwd = meas['backward']['Id']
                ax.plot(Vg_bwd, Id_bwd * 1e6, '--', color=color, linewidth=2,
                       alpha=0.4, marker='s', markersize=3, markevery=5)

            # Store metadata
            meas_meta = {
                'Vd': Vd,
                'Vg_min': Vg_fwd.min(),
                'Vg_max': Vg_fwd.max(),
                'Id_min': Id_fwd.min(),
                'Id_max': Id_fwd.max(),
                'num_points': len(Vg_fwd)
            }
            metadata['measurements'].append(meas_meta)

        # Axis labels
        ax.set_xlabel('$V_g$ (V)', fontsize=14, fontweight='bold')
        ax.set_ylabel('$I_d$ (μA)', fontsize=14, fontweight='bold')
        ax.legend(loc='best', frameon=False)

        # Tick marks
        ax.xaxis.set_major_locator(MaxNLocator(nbins=args.n_major_ticks, prune=None))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=args.n_major_ticks, prune=None))
        ax.xaxis.set_minor_locator(AutoMinorLocator(args.n_minor_ticks))
        ax.yaxis.set_minor_locator(AutoMinorLocator(args.n_minor_ticks))

        # Axis ranges
        if args.x_range is not None:
            ax.set_xlim(args.x_range)
        if args.y_range is not None:
            ax.set_ylim(args.y_range)

        # No grid lines (clean background)
        ax.grid(False)

        # Bold tick labels
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight('bold')

        # Apply annotations if provided
        if args.annotate:
            annotations = parse_annotations(args.annotate)
            apply_annotations(ax, annotations)

        plt.tight_layout()

        # Generate filename
        print(f"\n📝 Generating filename for {material} FET...")
        extension = get_extension(args.format)
        filename = generate_filename_safe(
            measurements,
            measurement_type='FET',
            subtype=material,
            device_id=device_id,
            sweep_type=sweep_type,
            extension=extension,
            interactive=args.interactive,
            verbose=True
        )

        if filename is None:
            print("❌ Filename generation cancelled")
            plt.close(fig)
            return None, None

        save_path = output_dir / filename

        # Save plot
        print(f"💾 Saving: {save_path.name}")
        plt.savefig(save_path, dpi=args.dpi, bbox_inches='tight', facecolor='white')
        print(f"✓ Saved: {save_path.name}")

        # Save metadata
        meta_path = save_path.with_suffix('.txt')
        if save_metadata(metadata, meta_path):
            print(f"✓ Metadata: {meta_path.name}")

        plt.close(fig)
        return fig, save_path

    except Exception as e:
        print(f"❌ Error plotting FET: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def plot_aat_clean(measurements, electrode_type, device_id, output_dir, args, sweep_type="Id-Vg"):
    """Plot AAT characteristics"""
    if not measurements:
        print("⚠️  No AAT measurements to plot")
        return None, None

    try:
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))

        # Get color palette
        colors = PALETTE_MAP[args.palette]

        metadata = {
            'device_id': device_id,
            'measurement_type': 'AAT',
            'electrode_type': electrode_type,
            'measurements': []
        }

        # Plot each sweep
        for idx, meas in enumerate(measurements):
            color = colors[idx % len(colors)]
            Vd = meas['Vd']
            Vg_fwd = meas['forward']['Vg']
            Id_fwd = meas['forward']['Id']

            peak_idx = np.argmax(np.abs(Id_fwd))
            peak_Vg = Vg_fwd[peak_idx]
            peak_Id = Id_fwd[peak_idx]

            # Use custom legend label if provided, otherwise use default
            if args.legend_labels and idx < len(args.legend_labels):
                label = args.legend_labels[idx]
            else:
                label = f"Vd = {Vd:.1f} V"

            ax.plot(Vg_fwd, Id_fwd * 1e9, '-', color=color, linewidth=2.5,
                   label=label, alpha=1.0, marker='o', markersize=3, markevery=5)

            if meas['backward']:
                Vg_bwd = meas['backward']['Vg']
                Id_bwd = meas['backward']['Id']
                ax.plot(Vg_bwd, Id_bwd * 1e9, '--', color=color, linewidth=2,
                       alpha=0.4, marker='s', markersize=3, markevery=5)

            # Store metadata
            meas_meta = {
                'Vd': Vd,
                'Vg_min': Vg_fwd.min(),
                'Vg_max': Vg_fwd.max(),
                'Id_min': Id_fwd.min(),
                'Id_max': Id_fwd.max(),
                'num_points': len(Vg_fwd),
                'peak': {
                    'Vpeak': peak_Vg,
                    'Ipeak': peak_Id
                }
            }
            metadata['measurements'].append(meas_meta)

        # Axis labels
        ax.set_xlabel('$V_g$ (V)', fontsize=14, fontweight='bold')
        ax.set_ylabel('$I_d$ (nA)', fontsize=14, fontweight='bold')
        ax.legend(loc='best', frameon=False)

        # Tick marks
        ax.xaxis.set_major_locator(MaxNLocator(nbins=args.n_major_ticks, prune=None))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=args.n_major_ticks, prune=None))
        ax.xaxis.set_minor_locator(AutoMinorLocator(args.n_minor_ticks))
        ax.yaxis.set_minor_locator(AutoMinorLocator(args.n_minor_ticks))

        # Axis ranges
        if args.x_range is not None:
            ax.set_xlim(args.x_range)
        if args.y_range is not None:
            ax.set_ylim(args.y_range)

        # No grid lines (clean background)
        ax.grid(False)

        # Bold tick labels
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight('bold')

        # Apply annotations if provided
        if args.annotate:
            annotations = parse_annotations(args.annotate)
            apply_annotations(ax, annotations)

        plt.tight_layout()

        # Generate filename
        print(f"\n📝 Generating filename for {electrode_type} AAT...")
        extension = get_extension(args.format)
        filename = generate_filename_safe(
            measurements,
            measurement_type='AAT',
            subtype=electrode_type.capitalize(),
            device_id=device_id,
            sweep_type=sweep_type,
            extension=extension,
            interactive=args.interactive,
            verbose=True
        )

        if filename is None:
            print("❌ Filename generation cancelled")
            plt.close(fig)
            return None, None

        save_path = output_dir / filename

        # Save plot
        print(f"💾 Saving: {save_path.name}")
        plt.savefig(save_path, dpi=args.dpi, bbox_inches='tight', facecolor='white')
        print(f"✓ Saved: {save_path.name}")

        # Save metadata
        meta_path = save_path.with_suffix('.txt')
        if save_metadata(metadata, meta_path):
            print(f"✓ Metadata: {meta_path.name}")

        plt.close(fig)
        return fig, save_path

    except Exception as e:
        print(f"❌ Error plotting AAT: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def plot_generic_merged(measurements, label, meas_type, device_id, output_dir, args, sweep_type="Id-Vg"):
    """
    Plot all measurements together in a single plot (fallback for no keyword match)

    Args:
        measurements: List of all measurements
        label: Custom label for the plot
        meas_type: 'AAT', 'FET', or 'auto'
        device_id: Device ID
        output_dir: Output directory
        args: Command-line arguments
        sweep_type: Type of sweep
    """
    if not measurements:
        print("⚠️  No measurements to plot")
        return None, None

    try:
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))

        # Get color palette
        colors = PALETTE_MAP[args.palette]

        # Auto-detect measurement type if needed
        if meas_type == 'auto':
            # Simple heuristic: if all currents are small (nA range), likely AAT
            all_currents = []
            for meas in measurements:
                all_currents.extend(np.abs(meas['forward']['Id']))
            max_current = np.max(all_currents)

            if max_current < 1e-6:  # Less than 1 µA
                meas_type = 'AAT'
                current_scale = 1e9  # nA
                current_unit = 'nA'
            else:
                meas_type = 'FET'
                current_scale = 1e6  # µA
                current_unit = 'µA'
        elif meas_type == 'AAT':
            current_scale = 1e9
            current_unit = 'nA'
        else:  # FET
            current_scale = 1e6
            current_unit = 'µA'

        print(f"\n📊 Plotting merged data as {meas_type}")
        print(f"   Total sweeps: {len(measurements)}")
        print(f"   Label: {label}")

        metadata = {
            'device_id': device_id,
            'measurement_type': meas_type,
            'label': label,
            'measurements': []
        }

        # Plot each sweep
        for idx, meas in enumerate(measurements):
            color = colors[idx % len(colors)]
            Vd = meas['Vd']
            Vg_fwd = meas['forward']['Vg']
            Id_fwd = meas['forward']['Id']

            # Use custom legend label if provided, otherwise use default
            if args.legend_labels and idx < len(args.legend_labels):
                label_text = args.legend_labels[idx]
            else:
                label_text = f"Vd = {Vd:.1f} V"

            ax.plot(Vg_fwd, Id_fwd * current_scale, '-', color=color, linewidth=2.5,
                   label=label_text, alpha=1.0, marker='o', markersize=3, markevery=5)

            if meas['backward']:
                Vg_bwd = meas['backward']['Vg']
                Id_bwd = meas['backward']['Id']
                ax.plot(Vg_bwd, Id_bwd * current_scale, '--', color=color, linewidth=2,
                       alpha=0.4, marker='s', markersize=3, markevery=5)

            # Store metadata
            meas_meta = {
                'Vd': Vd,
                'Vg_min': Vg_fwd.min(),
                'Vg_max': Vg_fwd.max(),
                'Id_min': Id_fwd.min(),
                'Id_max': Id_fwd.max(),
                'num_points': len(Vg_fwd)
            }
            metadata['measurements'].append(meas_meta)

        # Axis labels
        ax.set_xlabel('$V_g$ (V)', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'$I_d$ ({current_unit})', fontsize=14, fontweight='bold')
        ax.legend(loc='best', frameon=False)

        # Tick marks
        ax.xaxis.set_major_locator(MaxNLocator(nbins=args.n_major_ticks, prune=None))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=args.n_major_ticks, prune=None))
        ax.xaxis.set_minor_locator(AutoMinorLocator(args.n_minor_ticks))
        ax.yaxis.set_minor_locator(AutoMinorLocator(args.n_minor_ticks))

        # Axis ranges
        if args.x_range is not None:
            ax.set_xlim(args.x_range)
        if args.y_range is not None:
            ax.set_ylim(args.y_range)

        # No grid lines (clean background)
        ax.grid(False)

        # Bold tick labels
        for tick_label in ax.get_xticklabels() + ax.get_yticklabels():
            tick_label.set_fontweight('bold')

        # Apply annotations if provided
        if args.annotate:
            annotations = parse_annotations(args.annotate)
            apply_annotations(ax, annotations)

        plt.tight_layout()

        # Generate filename
        print(f"\n📝 Generating filename for {label}...")
        extension = get_extension(args.format)
        filename = generate_filename_safe(
            measurements,
            measurement_type=meas_type,
            subtype=label,
            device_id=device_id,
            sweep_type=sweep_type,
            extension=extension,
            interactive=args.interactive,
            verbose=True
        )

        if filename is None:
            # Fallback filename
            filename = f"{label}_{device_id}_{len(measurements)}sweeps{extension}"
            print(f"   Using fallback filename: {filename}")

        save_path = output_dir / filename

        # Save plot
        print(f"💾 Saving: {save_path.name}")
        plt.savefig(save_path, dpi=args.dpi, bbox_inches='tight', facecolor='white')
        print(f"✓ Saved: {save_path.name}")

        # Save metadata
        meta_path = save_path.with_suffix('.txt')
        if save_metadata(metadata, meta_path):
            print(f"✓ Metadata: {meta_path.name}")

        plt.close(fig)
        return fig, save_path

    except Exception as e:
        print(f"❌ Error plotting merged data: {e}")
        import traceback
        traceback.print_exc()
        return None, None

# ========== MAIN ==========
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

    # Apply defaults for remaining unspecified parameters
    args = apply_defaults(args)

    # Setup plotting style
    setup_plot_style(args)

    # Print banner
    print("\n" + "="*70)
    print(f"AAT/FET PLOTTING SYSTEM v{__version__}")
    print("="*70)
    print(f"Author: {__author__}")
    print(f"Lab: {__lab__}")

    # Determine input path(s)
    input_paths = [Path(p) for p in args.input]

    # Validate all paths exist
    for p in input_paths:
        if not p.exists():
            print(f"\n❌ Error: Path does not exist: {p}")
            return

    # For single input, use it directly; for multiple, treat as multi-file mode
    multi_file_mode = len(input_paths) > 1 or (len(input_paths) == 1 and input_paths[0].is_file() and len(args.input) > 1)
    data_path = input_paths[0]  # Primary path (used for output dir default)

    # Set output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        if multi_file_mode or data_path.is_file():
            output_dir = data_path.parent / "merged_plots_output"
        else:
            output_dir = data_path / "merged_plots_output"

    # Print configuration
    if multi_file_mode:
        print(f"\n📂 Input: {len(input_paths)} files")
        for p in input_paths:
            print(f"   → {p.name}")
    else:
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
    if args.force_merge:
        print(f"🔀 Mode: Force merge (all files in single plot)")
    if args.label:
        print(f"🏷️  Custom label: {args.label}")
    if args.type != 'auto':
        print(f"📊 Measurement type: {args.type}")

    # Create output directory
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory ready")
    except Exception as e:
        print(f"❌ Error creating output directory: {e}")
        return

    # Load data
    print("\n" + "="*70)
    print("LOADING DATA")
    print("="*70)

    loader = AATDataLoader()

    if multi_file_mode:
        # Multiple files specified - load each and merge
        all_measurements = []
        for fpath in input_paths:
            print(f"\n📄 File: {fpath.name}")
            measurements = loader.load_measurement(fpath)
            if measurements:
                all_measurements.extend(measurements)
                print(f"   ✓ Loaded {len(measurements)} sweep(s)")
            else:
                print(f"   ⚠️  No data loaded from {fpath.name}")
        print(f"\n📊 Total sweeps from {len(input_paths)} files: {len(all_measurements)}")
    elif data_path.is_file():
        print(f"\n📄 File: {data_path.name}")
        measurements = loader.load_measurement(data_path)
        if measurements:
            all_measurements = measurements
        else:
            print("❌ Failed to load data")
            return
    else:
        all_measurements = loader.load_directory(data_path)

    if not all_measurements:
        print("❌ No measurements found!")
        return

    # Get device ID - Priority: command line > settings file > default
    if args.device:
        device_id = args.device
        print(f"\n🔬 Device ID: {device_id} (from command line)")
    elif all_measurements[0]['metadata'].get('device_id'):
        device_id = all_measurements[0]['metadata']['device_id']
        print(f"\n🔬 Device ID: {device_id} (from settings file)")
    else:
        device_id = "DV-26-XX"  # Default fallback (DV=Device, 26=2026, XX=ID number)
        print(f"\n🔬 Device ID: {device_id} (default)")

    # Organize measurements
    organized = loader.organize_by_type(all_measurements)

    # Check if force-merge is requested or no keywords matched
    any_organized = any(
        organized['FET']['ReS2'] or organized['FET']['WSe2'] or
        organized['AAT']['inner'] or organized['AAT']['outer']
    )

    if args.force_merge or not any_organized:
        # FALLBACK: Plot all measurements together
        print("\n" + "="*70)
        if args.force_merge:
            print("FORCE MERGE MODE - Plotting all measurements together")
        else:
            print("NO KEYWORDS FOUND - Fallback to merged plot")
        print("="*70)

        # Get label
        if args.label:
            label = args.label
        elif args.interactive:
            label = input("\n📝 Enter plot label (e.g., 'Outer_AAT', 'Device_Test'): ").strip()
            if not label:
                label = "Merged_Plot"
        else:
            label = "Merged_Plot"

        # Get measurement type
        if args.type != 'auto':
            meas_type = args.type
        elif args.interactive:
            print("\n🔬 Measurement type:")
            print("   1) AAT (Anti-ambipolar, nA scale)")
            print("   2) FET (Field-effect, µA scale)")
            print("   3) Auto (detect from current magnitude)")
            choice = input("Select [1/2/3, default=3]: ").strip()
            if choice == '1':
                meas_type = 'AAT'
            elif choice == '2':
                meas_type = 'FET'
            else:
                meas_type = 'auto'
        else:
            meas_type = 'auto'

        print(f"\n📊 Creating merged plot: {label} ({meas_type})")
        plot_generic_merged(all_measurements, label, meas_type, device_id, output_dir, args)

    else:
        # KEYWORD-BASED GROUPING: Plot by categories
        print("\n" + "="*70)
        print("KEYWORD-BASED PLOTTING")
        print("="*70)

        # Plot FET measurements
        print("\n📊 FET Characteristics:")
        if organized['FET']['ReS2']:
            plot_fet_clean(organized['FET']['ReS2'], 'ReS2', device_id, output_dir, args)
        else:
            print("   ⚠️  No ReS2 FET measurements found")

        if organized['FET']['WSe2']:
            plot_fet_clean(organized['FET']['WSe2'], 'WSe2', device_id, output_dir, args)
        else:
            print("   ⚠️  No WSe2 FET measurements found")

        # Plot AAT measurements
        print("\n📊 AAT Characteristics:")
        if organized['AAT']['inner']:
            plot_aat_clean(organized['AAT']['inner'], 'inner', device_id, output_dir, args)
        else:
            print("   ⚠️  No inner electrode AAT measurements found")

        if organized['AAT']['outer']:
            plot_aat_clean(organized['AAT']['outer'], 'outer', device_id, output_dir, args)
        else:
            print("   ⚠️  No outer electrode AAT measurements found")

    # Final summary
    print("\n" + "="*70)
    print("COMPLETE!")
    print("="*70)
    print(f"\n📁 Output directory: {output_dir}")

    # List generated files
    plot_files = sorted(output_dir.glob(f"*.{args.format}"))
    if plot_files:
        print(f"\n✅ Generated {len(plot_files)} plot(s):")
        for f in plot_files:
            if 'diagnostic' not in f.stem:
                print(f"   • {f.name}")
    else:
        print("\n⚠️  No plots were generated")

    print("\n" + "="*70)
    print("✓ All operations completed successfully")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
