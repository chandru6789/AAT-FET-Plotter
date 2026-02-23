#!/usr/bin/env python3
"""
Robust Filename Generator with Manual Fallback
==============================================
Zero-tolerance error handling for research data

Features:
- Automatic detection with validation
- Manual input fallback when auto-detection fails
- Clear confirmation of all parameters
- No silent failures or wrong assumptions
"""

from pathlib import Path
import numpy as np
import sys

def validate_measurement_type(meas_type):
    """Validate measurement type"""
    valid = ['FET', 'AAT', 'fet', 'aat']
    if meas_type not in valid:
        print(f"⚠️  Warning: '{meas_type}' is not a standard measurement type")
        print(f"   Expected: FET or AAT")
        response = input(f"   Use '{meas_type}' anyway? (y/n): ").strip().lower()
        if response != 'y':
            return None
    return meas_type.upper()

def validate_sweep_type(sweep_type):
    """Validate sweep type"""
    valid = ['Id-Vg', 'Id-Vd', 'Ig-Vg', 'Ig-Vd', 'C-V', 'G-V']
    if sweep_type not in valid:
        print(f"⚠️  Warning: '{sweep_type}' is not a standard sweep type")
        print(f"   Expected: {', '.join(valid)}")
        response = input(f"   Use '{sweep_type}' anyway? (y/n): ").strip().lower()
        if response != 'y':
            return None
    return sweep_type

