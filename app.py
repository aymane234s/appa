import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math
import streamlit.components.v1 as components  # Required library to execute ad scripts

# Import backend physics and performance modules
import aerodynamics as aero
import propulsion_weight as prop

# ============================================================================
# 1. PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Eco Aero Designer Pro", 
    layout="wide"
)

# ============================================================================
# 2. NAVIGATION SIDEBAR & GLOBAL INPUTS
# ============================================================================
st.sidebar.title("Eco Aero Pro")
st.sidebar.markdown("**Industrial-Grade Aircraft Design & Analysis Suite**")
st.sidebar.markdown("*Preliminary design for electric aviation*")

page = st.sidebar.radio("Analysis Modules:", [
    "Vehicle Overview & KPIs", 
    "3D Aerodynamics & Stall Analysis", 
    "Weight, Balance & Stability",
    "Parametric Trade Studies",
    "Airfoil Explorer"
])
st.sidebar.markdown("---")

# Geometric inputs
st.sidebar.header("Aircraft Configuration")
wing_span = st.sidebar.number_input("Wing Span (b) [m]", min_value=2.0, max_value=30.0, value=12.0, step=0.1, format="%.2f")
wing_chord = st.sidebar.number_input("Mean Wing Chord (c̄) [m]", min_value=0.5, max_value=5.0, value=1.20, step=0.01, format="%.2f")

# Energy & payload
battery_energy_kwh = st.sidebar.number_input("Battery Capacity [kWh]", min_value=5.0, max_value=500.0, value=60.0, step=1.0, format="%.1f")
payload_mass = st.sidebar.number_input("Payload Mass [kg]", min_value=10.0, max_value=1000.0, value=160.0, step=5.0)

# Mission profile
st.sidebar.subheader("Mission Parameters")
cruise_speed_kph = st.sidebar.slider("Cruise Velocity [kph]", 60, 350, 160, 5)
altitude = st.sidebar.slider("Flight Altitude [m]", 0, 5000, 1200, 100)

# Aerodynamic parameters
st.sidebar.subheader("Aerodynamic Inputs")
cd0_input = st.sidebar.number_input("Zero-Lift Drag Coefficient (CD₀)", min_value=0.010, max_value=0.100, value=0.025, step=0.001, format="%.4f")
oswald_e = st.sidebar.number_input("Oswald Efficiency Factor (e)", min_value=0.60, max_value=0.98, value=0.85, step=0.01, format="%.3f")


# ============================================================================
# 3. ADVERTISEMENT SECTION (Lambda Project Monetization)
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📢 Sponsored Content")

with st.sidebar:
    # 1. Existing Popunder (Runs smoothly in the background)
    components.iframe("https://pl30099321.effectivecpmnetwork.com/db/4b/92/db4b92383ddc97608da999887f5fd381.js", height=0, width=0)

    # 2. Existing Banner Ad (468x60)
    banner_code = """
    <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
        <script type="text/javascript">
            atOptions = {
                'key' : '478176cd425efa7b2c40f8b6c31ea1e5',
                'format' : 'iframe',
                'height' : 60,
                'width' : 468,
                'params' : {}
            };
        </script>
        <script type="text/javascript" src="https://www.highperformanceformat.com/478176cd425efa7b2c40f8b6c31ea1e5/invoke.js"></script>
    </div>
    """
    components.html(banner_code, height=70, scrolling=False)

    st.sidebar.markdown("---")

    # 3. New Popunder_1 (Triggers safely on user background interaction)
    popunder_new_code = """
    <script src="https://pl30100251.effectivecpmnetwork.com/50/b1/01/50b1013f5362b39056aaed2284f122fe.js"></script>
    """
    components.html(popunder_new_code, height=0, width=0)

    # 4. New SocialBar_1 (Displays high-CTR clean user alerts)
    social_bar_code = """
    <script src="https://pl30100642.effectivecpmnetwork.com/98/ca/03/98ca03a3ae896845dea1a2f66cb410dd.js"></script>
    """
    components.html(social_bar_code, height=0, width=0)

    # 5. New Smart Link (Clean Call-to-Action button to optimize monetization)
    st.info("💡 Recommended Links:")
    st.link_button("🔥 Check Exclusive Offers", "https://www.effectivecpmnetwork.com/cp1j54cb2m?key=771fb76a7a71ee82219c877ea51948bb")


