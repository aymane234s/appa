"""
EcoAero Utility Functions
=========================
Provides unit conversions and helper functions for aircraft design calculations.

Standard Conversions:
  - Speed: m/s ↔ kph (kilometers per hour)
  - Mass: kg ↔ N (Newtons, force)
  - Angle: degrees ↔ radians (via math/numpy)
"""

import numpy as np
import math


# ============================================================================
# SPEED CONVERSIONS
# ============================================================================

def mps_to_kph(v):
    """
    Convert velocity from meters per second to kilometers per hour.
    
    Args:
        v (float): Velocity [m/s]
    
    Returns:
        float: Velocity [kph]
    
    Formula: V_kph = V_mps × 3.6
    
    Examples:
        >>> mps_to_kph(50)  # 50 m/s
        180.0  # kph
    """
    return v * 3.6


def kph_to_mps(v):
    """
    Convert velocity from kilometers per hour to meters per second.
    
    Args:
        v (float): Velocity [kph]
    
    Returns:
        float: Velocity [m/s]
    
    Formula: V_mps = V_kph / 3.6
    
    Examples:
        >>> kph_to_mps(180)  # 180 kph
        50.0  # m/s
    """
    return v / 3.6


# ============================================================================
# WEIGHT & MASS CONVERSIONS
# ============================================================================

def kg_to_N(m):
    """
    Convert mass to weight (force) using standard gravity.
    
    Args:
        m (float): Mass [kg]
    
    Returns:
        float: Weight force [N]
    
    Formula: F = m × g (where g = 9.80665 m/s²)
    
    Notes:
        - Uses standard gravity (9.80665 m/s²)
        - Not accounting for altitude variation
    
    Examples:
        >>> kg_to_N(100)  # 100 kg object
        980.665  # Newtons of force
    """
    GRAVITY_MSS = 9.80665  # Standard gravity [m/s²]
    return m * GRAVITY_MSS


def N_to_kg(N):
    """
    Convert weight (force) to mass using standard gravity.
    
    Args:
        N (float): Weight force [N]
    
    Returns:
        float: Mass [kg]
    
    Formula: m = F / g (where g = 9.80665 m/s²)
    
    Examples:
        >>> N_to_kg(980.665)  # 980.665 Newtons
        100.0  # kg
    """
    GRAVITY_MSS = 9.80665  # Standard gravity [m/s²]
    return N / GRAVITY_MSS


# ============================================================================
# ANGLE CONVERSIONS
# ============================================================================

def deg_to_rad(angle_deg):
    """
    Convert angle from degrees to radians.
    
    Args:
        angle_deg (float): Angle [degrees]
    
    Returns:
        float: Angle [radians]
    """
    return math.radians(angle_deg)


def rad_to_deg(angle_rad):
    """
    Convert angle from radians to degrees.
    
    Args:
        angle_rad (float): Angle [radians]
    
    Returns:
        float: Angle [degrees]
    """
    return math.degrees(angle_rad)