def generate_filename_safe(measurements, measurement_type, subtype, device_id, 
                           sweep_type="Id-Vg", extension=".png", 
                           interactive=True, verbose=True):
    """
    Generate filename with validation and manual fallback
    
    Parameters:
    -----------
    measurements : list of dict
        Measurement data
    measurement_type : str
        'FET' or 'AAT'
    subtype : str
        Material ('ReS2', 'WSe2') or electrode ('Inner', 'Outer')
    device_id : str
        Device identifier
    sweep_type : str
        Type of sweep (default: 'Id-Vg')
        Will be auto-detected from filename if available
    extension : str
        File extension (default: '.png')
    interactive : bool
        Allow manual input on detection failure (default: True)
    verbose : bool
        Print detailed information (default: True)
    
    Returns:
    --------
    str : Generated filename or None on failure
    """
    
    if not measurements:
        print("❌ Error: No measurements provided!")
        if interactive:
            print("\nManual filename entry:")
            manual = input("Enter filename (without extension): ").strip()
            if manual:
                return manual + extension
        return None
    
    # AUTO-DETECT SWEEP TYPE - Try metadata first, then filename
    detected_sweep_type = None
    metadata_source = None
    
    # Priority 1: Check if sweep_type is in metadata (already detected by data loader)
    if measurements[0].get('metadata', {}).get('sweep_type'):
        detected_sweep_type = measurements[0]['metadata']['sweep_type']
        metadata_source = measurements[0].get('metadata', {}).get('metadata_source', 'unknown')
        
        if verbose:
            source_label = "settings file" if metadata_source == 'settings_file' else "filename"
            print(f"✓ Sweep type from {source_label}: {detected_sweep_type}")
    
    # Priority 2: Parse from filepath if not in metadata
    elif measurements[0].get('metadata', {}).get('filepath'):
        filepath = measurements[0]['metadata']['filepath']
        filename_lower = str(filepath).lower()
        
        # Check for sweep type patterns in filename
        if 'id-vg' in filename_lower or 'idvg' in filename_lower:
            detected_sweep_type = 'Id-Vg'
        elif 'id-vd' in filename_lower or 'idvd' in filename_lower:
            detected_sweep_type = 'Id-Vd'
        elif 'ig-vg' in filename_lower or 'igvg' in filename_lower:
            detected_sweep_type = 'Ig-Vg'
        elif 'ig-vd' in filename_lower or 'igvd' in filename_lower:
            detected_sweep_type = 'Ig-Vd'
        
        if detected_sweep_type:
            metadata_source = 'filename'
            if verbose:
                print(f"✓ Auto-detected sweep type from filename: {detected_sweep_type}")
    
    # Use detected type if found
    if detected_sweep_type:
        sweep_type = detected_sweep_type

    
    # Validate inputs
    if verbose:
        print("\n" + "="*70)
        print("FILENAME GENERATION - VALIDATION")
        print("="*70)
    
    measurement_type = validate_measurement_type(measurement_type)
    if measurement_type is None:
        return None
    
    sweep_type = validate_sweep_type(sweep_type)
    if sweep_type is None:
        return None
    
    # Extract parameters from measurements
    try:
        vd_values = [m['Vd'] for m in measurements]
        vd_min = min(vd_values)
        vd_max = max(vd_values)
        num_sweeps = len(measurements)
        
        # Get Vg range from first measurement
        vg = measurements[0]['forward']['Vg']
        vg_min = vg.min()
        vg_max = vg.max()
        
        # Try to get date from first measurement
        date = measurements[0].get('metadata', {}).get('date', None)
        
        is_output = sweep_type in ('Id-Vd', 'Ig-Vd')
        if verbose:
            print(f"\n✓ Detected parameters:")
            print(f"  • Measurement type: {measurement_type}")
            print(f"  • Subtype: {subtype}")
            print(f"  • Sweep type: {sweep_type}")
            print(f"  • Number of sweeps: {num_sweeps}")
            if is_output:
                print(f"  • Vg range (parameter): {vd_min:.2f} to {vd_max:.2f} V")
                print(f"  • Vd range (sweep): {vg_min:.2f} to {vg_max:.2f} V")
            else:
                print(f"  • Vd range: {vd_min:.2f} to {vd_max:.2f} V")
                print(f"  • Vg range: {vg_min:.2f} to {vg_max:.2f} V")
            if date:
                print(f"  • Date: {date}")
            print(f"  • Device ID: {device_id}")

            # Show metadata source
            if metadata_source:
                source_label = "settings file" if metadata_source == 'settings_file' else "filename"
                print(f"  • Metadata source: {source_label} (high confidence)" if metadata_source == 'settings_file' else f"  • Metadata source: {source_label}")

    
    except Exception as e:
        print(f"❌ Error extracting parameters: {e}")
        if interactive:
            print("\n⚠️  Automatic detection failed. Manual input required.")
            return manual_filename_input(extension)
        return None
    
    # Build filename
    components = []
    
    # 1. Subtype (Material/Electrode)
    components.append(subtype)
    
    # 2. Measurement type
    components.append(measurement_type)
    
    # 3. Sweep type
    components.append(sweep_type)
    
    # 4. Number of sweeps
    sweep_word = "sweep" if num_sweeps == 1 else "sweeps"
    components.append(f"{num_sweeps}{sweep_word}")
    
    # 5 & 6. Parameter and sweep ranges (labels depend on sweep direction)
    if is_output:
        # Id-Vd d(Vg): 'Vd' key holds Vg parameter steps, 'forward.Vg' holds Vd sweep
        param_str = f"Vg{vd_min:.1f}to{vd_max:.1f}V"
        sweep_str = f"Vd{vg_min:.0f}to{vg_max:.0f}V"
    else:
        # Id-Vg (transfer): standard labeling
        if abs(vd_min - vd_max) < 0.01:
            param_str = f"Vd{vd_min:.1f}V"
        else:
            param_str = f"Vd{vd_min:.1f}to{vd_max:.1f}V"
        sweep_str = f"Vg{vg_min:.0f}to{vg_max:.0f}V"
    components.append(param_str)
    components.append(sweep_str)
    
    # 7. Device ID
    components.append(device_id)
    
    # 8. Date (if available)
    if date:
        components.append(date)
    
    # Join and clean
    filename = "_".join(components) + extension
    filename = filename.replace(" ", "_").replace(":", "-")
    
    # Confirmation
    if verbose or interactive:
        print(f"\n📝 Generated filename:")
        print(f"   {filename}")
        
        if interactive:
            response = input("\n   Confirm this filename? (y/n/edit): ").strip().lower()
            
            if response == 'n':
                return manual_filename_input(extension)
            elif response == 'edit':
                print(f"\n   Current: {filename}")
                new_name = input("   Enter new filename (without extension): ").strip()
                if new_name:
                    return new_name + extension
            elif response != 'y':
                print("   Invalid response. Using generated filename.")
    
    print("✓ Filename confirmed")
    return filename