# 6. New Native Banner_1 (Placed at the bottom of the main content area for maximum cross-device layout compatibility)
st.markdown("---")
native_banner_code = """
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; margin-top: 20px;">
    <p style="font-size: 11px; color: #888888; margin-bottom: 5px; font-family: sans-serif;">Sponsored Content</p>
    <script async="async" data-cfasync="false" src="https://pl30100640.effectivecpmnetwork.com/8569141da3e4adc87c040aa92f6807cc/invoke.js"></script>
    <div id="container-8569141da3e4adc87c040aa92f6807cc"></div>
</div>
"""
components.html(native_banner_code, height=200, scrolling=True)
# ============================================================================
# 4. GLOBAL CORE CALCULATIONS
# ============================================================================

# Geometric calculations
wing_area = wing_span * wing_chord  # Simplified: assume rectangular planform
aspect_ratio = (wing_span ** 2) / wing_area

# Unit conversions
cruise_speed_mps = cruise_speed_kph / 3.6

# ISA Atmosphere model (troposphere)
# ρ = ρ₀ × (1 - Λ×h)^4.256 where Λ = 0.0065 K/m, h in meters
temperature_offset = 2.25577e-5  # Coefficient for ISA model
rho = 1.225 * ((1 - temperature_offset * altitude) ** 4.25588)  # Air density [kg/m³]

# ============================================================================
# 5. MASS & WEIGHT ESTIMATION
# ============================================================================

# Battery mass sizing
energy_density_wh_kg = 220.0  # Typical modern Li-ion pack level [Wh/kg]
mass_margin_factor = 1.15  # 15% margin for BMS, casing, connectors
calculated_battery_mass = prop.battery_mass_kg_from_energy_kwh(battery_energy_kwh, energy_density_wh_kg, mass_margin_factor)

# Structure mass (composite construction estimate)
# Typical: 12-18 kg/m² for electric aircraft composite wing + fuselage
structure_mass_specific = 14.5  # kg/m² of wing area
structural_mass = wing_area * structure_mass_specific
# GLOBAL CORE CALCULATIONS
# ============================================================================

# Geometric calculations
wing_area = wing_span * wing_chord  # Simplified: assume rectangular planform
aspect_ratio = (wing_span ** 2) / wing_area

# Unit conversions
cruise_speed_mps = cruise_speed_kph / 3.6

# ISA Atmosphere model (troposphere)
# ρ = ρ₀ × (1 - Λ×h)^4.256 where Λ = 0.0065 K/m, h in meters
temperature_offset = 2.25577e-5  # Coefficient for ISA model
rho = 1.225 * ((1 - temperature_offset * altitude) ** 4.25588)  # Air density [kg/m³]

# ============================================================================
# MASS & WEIGHT ESTIMATION
# ============================================================================

# Battery mass sizing
energy_density_wh_kg = 220.0  # Typical modern Li-ion pack level [Wh/kg]
mass_margin_factor = 1.15  # 15% margin for BMS, casing, connectors
calculated_battery_mass = prop.battery_mass_kg_from_energy_kwh(battery_energy_kwh, energy_density_wh_kg, mass_margin_factor)

# Structure mass (composite construction estimate)
# Typical: 12-18 kg/m² for electric aircraft composite wing + fuselage
structure_mass_specific = 14.5  # kg/m² of wing area
structural_mass = wing_area * structure_mass_specific

# Propulsion system mass (motor + inverter + cooling)
# Typical scaling: ~35 kg base + 0.2 kg per kWh of battery
propulsion_mass = 35.0 + (battery_energy_kwh * 0.2)

# Total mass breakdown
empty_mass = calculated_battery_mass + structural_mass + propulsion_mass
total_mass = empty_mass + payload_mass
total_weight_N = total_mass * 9.81  # Convert to Newtons [N]

# ============================================================================
# AERODYNAMIC ANALYSIS - CALL BACKEND
# ============================================================================

# FIX: Call estimate_wing_aero with correct parameters (NO aspect_ratio parameter)
# The function computes AR internally from wing_area and span
aero_results = aero.estimate_wing_aero(
    wing_area_m2=wing_area,
    span_m=wing_span,
    weight_N=total_weight_N,
    rho=rho,
    V=cruise_speed_mps,
    CD0=cd0_input,
    e=oswald_e
)

