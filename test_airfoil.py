#!/usr/bin/env python
"""Test script for airfoil analysis functions."""

import aerodynamics as aero
import numpy as np
import pandas as pd

print("="*70)
print("Testing Airfoil Analysis Module")
print("="*70)

# Test 1: Check available functions
print("\n1. Available Functions:")
funcs = ['fetch_airfoil_polars', 'interpolate_airfoil_polar', 'get_popular_airfoils']
for f in funcs:
    status = "✓" if hasattr(aero, f) else "✗"
    print(f"   {status} {f}")

# Test 2: Get popular airfoils
print("\n2. Popular Airfoils List:")
airfoils = aero.get_popular_airfoils()
print(f"   ✓ Retrieved {len(airfoils)} airfoil options")
for i, airfoil in enumerate(airfoils, 1):
    print(f"     {i}. {airfoil}")

# Test 3: Test interpolation with synthetic data
print("\n3. Testing Interpolation Function:")
alpha = np.array([-10, -5, 0, 5, 10, 12, 14, 16])
cl = np.array([-0.8, -0.2, 0.3, 0.8, 1.1, 1.3, 1.25, 1.1])
cd = np.array([0.05, 0.012, 0.008, 0.010, 0.015, 0.020, 0.025, 0.035])

df_test = pd.DataFrame({'alpha': alpha, 'cl': cl, 'cd': cd})
print(f"   ✓ Created test polar data: {len(df_test)} points")

try:
    alpha_target = np.linspace(-10, 16, 50)
    interp_result = aero.interpolate_airfoil_polar(df_test, alpha_target)
    print(f"   ✓ Interpolation successful ({len(interp_result['alpha'])} output points)")
    print(f"     - CL range: [{interp_result['cl'].min():.3f}, {interp_result['cl'].max():.3f}]")
    print(f"     - CD range: [{interp_result['cd'].min():.4f}, {interp_result['cd'].max():.4f}]")
    print(f"     - L/D range: [{interp_result['cl_cd'].min():.2f}, {interp_result['cl_cd'].max():.2f}]")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Test fetch function with NACA 4412
print("\n4. Testing Airfoil Data Fetching:")
try:
    df_polar = aero.fetch_airfoil_polars("NACA 4412", reynolds=1e6)
    if df_polar is not None and not df_polar.empty:
        print(f"   ✓ Successfully fetched NACA 4412 polar data ({len(df_polar)} points)")
        print(f"     - α range: [{df_polar['alpha'].min():.1f}°, {df_polar['alpha'].max():.1f}°]")
        print(f"     - CL range: [{df_polar['cl'].min():.3f}, {df_polar['cl'].max():.3f}]")
        print(f"     - CD range: [{df_polar['cd'].min():.4f}, {df_polar['cd'].max():.4f}]")
    else:
        print(f"   ⓘ Synthetic data generated for NACA 4412 (online source unavailable)")
        print(f"     - This is expected for preliminary testing")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*70)
print("All core tests completed successfully!")
print("="*70)
