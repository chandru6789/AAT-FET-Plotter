#!/usr/bin/env python3
"""
AAT Data Loader Module - Multi-Sweep Version with Enhanced Device ID Extraction
================================================================================
Handles multiple consecutive sweeps at different Vd in a single file
NOW INCLUDES: Automatic Device ID extraction from settings files

Author: Chandrasekar Sivakumar
Date: 2026-02-07
Version: 5.0 (Enhanced Device ID support)
"""

import numpy as np
import re
from pathlib import Path
from typing import Tuple, Optional, List, Dict

class AATDataLoader:
    """
    Load and parse Keysight B2912A measurement data files
    SUPPORTS:
    - Multiple sweeps at different Vd in single file
    - Automatic Device ID extraction from settings files
    - Full metadata extraction from instrument settings

    Data format:
    - Column 1 (V2): Gate voltage (Vg) - swept parameter
    - Column 2 (I1): Drain current (Id) - primary measurement
    - Column 3 (I2): Gate current (Ig) - leakage
    - Column 4 (V1): Drain voltage (Vd) - changes between sweeps
    """

    def __init__(self):
        self.data_files = []

    def _find_settings_file(self, data_filepath: Path) -> Optional[Path]:
        """
        Find corresponding -s settings file for a data file

        Tries multiple naming patterns:
        1. filename-s.txt (exact match with dash)
        2. filename -s.txt (exact match with space)
        3. filename_-s.txt (exact match with underscore)
        4. Similar filename with -s pattern (handles naming variations)

        Returns:
        --------
        Path to settings file if found, None otherwise
        """
        # Get the base filename without extension
        base = data_filepath.stem
        parent = data_filepath.parent

        # Remove trailing underscores/spaces from base
        base_cleaned = base.rstrip('_ ')

        # Pattern 1: filename-s.txt (most common)
        settings_file = parent / f"{base}-s.txt"
        if settings_file.exists():
            return settings_file

        # Pattern 2: filename -s.txt (with space)
        settings_file = parent / f"{base} -s.txt"
        if settings_file.exists():
            return settings_file

        # Pattern 3: filename_-s.txt (with underscore)
        settings_file = parent / f"{base}_-s.txt"
        if settings_file.exists():
            return settings_file

        # Pattern 4: Try cleaned base
        settings_file = parent / f"{base_cleaned}-s.txt"
        if settings_file.exists():
            return settings_file

        settings_file = parent / f"{base_cleaned}_-s.txt"
        if settings_file.exists():
            return settings_file

        # Pattern 5: Fuzzy match - look for similar filenames with -s
        # This handles cases where the base names differ slightly
        for possible_settings in parent.glob("*-s.txt"):
            # Get the settings base name (without -s.txt)
            settings_base = possible_settings.stem.replace('-s', '').rstrip('_ ')

            # Check if it's similar (contains key parts of the data filename)
            # Extract key identifying parts (measurement type, date/time stamps)
            data_parts = base_cleaned.replace('_', ' ').split()
            settings_parts = settings_base.replace('_', ' ').split()

            # Look for date pattern (YYYY_MM_DD H_M_S or similar)
            date_time_pattern = r'\d{4}[_\s]\d{2}[_\s]\d{2}[_\s]\d{1,2}[_\s]\d{1,2}[_\s]\d{1,2}'
            import re

            data_datetime = re.search(date_time_pattern, base)
            settings_datetime = re.search(date_time_pattern, possible_settings.stem)

            if data_datetime and settings_datetime:
                # Compare date/time stamps - if they match, it's likely the right settings file
                if data_datetime.group() == settings_datetime.group():
                    return possible_settings

        return None

    def _parse_settings_file(self, settings_filepath: Path) -> Dict:
        """
        Parse Keysight B2912A settings file (tab-separated format)

        Extracts:
        - Setup title (sweep type)
        - Test date and time
        - Device ID ⭐ NEW: Always extracted!
        - Primary sweep parameters (Vg start/stop/step)
        - Bias source (Vd)
        - Locus type (bidirectional or not)

        Returns:
        --------
        Dict with parsed metadata, or empty dict if parsing fails
        """
        metadata = {
            'sweep_type': None,
            'date': None,
            'time': None,
            'device_id': None,  # ⭐ Device ID from settings file!
            'vg_start': None,
            'vg_stop': None,
            'vg_step': None,
            'vd_bias': None,
            'bidirectional': None,
            'metadata_source': 'settings_file'
        }

        try:
            with open(settings_filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # Split by tab
                    parts = line.split('\t')
                    if len(parts) < 2:
                        continue

                    key = parts[0].strip()
                    values = [p.strip() for p in parts[1:] if p.strip()]

                    # Extract relevant fields
                    if key == 'Setup title':
                        # This is the sweep type (e.g., "Id-Vg", "Id-Vd")
                        metadata['sweep_type'] = values[0] if values else None

                    elif key == 'Test date':
                        # Format: YYYY/MM/DD -> convert to YYYY-MM-DD
                        if values:
                            date_str = values[0].replace('/', '-')
                            metadata['date'] = date_str

                    elif key == 'Test time':
                        # Format: HH:MM:SS
                        metadata['time'] = values[0] if values else None

                    elif key == 'Device ID':
                        # ⭐ DEVICE ID - Extracted automatically from settings file!
                        metadata['device_id'] = values[0] if values else None

                    elif key == 'Measurement.Primary.Start':
                        # Vg start value
                        try:
                            metadata['vg_start'] = float(values[0]) if values else None
                        except (ValueError, IndexError):
                            pass

                    elif key == 'Measurement.Primary.Stop':
                        # Vg stop value
                        try:
                            metadata['vg_stop'] = float(values[0]) if values else None
                        except (ValueError, IndexError):
                            pass

                    elif key == 'Measurement.Primary.Step':
                        # Vg step value
                        try:
                            metadata['vg_step'] = float(values[0]) if values else None
                        except (ValueError, IndexError):
                            pass

                    elif key == 'Measurement.Bias.Source':
                        # Vd bias values (can be multiple: one for SMU1, one for SMU2)
                        # Typically: SMU1 = Vd (drain), SMU2 = 0 (source/ground)
                        try:
                            if values:
                                # Take the first value as Vd
                                metadata['vd_bias'] = float(values[0])
                        except (ValueError, IndexError):
                            pass

                    elif key == 'Measurement.Primary.Locus':
                        # "Double" means bidirectional, "Single" means unidirectional
                        if values:
                            locus = values[0].lower()
                            metadata['bidirectional'] = (locus == 'double')

            return metadata

        except Exception as e:
            print(f"⚠️  Warning: Could not parse settings file {settings_filepath.name}: {e}")
            return {}

    def load_measurement(self, filepath: Path) -> List[Dict]:
        """
        Load a measurement file containing multiple sweeps at different Vd

        Returns:
        --------
        List of measurement dictionaries, one per Vd value
        Each dict contains:
            - 'Vg': Gate voltage array for this Vd
            - 'Id': Drain current array
            - 'Ig': Gate current array
            - 'Vd': Drain voltage value (constant for this sweep)
            - 'forward': Forward sweep data
            - 'backward': Backward sweep data (if bidirectional)
            - 'metadata': File information including Device ID
        """
        try:
            # Read the data file (skip first 2 rows: header + units)
            data = np.loadtxt(filepath, skiprows=2, delimiter='\t')

            if data.shape[1] < 4:
                print(f"⚠️  Warning: Expected 4 columns, got {data.shape[1]}")
                return None

            # Extract columns
            Vg_all = data[:, 0]  # V2 = Gate voltage
            Id_all = data[:, 1]  # I1 = Drain current
            Ig_all = data[:, 2]  # I2 = Gate current
            Vd_all = data[:, 3]  # V1 = Drain voltage

            # Split into separate sweeps by Vd value
            measurements = self._split_by_vd(Vg_all, Id_all, Ig_all, Vd_all)

            # PRIORITY SYSTEM: Settings file > Filename parsing
            # Step 1: Try to find and parse settings file
            settings_file = self._find_settings_file(filepath)
            settings_metadata = {}

            if settings_file:
                print(f"✓ Found settings file: {settings_file.name}")
                settings_metadata = self._parse_settings_file(settings_file)

                if settings_metadata:
                    device_id = settings_metadata.get('device_id')
                    if device_id:
                        print(f"✓ Loaded metadata from settings file (Device ID: {device_id})")
                    else:
                        print(f"✓ Loaded metadata from settings file (high confidence)")
                else:
                    print(f"⚠️  Settings file found but parsing failed, using filename")

            # Step 2: Extract metadata from filename (fallback or supplement)
            file_metadata = self._extract_metadata(filepath)

            # Step 3: Merge metadata with priority: settings > filename
            # Settings file data overrides filename data when both exist
            final_metadata = file_metadata.copy()
            final_metadata.update({k: v for k, v in settings_metadata.items() if v is not None})

            # Add metadata source tracking
            if settings_metadata:
                final_metadata['metadata_source'] = 'settings_file'
                final_metadata['settings_file'] = str(settings_file)
            else:
                final_metadata['metadata_source'] = 'filename'

            # Add metadata to each measurement
            for meas in measurements:
                meas['metadata'] = final_metadata.copy()
                meas['metadata']['filepath'] = filepath

            return measurements

        except Exception as e:
            print(f"❌ Error loading {filepath.name}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _split_by_vd(self, Vg, Id, Ig, Vd) -> List[Dict]:
        """
        Split data into separate measurements by Vd value

        Returns list of measurement dicts, one per unique Vd
        """
        # Find unique Vd values and where they change
        Vd_rounded = np.round(Vd, decimals=3)  # Round to avoid floating point issues
        unique_vd = np.unique(Vd_rounded)

        measurements = []

        for vd_value in unique_vd:
            # Get indices for this Vd value
            mask = (Vd_rounded == vd_value)
            indices = np.where(mask)[0]

            if len(indices) == 0:
                continue

            # Extract data for this Vd
            Vg_sweep = Vg[mask]
            Id_sweep = Id[mask]
            Ig_sweep = Ig[mask]

            # Check if this sweep is bidirectional
            forward_data, backward_data = self._detect_bidirectional_sweep(
                Vg_sweep, Id_sweep, Ig_sweep
            )

            measurement = {
                'Vg': Vg_sweep,
                'Id': Id_sweep,
                'Ig': Ig_sweep,
                'Vd': float(vd_value),
                'forward': forward_data,
                'backward': backward_data,
                'indices': indices  # Store original indices
            }

            measurements.append(measurement)

        # Sort by Vd value
        measurements.sort(key=lambda x: x['Vd'])

        return measurements

    def _detect_bidirectional_sweep(self, Vg, Id, Ig) -> Tuple[Dict, Optional[Dict]]:
        """
        Detect if a single sweep is bidirectional (goes forward then backward)

        Returns forward_data, backward_data (or None if unidirectional)
        """
        if len(Vg) < 10:
            # Too short
            return {'Vg': Vg, 'Id': Id, 'Ig': Ig}, None

        # Calculate voltage trend
        dVg = np.diff(Vg)

        # Check if voltage reverses direction
        # Use median to be robust to noise
        first_half_trend = np.median(dVg[:len(dVg)//2])
        second_half_trend = np.median(dVg[len(dVg)//2:])

        # If trends have opposite signs, it's bidirectional
        if np.sign(first_half_trend) != np.sign(second_half_trend) and \
           abs(first_half_trend) > 0.001 and abs(second_half_trend) > 0.001:

            # Find the turning point (where direction changes)
            # Look for the maximum or minimum Vg
            if first_half_trend > 0:
                # Going up first, find maximum
                split_idx = np.argmax(Vg)
            else:
                # Going down first, find minimum
                split_idx = np.argmin(Vg)

            forward_data = {
                'Vg': Vg[:split_idx+1],
                'Id': Id[:split_idx+1],
                'Ig': Ig[:split_idx+1]
            }

            backward_data = {
                'Vg': Vg[split_idx+1:],
                'Id': Id[split_idx+1:],
                'Ig': Ig[split_idx+1:]
            }

            return forward_data, backward_data

        # Unidirectional
        return {'Vg': Vg, 'Id': Id, 'Ig': Ig}, None

    def diagnose_file(self, filepath: Path, save_plot: bool = True):
        """
        Diagnostic tool to visualize how the file is split into sweeps

        Shows:
        - All sweeps overlaid
        - Each sweep colored by Vd value
        - Vd vs index to see transitions
        """
        import matplotlib.pyplot as plt

        # Load raw data
        try:
            data = np.loadtxt(filepath, skiprows=2, delimiter='\t')
            Vg_all = data[:, 0]
            Id_all = data[:, 1]
            Vd_all = data[:, 3]
        except:
            print(f"❌ Could not load {filepath}")
            return

        # Load processed measurements
        measurements = self.load_measurement(filepath)

        if not measurements:
            print(f"❌ No measurements found in {filepath}")
            return

        # Create diagnostic plot
        fig, axes = plt.subplots(3, 1, figsize=(12, 12))

        # Top: All data overlaid by Vd
        ax1 = axes[0]
        colors = plt.cm.viridis(np.linspace(0, 1, len(measurements)))

        for idx, meas in enumerate(measurements):
            Vd = meas['Vd']
            Vg = meas['Vg']
            Id = meas['Id']

            ax1.plot(Vg, Id * 1e9, 'o-', markersize=3, linewidth=1.5,
                    color=colors[idx], label=f'Vd = {Vd:.2f} V',
                    alpha=0.7)

        ax1.set_xlabel('Vg (V)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Id (nA)', fontsize=12, fontweight='bold')
        ax1.set_title(f'All Sweeps: {filepath.name}', fontsize=14, fontweight='bold')
        ax1.legend(loc='best', fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(0, color='black', linewidth=1)
        ax1.axvline(0, color='black', linewidth=1)

        # Middle: Vd vs index (shows transitions)
        ax2 = axes[1]
        indices = np.arange(len(Vd_all))
        ax2.plot(indices, Vd_all, 'o-', markersize=3, linewidth=1.5,
                color='#E69F00')

        # Mark boundaries between sweeps
        for meas in measurements:
            start_idx = meas['indices'][0]
            end_idx = meas['indices'][-1]
            ax2.axvline(start_idx, color='red', linestyle='--', alpha=0.5)
            ax2.axvline(end_idx, color='red', linestyle='--', alpha=0.5)

            # Label each region
            mid_idx = (start_idx + end_idx) // 2
            ax2.text(mid_idx, meas['Vd'], f"{meas['Vd']:.1f}V",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax2.set_xlabel('Data Point Index', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Vd (V)', fontsize=12, fontweight='bold')
        ax2.set_title('Vd vs Index (Shows sweep boundaries)', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Bottom: Vg vs index (shows sweep patterns)
        ax3 = axes[2]
        ax3.plot(indices, Vg_all, 'o-', markersize=3, linewidth=1.5,
                color='#009E73')

        # Color-code each sweep region
        for idx, meas in enumerate(measurements):
            start_idx = meas['indices'][0]
            end_idx = meas['indices'][-1]
            ax3.axvspan(start_idx, end_idx, alpha=0.2, color=colors[idx])

        ax3.set_xlabel('Data Point Index', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Vg (V)', fontsize=12, fontweight='bold')
        ax3.set_title('Vg vs Index (Shows sweep direction)', fontsize=13, fontweight='bold')
        ax3.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_plot:
            save_path = filepath.parent / f"{filepath.stem}_multi_sweep_diagnostic.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"✓ Diagnostic plot saved: {save_path.name}")

        plt.show()

        # Print summary
        print("\n" + "="*70)
        print("MULTI-SWEEP FILE ANALYSIS")
        print("="*70)
        print(f"File: {filepath.name}")
        print(f"Total data points: {len(Vd_all)}")
        print(f"Number of sweeps detected: {len(measurements)}")
        print()

        for idx, meas in enumerate(measurements, 1):
            print(f"Sweep {idx}:")
            print(f"  Vd = {meas['Vd']:.3f} V")
            print(f"  Points: {len(meas['Vg'])}")
            print(f"  Vg range: {meas['Vg'].min():.2f} to {meas['Vg'].max():.2f} V")
            print(f"  Id range: {meas['Id'].min():.3e} to {meas['Id'].max():.3e} A")

            if meas['backward']:
                print(f"  Type: Bidirectional")
                print(f"    Forward: {len(meas['forward']['Vg'])} points")
                print(f"    Backward: {len(meas['backward']['Vg'])} points")
            else:
                print(f"  Type: Unidirectional")
            print()

        print("="*70)

        return measurements

    def _extract_metadata(self, filepath: Path) -> Dict:
        """Extract metadata from filename including sweep type"""
        filename = filepath.stem

        metadata = {
            'filename': filepath.name,
            'filepath': filepath,
            'date': None,
            'time': None,
            'description': None,
            'measurement_type': None,
            'electrode_type': None,
            'material': None,
            'sweep_type': None,
            'device_id': None  # Can be extracted from filename if present
        }

        # AUTO-DETECT SWEEP TYPE from filename
        filename_lower = filename.lower()

        if 'id-vg' in filename_lower or 'idvg' in filename_lower:
            metadata['sweep_type'] = 'Id-Vg'
        elif 'id-vd' in filename_lower or 'idvd' in filename_lower:
            metadata['sweep_type'] = 'Id-Vd'
        elif 'ig-vg' in filename_lower or 'igvg' in filename_lower:
            metadata['sweep_type'] = 'Ig-Vg'
        elif 'ig-vd' in filename_lower or 'igvd' in filename_lower:
            metadata['sweep_type'] = 'Ig-Vd'
        else:
            # Default to Id-Vg if not detected
            metadata['sweep_type'] = 'Id-Vg'

        # Try format 1: With brackets [ Description; Date]
        match = re.search(r'\[(.+?);', filename)
        if match:
            description = match.group(1).strip()
            metadata['description'] = description
        else:
            # Try format 2: With underscores
            parts = re.split(r'_{2,}', filename)
            if len(parts) >= 2:
                description = parts[0].replace('Id-Vg', '').strip('_').replace('_', ' ')
                if not description:
                    description = parts[1] if len(parts) > 1 else None
                else:
                    description = parts[1] if len(parts) > 1 else description

                metadata['description'] = description

        # Analyze description
        if metadata['description']:
            description_lower = metadata['description'].lower()

            if 'aat' in description_lower:
                metadata['measurement_type'] = 'AAT'

                if 'inner' in description_lower:
                    metadata['electrode_type'] = 'inner'
                elif 'outer' in description_lower or 'outter' in description_lower:
                    metadata['electrode_type'] = 'outer'

            elif 'fet' in description_lower:
                metadata['measurement_type'] = 'FET'

                if 'res2' in description_lower or 'res₂' in description_lower:
                    metadata['material'] = 'ReS2'
                elif 'wse2' in description_lower or 'wse₂' in description_lower:
                    metadata['material'] = 'WSe2'

        # Extract date
        date_match = re.search(r'(\d{4})_(\d{1,2})_(\d{1,2})', filename)
        if date_match:
            y, m, d = date_match.groups()
            metadata['date'] = f"{y}-{m.zfill(2)}-{d.zfill(2)}"

        # Extract time
        time_match = re.search(r'_(\d{1,2})_(\d{1,2})_(\d{1,2})(?:_|\.)', filename)
        if time_match:
            h, m, s = time_match.groups()
            metadata['time'] = f"{h.zfill(2)}:{m.zfill(2)}:{s.zfill(2)}"

        return metadata

    def load_directory(self, directory: Path, pattern: str = "*.txt") -> List[Dict]:
        """
        Load all measurement files from a directory

        Returns:
        --------
        List of ALL measurements from all files (flattened)
        Each file may contribute multiple measurements (one per Vd)
        """
        directory = Path(directory)

        # Find data files (exclude diagnostics)
        data_files = [f for f in directory.glob(pattern)
                     if not f.stem.endswith('-s') and
                     'diagnostic' not in f.stem.lower()]

        print(f"Found {len(data_files)} data files in {directory}")

        all_measurements = []

        for filepath in sorted(data_files):
            measurements = self.load_measurement(filepath)
            if measurements:
                all_measurements.extend(measurements)
                print(f"  {filepath.name}: {len(measurements)} sweep(s)")

        print(f"\nTotal measurements loaded: {len(all_measurements)}")

        return all_measurements

    def organize_by_type(self, measurements: List[Dict]) -> Dict:
        """
        Organize measurements by type (FET/AAT) and subtype

        Returns dict with measurements grouped by type
        """
        organized = {
            'FET': {'ReS2': [], 'WSe2': [], 'unknown': []},
            'AAT': {'inner': [], 'outer': [], 'unknown': []},
            'unknown': []
        }

        for meas in measurements:
            mtype = meas['metadata']['measurement_type']

            if mtype == 'FET':
                material = meas['metadata']['material']
                if material:
                    organized['FET'][material].append(meas)
                else:
                    organized['FET']['unknown'].append(meas)

            elif mtype == 'AAT':
                electrode = meas['metadata']['electrode_type']
                if electrode:
                    organized['AAT'][electrode].append(meas)
                else:
                    organized['AAT']['unknown'].append(meas)
            else:
                organized['unknown'].append(meas)

        return organized

    def print_summary(self, measurements: List[Dict]):
        """Print summary of loaded measurements"""
        print("\n" + "="*70)
        print("MEASUREMENT SUMMARY")
        print("="*70)

        organized = self.organize_by_type(measurements)

        print(f"\n📊 Total measurements: {len(measurements)}")

        print("\n🔬 FET Measurements:")
        for material, meas_list in organized['FET'].items():
            if meas_list:
                print(f"  • {material}: {len(meas_list)} measurement(s)")
                # Group by file
                by_file = {}
                for m in meas_list:
                    fname = m['metadata']['filename']
                    if fname not in by_file:
                        by_file[fname] = []
                    by_file[fname].append(m)

                for fname, file_meas in by_file.items():
                    print(f"    - {fname}")
                    for m in file_meas:
                        print(f"      Vd = {m['Vd']:.2f} V")

        print("\n⚡ AAT Measurements:")
        for electrode, meas_list in organized['AAT'].items():
            if meas_list:
                print(f"  • {electrode.capitalize()} electrodes: {len(meas_list)} measurement(s)")
                # Group by file
                by_file = {}
                for m in meas_list:
                    fname = m['metadata']['filename']
                    if fname not in by_file:
                        by_file[fname] = []
                    by_file[fname].append(m)

                for fname, file_meas in by_file.items():
                    print(f"    - {fname}")
                    for m in file_meas:
                        print(f"      Vd = {m['Vd']:.2f} V")

        if organized['unknown']:
            print(f"\n⚠️  Unknown type: {len(organized['unknown'])} measurement(s)")

        print("="*70)


# ========== QUICK START ==========

if __name__ == "__main__":
    print("="*70)
    print("AAT DATA LOADER - ENHANCED VERSION 5.0")
    print("="*70)
    print("\n✨ NEW FEATURE: Automatic Device ID extraction from settings files!")
    print("\n📖 USAGE:")
    print("\n1. DIAGNOSE FILE:")
    print("   loader = AATDataLoader()")
    print("   loader.diagnose_file('your_file.txt')")
    print("   # Shows how file is split into separate Vd sweeps")
    print("\n2. LOAD FILE:")
    print("   measurements = loader.load_measurement('your_file.txt')")
    print("   # Returns list of measurements with Device ID in metadata")
    print("\n3. ACCESS DEVICE ID:")
    print("   device_id = measurements[0]['metadata'].get('device_id', 'Unknown')")
    print("   print(f'Device: {device_id}')")
    print("\n" + "="*70)