cl_required = aero_results["CL"]
cd_total = aero_results["CD"]
drag_force_N = aero_results["drag_N"]
v_stall_mps = aero_results["v_stall"]

# ============================================================================
# PROPULSION & PERFORMANCE ANALYSIS
# ============================================================================

# Propeller/motor efficiency (depends on design point and operating condition)
prop_efficiency = 0.82  # High-efficiency propeller design
thrust_required_N = drag_force_N  # Thrust = Drag in level cruise

# Shaft power required: P = (Thrust × Velocity) / Efficiency
required_shaft_power_kw = prop.motor_power_kw_from_thrust_N_and_speed_mps(
    thrust_required_N, cruise_speed_mps, prop_efficiency
)

# Flight endurance (hours of flight at cruise conditions)
flight_endurance_hours = battery_energy_kwh / required_shaft_power_kw if required_shaft_power_kw > 0 else 0.0

# Maximum range (distance traveled at cruise speed)
max_range_km = flight_endurance_hours * cruise_speed_kph

# ============================================================================
# MODULE 1: VEHICLE OVERVIEW & KEY PERFORMANCE INDICATORS
# ============================================================================

if page == "Vehicle Overview & KPIs":
    st.title("Eco Aero - Aircraft Configuration & Key Performance Indicators")
    st.markdown("**Master design summary with synthesized structural and aerodynamic profiles.**")
    st.markdown("---")
    col3, col4 = st.columns(2)
    col3.metric("Mission Endurance", f"{flight_endurance_hours:.2f} hrs", delta=f"Reserve: TBD")
    col4.metric("Maximum Range", f"{max_range_km:.1f} km", delta=f"@{cruise_speed_kph} kph")
    
    st.markdown("---")
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.subheader("Mass Breakdown (Subsystem Distribution)")
        components = ["Battery Pack", "Airframe Structure", "Propulsion System", "Payload"]
        masses = [calculated_battery_mass, structural_mass, propulsion_mass, payload_mass]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=components, 
            values=masses, 
            hole=0.4,
            marker=dict(colors=['#1f77b4', '#aec7e8', '#ff7f0e', '#2ca02c']),
            textinfo="label+percent"
        )])
        fig_pie.update_layout(
            margin=dict(t=20, b=20, l=20, r=20),
            height=350,
            template="plotly_white"
        )
        st.plotly_chart(fig_pie, width='stretch')
        
    with col_b:
        st.subheader("Propulsion Analysis")
        st.write(f"**Cruise Drag:** {drag_force_N:.1f} N")
        st.write(f"**Required Power:** {required_shaft_power_kw:.2f} kW")
        st.write(f"**Power Density:** {required_shaft_power_kw/total_mass:.2f} kW/kg")
        st.write(f"**Efficiency Factor:** {prop_efficiency:.1%}")
        if required_shaft_power_kw > 0:
            st.write(f"**Energy Reserve:** {battery_energy_kwh/required_shaft_power_kw/1.2:.1f}x")


# ============================================================================
# MODULE 2: AERODYNAMIC ANALYSIS & FLIGHT ENVELOPE
# ============================================================================

