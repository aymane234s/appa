"""
EcoAero Import & Integration Test Suite
========================================
Validates that all modules load correctly and key functions work as expected.
Run this before launching the Streamlit app.
"""

import sys
import traceback

def test_imports():
    """Test that all core modules can be imported."""
    print("\n" + "=" * 70)
    print("IMPORT VALIDATION TESTS")
    print("=" * 70)
    
    modules_to_test = [
        ("numpy", "NumPy scientific computing"),
        ("streamlit", "Streamlit UI framework"),
        ("plotly.graph_objects", "Plotly visualization"),
        ("pandas", "Pandas data analysis"),
        ("math", "Python math library"),
        ("aerodynamics", "EcoAero aerodynamics backend"),
        ("propulsion_weight", "EcoAero propulsion module"),
        ("utils", "EcoAero utilities"),
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✓ {module_name:<25} - {description}")
        except ImportError as e:
            print(f"✗ {module_name:<25} - FAILED: {str(e)}")
            failed_imports.append((module_name, str(e)))
        except Exception as e:
            print(f"✗ {module_name:<25} - ERROR: {str(e)}")
            failed_imports.append((module_name, str(e)))
    
    return failed_imports


def test_aerodynamics_functions():
    """Test aerodynamics module functions."""
    print("\n" + "=" * 70)
    print("AERODYNAMICS MODULE TESTS")
    print("=" * 70)
    
    try:
        import aerodynamics as aero
        
        # Test 1: Drag polar calculation
        print("\n[TEST 1] Drag Polar Calculation")
        CL = 0.5
        CD0 = 0.025
        AR = 8.0
        e = 0.85
        CD = aero.compute_drag_polar(CL, CD0, AR, e)
        print(f"  CL = {CL}, CD0 = {CD0}, AR = {AR}, e = {e}")
        print(f"  Result: CD = {CD:.5f}")
        assert 0.025 <= CD <= 0.15, f"CD out of physical range: {CD}"
        print(f"  ✓ PASS")
        
        # Test 2: Stability derivatives
        print("\n[TEST 2] Stability Derivatives")
        AR = 8.0
        cm_alpha, a = aero.compute_stability_derivatives(AR)
        print(f"  AR = {AR}")
        print(f"  Result: Cm_α = {cm_alpha:.4f}, Lift Slope = {a:.4f}")
        assert cm_alpha < 0, "Cm_α should be negative (stable)"
        assert a > 0, "Lift curve slope should be positive"
        print(f"  ✓ PASS")
        
        # Test 3: Wing aerodynamics (main function)
        print("\n[TEST 3] Wing Aerodynamics Analysis (estimate_wing_aero)")
        wing_area = 15.0
        span = 12.0
        weight_N = 10000.0
        rho = 1.225
        V = 50.0
        
        result = aero.estimate_wing_aero(wing_area, span, weight_N, rho, V)
        
        print(f"  Inputs: S={wing_area} m², b={span} m, W={weight_N} N, ρ={rho} kg/m³, V={V} m/s")
        print(f"  Results:")
        print(f"    - CL = {result['CL']:.4f}")
        print(f"    - CD = {result['CD']:.5f}")
        print(f"    - Drag = {result['drag_N']:.1f} N")
        print(f"    - AR = {result['AR']:.2f}")
        print(f"    - V_stall = {result['v_stall']:.2f} m/s ({result['v_stall']*3.6:.1f} kph)")
        print(f"    - L/D = {result['LD_ratio']:.2f}")
        
        assert result['CL'] > 0, "CL should be positive"
        assert result['CD'] > 0, "CD should be positive"
        assert result['v_stall'] > 0, "Stall speed should be positive"
        assert result['LD_ratio'] > 0, "L/D should be positive"
        print(f"  ✓ PASS")
        
        # Test 4: Breguet range calculation
        print("\n[TEST 4] Breguet Range Calculation")
        battery_kwh = 60.0
        drag_N = 250.0
        velocity_mps = 50.0
        range_km = aero.compute_breguet_range(battery_kwh, drag_N, velocity_mps)
        
        print(f"  Battery = {battery_kwh} kWh, Drag = {drag_N} N, V = {velocity_mps} m/s")
        print(f"  Result: Range = {range_km:.1f} km")
        assert range_km > 0, "Range should be positive"
        assert range_km < 5000, "Range should be realistic"
        print(f"  ✓ PASS")
        
        return []
        
    except Exception as e:
        print(f"\n✗ ERROR in aerodynamics tests: {str(e)}")
        traceback.print_exc()
        return [("aerodynamics tests", str(e))]


def test_propulsion_functions():
    """Test propulsion and weight module functions."""
    print("\n" + "=" * 70)
    print("PROPULSION & WEIGHT MODULE TESTS")
    print("=" * 70)
    
    try:
        import propulsion_weight as prop
        
        # Test 1: Battery mass
        print("\n[TEST 1] Battery Mass Estimation")
        energy_kwh = 50.0
        mass = prop.battery_mass_kg_from_energy_kwh(energy_kwh, 220.0, 1.15)
        print(f"  Energy = {energy_kwh} kWh @ 220 Wh/kg with 1.15x margin")
        print(f"  Result: Mass = {mass:.1f} kg")
        assert 200 < mass < 350, f"Battery mass out of range: {mass}"
        print(f"  ✓ PASS")
        
        # Test 2: Motor power
        print("\n[TEST 2] Motor Power Requirement")
        thrust_N = 250.0
        speed_mps = 50.0
        efficiency = 0.82
        power = prop.motor_power_kw_from_thrust_N_and_speed_mps(thrust_N, speed_mps, efficiency)
        print(f"  Thrust = {thrust_N} N, Speed = {speed_mps} m/s, η = {efficiency}")
        print(f"  Result: Power = {power:.2f} kW")
        assert 0 < power < 100, f"Power out of range: {power}"
        print(f"  ✓ PASS")
        
        # Test 3: Range calculation
        print("\n[TEST 3] Range Calculation")
        battery = 60.0
        power = 15.0
        speed_kph = 160.0
        range_km = prop.range_km_from_battery_and_power(battery, power, speed_kph)
        print(f"  Battery = {battery} kWh, Power = {power} kW, Speed = {speed_kph} kph")
        print(f"  Result: Range = {range_km:.0f} km")
        assert 100 < range_km < 2000, f"Range out of realistic bounds: {range_km}"
        print(f"  ✓ PASS")
        
        return []
        
    except Exception as e:
        print(f"\n✗ ERROR in propulsion tests: {str(e)}")
        traceback.print_exc()
        return [("propulsion tests", str(e))]


def test_utils_functions():
    """Test utility functions."""
    print("\n" + "=" * 70)
    print("UTILITY FUNCTIONS TESTS")
    print("=" * 70)
    
    try:
        import utils
        
        # Test 1: Speed conversions
        print("\n[TEST 1] Speed Conversions")
        v_mps = 50.0
        v_kph = utils.mps_to_kph(v_mps)
        v_mps_back = utils.kph_to_mps(v_kph)
        print(f"  {v_mps} m/s = {v_kph} kph = {v_mps_back:.1f} m/s")
        assert abs(v_mps - v_mps_back) < 0.01, "Speed conversion failed"
        print(f"  ✓ PASS")
        
        # Test 2: Mass conversions
        print("\n[TEST 2] Mass to Weight Conversions")
        mass_kg = 100.0
        weight_N = utils.kg_to_N(mass_kg)
        mass_back = utils.N_to_kg(weight_N)
        print(f"  {mass_kg} kg = {weight_N:.1f} N = {mass_back:.1f} kg")
        assert abs(mass_kg - mass_back) < 0.01, "Mass conversion failed"
        print(f"  ✓ PASS")
        
        return []
        
    except Exception as e:
        print(f"\n✗ ERROR in utils tests: {str(e)}")
        traceback.print_exc()
        return [("utils tests", str(e))]


def main():
    """Run all tests and generate report."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "EcoAero Integration Test Suite" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Run all test suites
    import_failures = test_imports()
    aero_failures = test_aerodynamics_functions()
    prop_failures = test_propulsion_functions()
    utils_failures = test_utils_functions()
    
    # Aggregate results
    all_failures = import_failures + aero_failures + prop_failures + utils_failures
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    if not all_failures:
        print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
        print("\nThe EcoAero project is ready for deployment!")
        print("Launch the Streamlit app with: streamlit run app.py")
        return 0
    else:
        print(f"\n✗✗✗ {len(all_failures)} TEST(S) FAILED ✗✗✗")
        print("\nFailed tests:")
        for test_name, error in all_failures:
            print(f"  - {test_name}: {error}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
