"""
EcoAero Propulsion & Weight Estimation Module
==============================================
Provides electric motor and battery sizing functions for preliminary aircraft design.

This module encapsulates standard methods for:
  - Battery mass estimation from energy storage requirements
  - Motor power calculation from thrust and speed demands
  - Electric propulsion system sizing and scaling

Standard References:
  - AIAA Aircraft Design Standards
  - Electric Aircraft Performance Handbook
  - Lithium-ion Battery Pack Engineering (Tesla, Panasonic specs)
"""

import math
import numpy as np


def battery_mass_kg_from_energy_kwh(energy_kwh, energy_density_wh_per_kg=200.0, mass_margin=1.15):
    """
    Estimate battery pack mass from required stored energy.
    
    Formula: M_battery = (Energy [Wh] / Energy_Density [Wh/kg]) × Margin_Factor
    
    Args:
        energy_kwh (float): Required energy storage [kWh]
        energy_density_wh_per_kg (float): Cell/pack energy density [Wh/kg], default 200
            - Modern Li-ion cells: 180-260 Wh/kg
            - Typical pack level: 180-220 Wh/kg (accounting for BMS, structure)
            - High-energy packs: 220-260 Wh/kg (at cost of cycle life)
        mass_margin (float): Engineering margin for packaging, BMS, thermal, default 1.15
            - Accounts for battery management system (~5%)
            - Casing and structure (~7%)
            - Thermal management (~3%)
    
    Returns:
        float: Estimated battery pack mass [kg], including all packaging
    
    Examples:
        >>> battery_mass_kg_from_energy_kwh(50, 220, 1.15)  # ~263 kg
        >>> battery_mass_kg_from_energy_kwh(20, 200, 1.15)  # ~115 kg
    """
    if energy_kwh <= 0:
        return 0.0
    
    # Convert kWh to Wh (1 kWh = 1000 Wh)
    energy_wh = energy_kwh * 1000.0
    
    # Base battery mass without margin
    base_mass_kg = energy_wh / energy_density_wh_per_kg
    
    # Apply engineering margin
    total_mass_kg = base_mass_kg * mass_margin
    
    return total_mass_kg


def motor_power_kw_from_thrust_N_and_speed_mps(thrust_N, speed_mps, prop_efficiency=0.7):
    """
    Calculate electrical power required to produce thrust at a given airspeed.
    Accounts for propeller efficiency and motor losses.
    
    Formula: P_shaft = (T × V) / η_propeller
    
    Where:
        T = Thrust required [N]
        V = Airspeed [m/s]
        η_propeller = Propeller figure-of-merit (typical: 0.65-0.85)
    
    Args:
        thrust_N (float): Thrust requirement [N]
        speed_mps (float): Airspeed [m/s]
        prop_efficiency (float): Propeller efficiency [0-1], default 0.7
            - Slow-speed propeller (80-120 rpm): 0.65-0.75 (high blade loading)
            - Optimal cruise propeller (1000-2000 rpm): 0.78-0.88
            - High-speed propeller (3000+ rpm): 0.60-0.70 (tip losses dominate)
    
    Returns:
        float: Shaft power requirement [kW]
    
    Notes:
        - At hover/static (V=0), function assumes minimal hover speed
        - Motor efficiency not included (assumption: motor ≈95% efficient)
        - Does not account for climb, maneuvering, or reserve power
    
    Examples:
        >>> motor_power_kw_from_thrust_N_and_speed_mps(500, 40, 0.82)  # ≈24.4 kW
        >>> motor_power_kw_from_thrust_N_and_speed_mps(200, 60, 0.80)  # ≈15 kW
    """
    # Handle zero or near-zero speed (hover condition)
    if speed_mps <= 0:
        # Use disk loading approximation for hover (beyond scope for fixed-wing)
        speed_mps = 1.0  # Approximate very slow speed
    
    # Power = Thrust × Velocity / Efficiency
    power_watts = (thrust_N * speed_mps) / prop_efficiency
    
    # Convert watts to kilowatts
    power_kw = power_watts / 1000.0
    
    return power_kw


def energy_required_kwh(power_kw, time_hours):
    """
    Calculate total energy consumed during a flight segment.
    
    Formula: E = P × t
    
    Args:
        power_kw (float): Average power consumption [kW]
        time_hours (float): Duration of flight segment [hours]
    
    Returns:
        float: Total energy consumed [kWh]
    
    Notes:
        - Assumes constant power (conservative, does not account for descent efficiency)
        - Does not include climbing or battery voltage sag effects
    """
    return power_kw * time_hours


def range_km_from_battery_and_power(battery_kwh, cruise_power_kw, cruise_speed_kph):
    """
    Calculate maximum range from battery capacity and cruise power requirement.
    
    Formula: Range = (Energy / Power) × Cruise_Speed = Endurance × Cruise_Speed
    
    Args:
        battery_kwh (float): Usable battery energy [kWh]
        cruise_power_kw (float): Cruise electrical power [kW]
        cruise_speed_kph (float): Cruise airspeed [kph]
    
    Returns:
        float: Maximum range [km]
    
    Notes:
        - Does not account for reserve fuel (typical: 5-10% of battery energy)
        - Assumes constant speed and altitude
        - Descent is assumed to be gliding (zero power)
    """
    if cruise_power_kw <= 0:
        return 0.0
    
    # Calculate endurance in hours
    endurance_hours = battery_kwh / cruise_power_kw
    
    # Calculate range: Distance = Speed × Time
    range_km = endurance_hours * cruise_speed_kph
    
    return range_km


# ============================================================================
# SMOKE TESTS (Run if executed as main module)
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EcoAero Propulsion & Weight Module - Smoke Tests")
    print("=" * 60)
    
    # Test 1: Battery mass calculation
    mass_batt = battery_mass_kg_from_energy_kwh(20, 200)
    print(f"\n[TEST 1] Battery Mass (20 kWh @ 200 Wh/kg):")
    print(f"  Result: {mass_batt:.1f} kg")
    assert 100 < mass_batt < 150, "Battery mass out of range!"
    
    # Test 2: Motor power calculation
    power_req = motor_power_kw_from_thrust_N_and_speed_mps(200, 40)
    print(f"\n[TEST 2] Motor Power (200 N @ 40 m/s, η=0.7):")
    print(f"  Result: {power_req:.1f} kW")
    assert 10 < power_req < 15, "Power calculation out of range!"
    
    # Test 3: Range calculation
    rng = range_km_from_battery_and_power(60, 15, 160)
    print(f"\n[TEST 3] Range (60 kWh battery, 15 kW cruise, 160 kph):")
    print(f"  Result: {rng:.0f} km")
    assert 500 < rng < 1000, "Range out of realistic bounds!"
    
    print("\n" + "=" * 60)
    print("✓ All smoke tests passed!")
    print("=" * 60)