elif page == "3D Aerodynamics & Stall Analysis":
    st.title("High-Fidelity Aerodynamic & Flight Envelope Analysis")
    st.markdown("---")
    
    # Stall speed
    v_stall_kph = v_stall_mps * 3.6
    ld_ratio = aero_results["LD_ratio"]
    cm_alpha = aero_results["cm_alpha"]
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Stall Speed (V_stall)", f"{v_stall_kph:.1f} kph", 
                  delta=f"{v_stall_mps:.1f} m/s")
    col_m2.metric("Cruise Lift Coefficient", f"{cl_required:.4f}",
                  delta=f"CD = {cd_total:.4f}")
    col_m3.metric("Lift-to-Drag Ratio (L/D)", f"{ld_ratio:.2f}",
                  delta=f"Efficiency measure")
    
    # SAFETY CHECK: Flight envelope validation
    safety_margin = cruise_speed_kph / v_stall_kph if v_stall_kph > 0 else 0
    st.markdown("---")
    st.subheader("Flight Envelope Validation")
    
    if cruise_speed_kph < v_stall_kph:
        st.error(f"🚨 **CRITICAL VIOLATION:** Cruise speed ({cruise_speed_kph} kph) < Stall Speed ({v_stall_kph:.1f} kph)!")
        st.error("**ACTION REQUIRED:** Increase wing span, reduce payload, or select higher cruise speed.")
    elif safety_margin < 1.2:
        st.warning(f"⚠️ **MARGINAL:** Safety margin is only {safety_margin:.2f}x (recommend ≥1.3x)")
    else:
        st.success(f"✓ **SAFE:** Speed margin = {safety_margin:.2f}x above stall (cruise/V_stall)")
    
    # Lift curve prediction
    st.markdown("---")
    st.subheader("Lift Curve & Stall Prediction (CL vs. Angle-of-Attack)")
    
    alphas = np.linspace(-6, 16, 50)
    # Simplified lift curve: CL = a × α (linear until stall)
    cl_max = 1.4  # Clean NACA 4-digit section
    lift_curve_slope_deg = aero_results["lift_curve_slope"] * (180/np.pi)  # Convert to 1/deg
    cl_sweep = cl_required + lift_curve_slope_deg * alphas  # Shifted for cruise CL
    
    # Truncate at stall (post-stall not modeled)
    cl_sweep = np.where(cl_sweep > cl_max, cl_max, cl_sweep)
    
    fig_env = go.Figure()
    fig_env.add_trace(go.Scatter(
        x=alphas, y=cl_sweep,
        mode='lines+markers',
        name='Lift Curve',
        line=dict(color='#d62728', width=3),
        marker=dict(size=4)
    ))
    
    # Stall angle annotation
    stall_angle = 12.0  # Typical clean section
    fig_env.add_vline(x=stall_angle, line_dash="dash", line_color="orange",
                      annotation_text=f"Stall ≈ {stall_angle}°")
    
    # Current operating point
    fig_env.add_hline(y=cl_required, line_dash="dot", line_color="green",
                      annotation_text=f"Cruise CL = {cl_required:.3f}")
    
    fig_env.update_xaxes(title_text="Angle of Attack α [degrees]")
    fig_env.update_yaxes(title_text="Lift Coefficient CL [-]")
    fig_env.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_env, width='stretch')


# ============================================================================
# MODULE 3: WEIGHT, BALANCE & LONGITUDINAL STABILITY
# ============================================================================

elif page == "Weight, Balance & Stability":
    st.title("Center of Gravity (CG) Tracking & Longitudinal Stability Analysis")
    st.markdown("---")
    
    st.subheader("CG Position Matrix (% Mean Aerodynamic Chord)")
    
    # Aerodynamic Center (typical location for low-speed flight)
    x_ac_percent_mac = 25.0  # 25% MAC is standard for subsonic wings
    
    # User controls for CG location of major components
    cg_battery_mac = st.slider(
        "Battery CG Location (% MAC)", 10.0, 80.0, 20.0,
        help="Longitudinal position of battery pack relative to wing leading edge"
    )
    cg_payload_mac = st.slider(
        "Payload CG Location (% MAC)", 15.0, 90.0, 35.0,
        help="Longitudinal position of payload relative to wing leading edge"
    )
    
    # Composite CG calculation (mass-weighted average)
    numerator = (calculated_battery_mass * cg_battery_mac + 
                 payload_mass * cg_payload_mac + 
                 structural_mass * 40.0)  # Assume structure at 40% MAC
    calculated_cg_x = numerator / total_mass
    
    # Static Margin (% MAC)
    # Positive static margin = stable (CG ahead of AC)
    # Neutral: SM = 0, Unstable: SM < 0
    static_margin_percent = x_ac_percent_mac - calculated_cg_x
    
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Calculated CG Position", f"{calculated_cg_x:.2f}% MAC")
    col_s2.metric("Aerodynamic Center (AC)", f"{x_ac_percent_mac:.2f}% MAC")
    col_s3.metric("Static Margin (SM)", f"{static_margin_percent:.2f}% MAC")
    
    st.markdown("---")
    st.subheader("Stability Assessment")
    
    # Stability criteria per design standards
    if static_margin_percent > 5.0:
        st.success("✓ **STABLE:** Aircraft will naturally return to cruise equilibrium after perturbation.")
        st.write(f"Static margin of {static_margin_percent:.2f}% is within acceptable range (3-7% for transport)")
        
    elif static_margin_percent >= 0:
        st.warning("⚠️ **NEUTRAL/MARGINAL:** Aircraft possesses minimal pitch restoring moment.")
        st.write("Automatic trim system required; sensitive to loading changes.")
        
    else:
        st.error("❌ **UNSTABLE:** Aircraft is statically unstable (CG behind AC).")
        st.error("This configuration will experience divergent pitch motion. Reposition CG forward immediately.")
    
    # Pitching moment stability derivative
    cm_alpha_val = aero_results["cm_alpha"]
    st.write(f"**Cm_α (Pitch Stability Derivative):** {cm_alpha_val:.4f} [1/rad]")
    st.caption("*Negative Cm_α indicates stable configuration (standard)*")