def manual_filename_input(extension=".png"):
    """
    Prompt user for manual filename input
    
    Returns:
    --------
    str : Manually entered filename or None
    """
    print("\n" + "="*70)
    print("MANUAL FILENAME INPUT")
    print("="*70)
    
    print("\nPlease provide the following information:")
    
    # Get each component
    subtype = input("  1. Material/Electrode (e.g., ReS2, Inner): ").strip()
    if not subtype:
        print("❌ Cancelled")
        return None
    
    meas_type = input("  2. Measurement type (FET/AAT): ").strip().upper()
    if meas_type not in ['FET', 'AAT']:
        print("❌ Invalid measurement type")
        return None
    
    sweep_type = input("  3. Sweep type (e.g., Id-Vg): ").strip()
    if not sweep_type:
        sweep_type = "Id-Vg"
        print(f"     Using default: {sweep_type}")
    
    num_sweeps = input("  4. Number of sweeps: ").strip()
    if not num_sweeps:
        num_sweeps = "1"
    try:
        num_sweeps = int(num_sweeps)
    except:
        print("❌ Invalid number")
        return None
    
    vd_range = input("  5. Vd range (e.g., -1.0to1.0V or 0.5V): ").strip()
    if not vd_range:
        vd_range = "VdUnknown"
    
    device_id = input("  6. Device ID (e.g., DV-25-06): ").strip()
    if not device_id:
        device_id = "DeviceX"
    
    date = input("  7. Date (YYYY-MM-DD) [optional]: ").strip()
    
    # Build filename
    sweep_word = "sweep" if num_sweeps == 1 else "sweeps"
    components = [
        subtype,
        meas_type,
        sweep_type,
        f"{num_sweeps}{sweep_word}",
        vd_range,
        device_id
    ]
    
    if date:
        components.append(date)
    
    filename = "_".join(components) + extension
    filename = filename.replace(" ", "_").replace(":", "-")
    
    print(f"\n📝 Generated filename: {filename}")
    confirm = input("   Confirm? (y/n): ").strip().lower()
    
    if confirm == 'y':
        return filename
    else:
        print("❌ Filename not confirmed")
        return None

def generate_filename_compact(measurements, measurement_type, subtype, device_id,
                              sweep_type="Id-Vg", extension=".png"):
    """
    Compact filename (shorter - no date, no sweep count, but includes Vg range)
    
    Example: ReS2_FET_Id-Vg_Vd-1.0to1.0V_Vg-8to0V_DV-25-06.png
    """
    if not measurements:
        return f"{subtype}_{measurement_type}_{device_id}{extension}"
    
    # Auto-detect sweep type from metadata (priority 1) or filename (priority 2)
    if measurements[0].get('metadata', {}).get('sweep_type'):
        sweep_type = measurements[0]['metadata']['sweep_type']
    elif measurements[0].get('metadata', {}).get('filepath'):
        filepath = measurements[0]['metadata']['filepath']
        filename_lower = str(filepath).lower()
        
        if 'id-vg' in filename_lower or 'idvg' in filename_lower:
            sweep_type = 'Id-Vg'
        elif 'id-vd' in filename_lower or 'idvd' in filename_lower:
            sweep_type = 'Id-Vd'
        elif 'ig-vg' in filename_lower or 'igvg' in filename_lower:
            sweep_type = 'Ig-Vg'
        elif 'ig-vd' in filename_lower or 'igvd' in filename_lower:
            sweep_type = 'Ig-Vd'
    
    vd_values = [m['Vd'] for m in measurements]
    vd_min = min(vd_values)
    vd_max = max(vd_values)
    
    # Get Vg range
    vg = measurements[0]['forward']['Vg']
    vg_min = vg.min()
    vg_max = vg.max()
    
    if abs(vd_min - vd_max) < 0.01:
        vd_str = f"Vd{vd_min:.1f}V"
    else:
        vd_str = f"Vd{vd_min:.1f}to{vd_max:.1f}V"
    
    vg_str = f"Vg{vg_min:.0f}to{vg_max:.0f}V"
    
    components = [subtype, measurement_type, sweep_type, vd_str, vg_str, device_id]
    filename = "_".join(components) + extension
    filename = filename.replace(" ", "_").replace(":", "-")
    
    return filename

