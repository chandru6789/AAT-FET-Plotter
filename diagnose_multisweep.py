#!/usr/bin/env python3
"""
Quick Diagnostic for Multi-Sweep AAT Data Files
===============================================
Check how your data file is split into separate Vd sweeps

Usage:
    python diagnose_multisweep.py /path/to/file.txt
    python diagnose_multisweep.py /path/to/directory/
"""

import sys
from pathlib import Path

# Set non-interactive backend BEFORE importing pyplot
import matplotlib
matplotlib.use('Agg')  # Non-interactive: saves files without displaying

from aat_data_loader_multisweep import AATDataLoader

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python diagnose_multisweep.py /path/to/file.txt")
        print("  python diagnose_multisweep.py /path/to/directory/")
        return
    
    target = Path(sys.argv[1])
    loader = AATDataLoader()
    
    if target.is_file():
        # Single file diagnostic
        print("="*70)
        print("MULTI-SWEEP FILE DIAGNOSTIC")
        print("="*70)
        loader.diagnose_file(target, save_plot=True)
        
    elif target.is_dir():
        # Batch diagnostic
        print("="*70)
        print("BATCH DIAGNOSTIC - MULTI-SWEEP FILES")
        print("="*70)
        
        files = [f for f in target.glob("*.txt") 
                if not f.stem.endswith('-s') and 
                'diagnostic' not in f.stem.lower()]
        
        print(f"\nFound {len(files)} data files\n")
        
        for filepath in sorted(files):
            print(f"\n{'='*70}")
            print(f"File: {filepath.name}")
            print(f"{'='*70}")
            
            measurements = loader.load_measurement(filepath)
            
            if measurements:
                print(f"✓ {len(measurements)} sweep(s) detected:")
                for idx, meas in enumerate(measurements, 1):
                    bidir = "bidirectional" if meas['backward'] else "unidirectional"
                    print(f"  {idx}. Vd = {meas['Vd']:.2f} V ({bidir}, {len(meas['Vg'])} points)")
            else:
                print(f"❌ Failed to load")
        
        # Offer to create diagnostic plots
        print("\n" + "="*70)
        response = input("\nCreate diagnostic plots for all files? (y/n): ")
        
        if response.lower() == 'y':
            print("\nGenerating diagnostic plots...")
            for filepath in files:
                print(f"\n  Processing: {filepath.name}")
                loader.diagnose_file(filepath, save_plot=True)
            
            print("\n✓ All diagnostic plots saved!")
    else:
        print(f"❌ Error: {target} not found!")

if __name__ == "__main__":
    main()