# ============================================================================
# MODULE 4: PARAMETRIC TRADE STUDIES & SENSITIVITY
# ============================================================================

elif page == "Parametric Trade Studies":
    st.title("Multi-Variable Trade Studies (Sensitivity Analysis)")
    st.markdown("Analyze how independent parameters affect Range and Gross Weight.")
    st.markdown("---")
    
    sweep_param = st.selectbox("Select Sweep Parameter:", 
                               ["Wing Span", "Battery Capacity"])
    
    # Define sweep ranges
    if sweep_param == "Wing Span":
        sweep_range = np.linspace(5.0, 25.0, 20)
        xlabel = "Wing Span [m]"
    else:
        sweep_range = np.linspace(20.0, 200.0, 20)
        xlabel = "Battery Capacity [kWh]"
    
    sweep_ranges_km = []
    sweep_weights_kg = []
    
    # Parametric sweep calculation
    for val in sweep_range:
        if sweep_param == "Wing Span":
            # Vary wing span, keep chord constant
            local_s = val * wing_chord
            local_wn = total_weight_N  # Weight unchanged
            res = aero.estimate_wing_aero(local_s, val, local_wn, rho, cruise_speed_mps, cd0_input, oswald_e)
            local_tm = total_mass  # Mass unchanged
            
        else:  # Battery Capacity sweep
            # Vary battery, which affects mass
            local_bm = prop.battery_mass_kg_from_energy_kwh(val, 220.0, 1.15)
            delta_mass = local_bm - calculated_battery_mass
            local_tm = total_mass + delta_mass
            local_wn = local_tm * 9.81
            res = aero.estimate_wing_aero(wing_area, wing_span, local_wn, rho, cruise_speed_mps, cd0_input, oswald_e)
            
        # Performance calculation
        l_drag = res["drag_N"]
        l_power = prop.motor_power_kw_from_thrust_N_and_speed_mps(l_drag, cruise_speed_mps, prop_efficiency)
        
        if l_power > 0:
            if sweep_param == "Battery Capacity":
                l_end = val / l_power
            else:
                l_end = battery_energy_kwh / l_power
            sweep_ranges_km.append(l_end * cruise_speed_kph)
        else:
            sweep_ranges_km.append(0.0)
            
        sweep_weights_kg.append(local_tm)
    
    # Dual-axis plot
    fig_trade = go.Figure()
    fig_trade.add_trace(go.Scatter(
        x=sweep_range, y=sweep_ranges_km,
        name="Max Range (km)",
        yaxis="y1",
        line=dict(color="#1f77b4", width=3),
        mode='lines+markers'
    ))
    fig_trade.add_trace(go.Scatter(
        x=sweep_range, y=sweep_weights_kg,
        name="Gross Mass (kg)",
        yaxis="y2",
        line=dict(color="#d62728", width=3, dash="dash"),
        mode='lines+markers'
    ))
    
    fig_trade.update_layout(
        title=f"Parametric Sweep: {sweep_param} Impact on Range & Weight",
        xaxis=dict(title=xlabel),
        yaxis=dict(
            title=dict(text="Maximum Range [km]", font=dict(color="#1f77b4")),
            tickfont=dict(color="#1f77b4")
        ),
        yaxis2=dict(
            title=dict(text="Gross Mass [kg]", font=dict(color="#d62728")),
            tickfont=dict(color="#d62728"),
            overlaying="y",
            side="right"
        ),
        template="plotly_white",
        hovermode="x unified",
        height=500
    )
    
    st.plotly_chart(fig_trade, width='stretch')
    
    # Sensitivity metrics
    st.markdown("---")
    st.subheader("Sensitivity Metrics")
    
    range_delta = sweep_ranges_km[-1] - sweep_ranges_km[0]
    param_delta = sweep_range[-1] - sweep_range[0]
    sensitivity = range_delta / param_delta if param_delta > 0 else 0
    
    col_sen1, col_sen2 = st.columns(2)
    col_sen1.metric("Range Sensitivity", f"{sensitivity:.2f} km per unit {sweep_param}")
    col_sen2.metric("Weight Sensitivity", f"{(sweep_weights_kg[-1]-sweep_weights_kg[0])/param_delta:.2f} kg per unit {sweep_param}")