def generate_filename_detailed(measurements, measurement_type, subtype, device_id,
                               sweep_type="Id-Vg", extension=".png"):
    """
    Detailed filename with maximum information
    
    Example: ReS2_FET_Id-Vg_5sweeps_Vd-1.0to1.0V_Vg-8to0V_101pts_DV-25-06_2026-02-05_09-59.png
    """
    if not measurements:
        return f"{subtype}_{measurement_type}_{device_id}{extension}"
    
    # Auto-detect sweep type from metadata (priority 1) or filename (priority 2)
    if measurements[0].get('metadata', {}).get('sweep_type'):
        sweep_type = measurements[0]['metadata']['sweep_type']
    elif measurements[0].get('metadata', {}).get('filepath'):
        filepath = measurements[0]['metadata']['filepath']
        filename_lower = str(filepath).lower()
        
        if 'id-vg' in filename_lower or 'idvg' in filename_lower:
            sweep_type = 'Id-Vg'
        elif 'id-vd' in filename_lower or 'idvd' in filename_lower:
            sweep_type = 'Id-Vd'
        elif 'ig-vg' in filename_lower or 'igvg' in filename_lower:
            sweep_type = 'Ig-Vg'
        elif 'ig-vd' in filename_lower or 'igvd' in filename_lower:
            sweep_type = 'Ig-Vd'
    
    # Extract all parameters
    vd_values = [m['Vd'] for m in measurements]
    vd_min = min(vd_values)
    vd_max = max(vd_values)
    num_sweeps = len(measurements)
    
    # Vg range from first measurement
    vg = measurements[0]['forward']['Vg']
    vg_min = vg.min()
    vg_max = vg.max()
    
    # Average points
    avg_points = int(np.mean([len(m['forward']['Vg']) for m in measurements]))
    
    # Date and time
    date = measurements[0].get('metadata', {}).get('date', None)
    time = measurements[0].get('metadata', {}).get('time', None)
    
    # Build components
    components = []
    components.append(subtype)
    components.append(measurement_type)
    components.append(sweep_type)
    
    sweep_word = "sweep" if num_sweeps == 1 else "sweeps"
    components.append(f"{num_sweeps}{sweep_word}")
    
    if abs(vd_min - vd_max) < 0.01:
        components.append(f"Vd{vd_min:.1f}V")
    else:
        components.append(f"Vd{vd_min:.1f}to{vd_max:.1f}V")
    
    components.append(f"Vg{vg_min:.0f}to{vg_max:.0f}V")
    components.append(f"{avg_points}pts")
    components.append(device_id)
    
    if date:
        components.append(date)
    if time:
        time_short = time[:5].replace(":", "-")
        components.append(time_short)
    
    filename = "_".join(components) + extension
    filename = filename.replace(" ", "_").replace(":", "-")
    
    return filename

# Alias for backward compatibility
generate_filename = generate_filename_safe

if __name__ == "__main__":
    print("="*70)
    print("ROBUST FILENAME GENERATOR - INTERACTIVE TEST")
    print("="*70)
    
    # Mock data
    mock_measurements = [
        {'Vd': -1.0, 'forward': {'Vg': np.linspace(0, -8, 101)}, 
         'metadata': {'date': '2026-02-05', 'time': '09:59:53'}},
        {'Vd': -0.5, 'forward': {'Vg': np.linspace(0, -8, 101)}, 
         'metadata': {'date': '2026-02-05', 'time': '09:59:53'}},
        {'Vd': 0.0, 'forward': {'Vg': np.linspace(0, -8, 101)}, 
         'metadata': {'date': '2026-02-05', 'time': '09:59:53'}},
        {'Vd': 0.5, 'forward': {'Vg': np.linspace(0, -8, 101)}, 
         'metadata': {'date': '2026-02-05', 'time': '09:59:53'}},
        {'Vd': 1.0, 'forward': {'Vg': np.linspace(0, -8, 101)}, 
         'metadata': {'date': '2026-02-05', 'time': '09:59:53'}},
    ]
    
    print("\n1. TESTING SAFE MODE (with validation):")
    print("-" * 70)
    filename = generate_filename_safe(
        mock_measurements, 
        'FET', 
        'ReS2', 
        'DV-25-06',
        interactive=True,
        verbose=True
    )
    print(f"\nFinal result: {filename}")
    
    print("\n" + "="*70)
    print("Test complete!")