# ============================================================================
# MODULE 5: AIRFOIL EXPLORER & ANALYSIS
# ============================================================================

elif page == "Airfoil Explorer":
    st.title("Interactive Airfoil Analysis & Aerodynamic Curves")
    st.markdown("Explore lift and drag characteristics of popular electric aircraft airfoils.")
    st.markdown("---")
    
    # Get list of popular airfoils
    airfoil_list = aero.get_popular_airfoils()
    
    # Airfoil selection
    col_sel1, col_sel2 = st.columns([2, 1])
    with col_sel1:
        selected_airfoil = st.selectbox(
            "Select Airfoil Profile",
            options=airfoil_list,
            index=0,
            help="Popular airfoils for electric aircraft preliminary design"
        )
    
    with col_sel2:
        reynolds_number = st.number_input(
            "Reynolds Number",
            value=1e6,
            format="%.0e",
            help="Typical range: 0.3M - 5M for electric aircraft"
        )
        enable_xfoil = st.checkbox("Enable XFOIL (if installed)", value=True)
        enable_asb = st.checkbox("Enable AeroSandbox (if installed)", value=False)
    
    st.markdown("---")
    
    # Fetch airfoil data (multi-source comparison)
    with st.spinner(f"🔄 Fetching polar data for {selected_airfoil}..."):
        try:
            coords = aero.fetch_airfoil_data(selected_airfoil)

            # Show airfoil coordinates if available
            if coords is not None and not coords.empty:
                st.subheader('Airfoil Coordinates')
                fig_coords = go.Figure()
                fig_coords.add_trace(go.Scatter(x=coords['x'], y=coords['y'], mode='lines', name='Airfoil'))
                fig_coords.update_layout(title=f"Airfoil: {selected_airfoil}", yaxis=dict(scaleanchor='x', scaleratio=1), height=300, template='plotly_white')
                st.plotly_chart(fig_coords, width='stretch')
            results = {}

            # Try XFOIL/fetch if enabled
            if enable_xfoil:
                try:
                    df_x = aero.fetch_airfoil_polars(selected_airfoil, reynolds=reynolds_number)
                    if df_x is not None and not df_x.empty:
                        results['XFOIL'] = df_x
                except Exception:
                    pass

            # Synthetic archive
            try:
                df_syn = aero._fetch_from_naca_archive(selected_airfoil, reynolds_number)
                if df_syn is not None and not df_syn.empty:
                    results['Synthetic'] = df_syn
            except Exception:
                pass

            # AeroSandbox
            if enable_asb:
                try:
                    df_asb = aero.run_aerosandbox_polar(coords if coords is not None else df_syn, reynolds_number, np.arange(-12, 16+1e-6, 1.0))
                    if df_asb is not None and not df_asb.empty:
                        results['AeroSandbox'] = df_asb
                except Exception:
                    pass

            # If nothing found, attempt a final generic fetch
            if not results:
                df_fallback = aero.fetch_airfoil_polars(selected_airfoil, reynolds=reynolds_number)
                if df_fallback is not None and not df_fallback.empty:
                    results['Fallback'] = df_fallback

            if not results:
                st.warning(f"⚠️ No polar data available for {selected_airfoil} at Re = {reynolds_number:.2e}")
                st.info("Try enabling different sources (XFOIL/AeroSandbox) or check XFOIL installation.")
            else:
                # Build comparison plots
                alpha_target = np.arange(-12, 16 + 1e-6, 1.0)
                fig_cl = go.Figure()
                fig_cd = go.Figure()
                fig_ld = go.Figure()
                table_rows = []

                for label, df_src in results.items():
                    try:
                        interp = aero.interpolate_airfoil_polar(df_src, alpha_target)
                        fig_cl.add_trace(go.Scatter(x=interp['alpha'], y=interp['cl'], mode='lines', name=label))
                        fig_cd.add_trace(go.Scatter(x=interp['alpha'], y=interp['cd'], mode='lines', name=label))
                        fig_ld.add_trace(go.Scatter(x=interp['alpha'], y=interp['cl_cd'], mode='lines', name=label))

                        mid = len(interp['alpha']) // 2
                        table_rows.append({'source': label, 'alpha_mid': interp['alpha'][mid], 'cl_mid': float(interp['cl'][mid]), 'cd_mid': float(interp['cd'][mid]), 'ld_mid': float(interp['cl_cd'][mid])})
                    except Exception:
                        continue

                fig_cl.update_layout(title='CL vs Alpha (comparison)', xaxis_title='Alpha [deg]', yaxis_title='CL', template='plotly_white')
                fig_cd.update_layout(title='CD vs Alpha (comparison)', xaxis_title='Alpha [deg]', yaxis_title='CD', template='plotly_white')
                fig_ld.update_layout(title='L/D vs Alpha (comparison)', xaxis_title='Alpha [deg]', yaxis_title='L/D', template='plotly_white')

                st.plotly_chart(fig_cl, width='stretch')
                st.plotly_chart(fig_cd, width='stretch')
                st.plotly_chart(fig_ld, width='stretch')

                if table_rows:
                    df_table = pd.DataFrame(table_rows)
                    st.subheader('Summary (mid alpha sample)')
                    st.table(df_table)

                # Combined CSV
                agg_rows = []
                for label, df_src in results.items():
                    try:
                        interp = aero.interpolate_airfoil_polar(df_src, alpha_target)
                        for a, clv, cdv, ldv in zip(interp['alpha'], interp['cl'], interp['cd'], interp['cl_cd']):
                            agg_rows.append({'source': label, 'alpha': a, 'cl': float(clv), 'cd': float(cdv), 'cl_cd': float(ldv)})
                    except Exception:
                        continue

                if agg_rows:
                    df_out = pd.DataFrame(agg_rows)
                    csv = df_out.to_csv(index=False).encode('utf-8')
                    st.download_button('Download combined CSV', data=csv, file_name=f'{selected_airfoil.replace(" ","_")}_polars_all.csv')

                # Detailed single-source analysis controls
                st.markdown('---')
                src_keys = list(results.keys())
                chosen_source = st.selectbox('Select source for detailed plots:', src_keys, index=0)
                df_src = results.get(chosen_source)
                if df_src is not None and not df_src.empty:
                    alpha_target_fine = np.linspace(np.min(df_src['alpha']), np.max(df_src['alpha']), 200)
                    interp = aero.interpolate_airfoil_polar(df_src, alpha_target_fine)

                    # Single-source plots
                    fig_cl_single = go.Figure()
                    fig_cl_single.add_trace(go.Scatter(x=interp['alpha'], y=interp['cl'], mode='lines', name='CL'))
                    fig_cl_single.update_layout(title=f'CL vs Alpha — {chosen_source}', xaxis_title='Alpha [deg]', yaxis_title='CL', template='plotly_white')

                    fig_cd_single = go.Figure()
                    fig_cd_single.add_trace(go.Scatter(x=interp['alpha'], y=interp['cd'], mode='lines', name='CD', line=dict(color='#d62728')))
                    fig_cd_single.update_layout(title=f'CD vs Alpha — {chosen_source}', xaxis_title='Alpha [deg]', yaxis_title='CD', template='plotly_white')

                    fig_polar_single = go.Figure()
                    fig_polar_single.add_trace(go.Scatter(x=interp['cd'], y=interp['cl'], mode='lines+markers', name='Polar', line=dict(color='#2ca02c')))
                    fig_polar_single.update_layout(title=f'CL vs CD (Polar) — {chosen_source}', xaxis_title='CD', yaxis_title='CL', template='plotly_white')

                    # L/D vs CL
                    ld = np.array(interp['cl']) / np.maximum(np.array(interp['cd']), 1e-6)
                    fig_ld_cl = go.Figure()
                    fig_ld_cl.add_trace(go.Scatter(x=interp['cl'], y=ld, mode='lines', name='L/D vs CL'))
                    fig_ld_cl.update_layout(title=f'L/D vs CL — {chosen_source}', xaxis_title='CL', yaxis_title='L/D', template='plotly_white')

                    # CD vs L/D
                    fig_cd_ld = go.Figure()
                    fig_cd_ld.add_trace(go.Scatter(x=ld, y=interp['cd'], mode='lines', name='CD vs L/D', line=dict(color='#9467bd')))
                    fig_cd_ld.update_layout(title=f'CD vs L/D — {chosen_source}', xaxis_title='L/D', yaxis_title='CD', template='plotly_white')

                    # Cm vs Alpha if available
                    if 'cm' in df_src.columns:
                        try:
                            spline_cm = None
                            cm_series = df_src['cm'].values
                            if not np.all(np.isnan(cm_series)):
                                interp_cm = np.interp(alpha_target_fine, df_src['alpha'].values, cm_series)
                                fig_cm = go.Figure()
                                fig_cm.add_trace(go.Scatter(x=alpha_target_fine, y=interp_cm, mode='lines', name='Cm'))
                                fig_cm.update_layout(title=f'Cm vs Alpha — {chosen_source}', xaxis_title='Alpha [deg]', yaxis_title='Cm', template='plotly_white')
                                show_cm = True
                            else:
                                show_cm = False
                        except Exception:
                            show_cm = False
                    else:
                        show_cm = False

                    # Display arranged plots
                    st.plotly_chart(fig_cl_single, width='stretch')
                    st.plotly_chart(fig_cd_single, width='stretch')
                    st.plotly_chart(fig_polar_single, width='stretch')
                    st.plotly_chart(fig_ld_cl, width='stretch')
                    st.plotly_chart(fig_cd_ld, width='stretch')
                    if show_cm:
                        st.plotly_chart(fig_cm, width='stretch')

                    # Cp distribution (requires XFOIL)
                    if enable_xfoil:
                        st.markdown('---')
                        st.subheader('Cp Distribution (requires XFOIL)')
                        alpha_cp = st.slider('Select alpha for Cp [deg]', float(np.min(df_src['alpha'])), float(np.max(df_src['alpha'])), float(alpha_target_fine[len(alpha_target_fine)//2]))
                        if st.button('Compute Cp (XFOIL)'):
                            with st.spinner('Running XFOIL to compute Cp...'):
                                # Try coords from fetch or generate from NACA
                                cp_coords = coords
                                if (cp_coords is None or cp_coords.empty) and 'NACA' in selected_airfoil.upper():
                                    try:
                                        cp_coords = aero._generate_naca_coords(selected_airfoil)
                                    except Exception:
                                        cp_coords = None

                                if cp_coords is not None and not cp_coords.empty:
                                    cp_df = aero._run_xfoil_cp(cp_coords, reynolds_number, alpha_cp)
                                    if cp_df is not None and not cp_df.empty:
                                        fig_cp = go.Figure()
                                        fig_cp.add_trace(go.Scatter(x=cp_df['x'], y=cp_df['cp'], mode='lines', name=f'Cp @ {alpha_cp}°'))
                                        fig_cp.update_layout(title=f'Pressure Coefficient Cp — {selected_airfoil} @ {alpha_cp}°', xaxis_title='x/c', yaxis_title='Cp', yaxis=dict(autorange='reversed'), template='plotly_white', height=400)
                                        st.plotly_chart(fig_cp, width='stretch')
                                    else:
                                        st.error('Cp computation failed or XFOIL did not produce Cp file.')
                                else:
                                    st.error('No coordinates available to run XFOIL for Cp.')

        except Exception as e:
            st.error(f"❌ Error loading airfoil data: {str(e)}")
            st.info("Ensure internet connection is available for online database access.")
