"""
Module 1: Transistor Switching Simulation.
Provides interactive exploration of transistor switching dynamics with:
- Synchronized sliders and manual numeric inputs
- Dynamic circuit schematics (SVG)
- Physics engine (Cutoff, Active, Saturation)
- Voltage Transfer Characteristic (VTC) curve and DC Load Line plots
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils.svg_generator import generate_transistor_circuit_svg, render_svg


def init_transistor_state():
    """Initializes session state keys for bidirectional synchronization."""
    defaults = {
        "v_in": 3.3,
        "v_th": 0.7,
        "r_l": 1000.0,
        "v_cc": 5.0,
        "i_c_max": 20.0,
    }
    for k, v in defaults.items():
        if f"trans_{k}" not in st.session_state:
            st.session_state[f"trans_{k}"] = v
        if f"slider_{k}" not in st.session_state:
            st.session_state[f"slider_{k}"] = v
        if f"num_{k}" not in st.session_state:
            st.session_state[f"num_{k}"] = v


def sync_param(param_key, source):
    """Synchronizes value between slider and manual text input."""
    if source == "slider":
        val = float(st.session_state[f"slider_{param_key}"])
        st.session_state[f"trans_{param_key}"] = val
        st.session_state[f"num_{param_key}"] = val
    elif source == "num":
        val = float(st.session_state[f"num_{param_key}"])
        st.session_state[f"trans_{param_key}"] = val
        st.session_state[f"slider_{param_key}"] = val


def render_transistor_module():
    """Renders the complete Transistor Switching module."""
    init_transistor_state()

    st.html("""
    <div class="hero-banner">
        <div class="hero-title">Module 1: Transistor as an Electronic Switch</div>
        <div class="hero-subtitle">
            Observe how a semiconductor device transitions between <b>Cutoff (Open Switch / Logic 1)</b> 
            and <b>Saturation (Closed Switch / Logic 0)</b>. Adjust parameters using the synchronized sliders and manual input fields.
        </div>
    </div>
    """)

    # Quick switching demo buttons — directly demonstrate transistor switching
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        if st.button("🔴 Set to OFF (Cutoff — V_in below threshold)", use_container_width=True):
            st.session_state["trans_v_in"] = 0.2
            st.session_state["slider_v_in"] = 0.2
            st.session_state["num_v_in"] = 0.2
            st.rerun()
    with col_p2:
        if st.button("🟢 Set to ON (Saturation — V_in above threshold)", use_container_width=True):
            st.session_state["trans_v_in"] = 3.3
            st.session_state["slider_v_in"] = 3.3
            st.session_state["num_v_in"] = 3.3
            st.rerun()

    # Layout: Controls on Left, Visualizations on Right
    left_col, right_col = st.columns([1.1, 1.9], gap="large")

    with left_col:
        st.markdown("### 🎛️ Control Panel")
        st.caption("Adjust sliders or type precise values into text boxes:")

        # 1. Base Voltage (V_in)
        st.markdown("**1. Base / Gate Input Voltage ($V_{in}$)**")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.slider(
                "Base Voltage Slider (V)",
                min_value=0.0,
                max_value=6.0,
                value=float(st.session_state["trans_v_in"]),
                step=0.05,
                key="slider_v_in",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("v_in", "slider"),
            )
        with c2:
            st.number_input(
                "Base Voltage Num (V)",
                min_value=0.0,
                max_value=6.0,
                value=float(st.session_state["trans_v_in"]),
                step=0.05,
                key="num_v_in",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("v_in", "num"),
            )

        # 2. Switching Threshold (V_th)
        st.markdown("**2. Switching Threshold ($V_{th}$ / $V_{BE(on)}$)**")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.slider(
                "Threshold Slider (V)",
                min_value=0.1,
                max_value=4.0,
                value=float(st.session_state["trans_v_th"]),
                step=0.05,
                key="slider_v_th",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("v_th", "slider"),
            )
        with c2:
            st.number_input(
                "Threshold Num (V)",
                min_value=0.1,
                max_value=4.0,
                value=float(st.session_state["trans_v_th"]),
                step=0.05,
                key="num_v_th",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("v_th", "num"),
            )

        # 3. Load Resistance (R_L)
        st.markdown("**3. Collector/Drain Load Resistance ($R_L$)**")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.slider(
                "Load Resistance Slider (Ω)",
                min_value=100.0,
                max_value=10000.0,
                value=float(st.session_state["trans_r_l"]),
                step=100.0,
                key="slider_r_l",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("r_l", "slider"),
            )
        with c2:
            st.number_input(
                "Load Resistance Num (Ω)",
                min_value=100.0,
                max_value=10000.0,
                value=float(st.session_state["trans_r_l"]),
                step=50.0,
                key="num_r_l",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("r_l", "num"),
            )

        # 4. Collector/Drain Current Limit (I_C max / rating)
        st.markdown("**4. Max Collector/Drain Current Limit ($I_{C,max}$ in mA)**")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.slider(
                "Max Current Slider (mA)",
                min_value=1.0,
                max_value=50.0,
                value=float(st.session_state["trans_i_c_max"]),
                step=0.5,
                key="slider_i_c_max",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("i_c_max", "slider"),
            )
        with c2:
            st.number_input(
                "Max Current Num (mA)",
                min_value=1.0,
                max_value=50.0,
                value=float(st.session_state["trans_i_c_max"]),
                step=0.5,
                key="num_i_c_max",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("i_c_max", "num"),
            )


    # Physics Calculation Engine
    v_in = float(st.session_state["trans_v_in"])
    v_th = float(st.session_state["trans_v_th"])
    r_l  = float(st.session_state["trans_r_l"])
    v_cc = 5.0  # Fixed supply voltage (V) — standard digital logic rail
    i_c_limit = float(st.session_state["trans_i_c_max"]) / 1000.0  # in Amperes
    r_b = 10000.0  # 10 kΩ base resistor
    v_ce_sat = 0.2  # Saturation voltage (V)
    beta = 100.0    # Transistor Current Gain

    # Base Current (A)
    if v_in <= v_th:
        i_b = 0.0
    else:
        i_b = (v_in - v_th) / r_b

    # Active Collector Current (A)
    i_c_active = beta * i_b

    # Maximum Collector Current allowed by DC Load Line (Saturation Current)
    i_c_sat_circuit = (v_cc - v_ce_sat) / r_l
    i_c_max_allowed = min(i_c_sat_circuit, i_c_limit)

    # Actual Collector Current & Output Voltage
    if v_in <= v_th:
        state = "CUTOFF"
        i_c = 0.0
        v_out = v_cc
        switch_mode = "OPEN (OFF)"
        badge_class = "badge-cutoff"
        icon = "⭕"
    elif i_c_active >= i_c_max_allowed:
        state = "SATURATION"
        i_c = i_c_max_allowed
        v_out = v_ce_sat
        switch_mode = "CLOSED (ON)"
        badge_class = "badge-saturation"
        icon = "🟢"
    else:
        state = "ACTIVE"
        i_c = i_c_active
        v_out = max(v_ce_sat, v_cc - i_c * r_l)
        switch_mode = "TRANSITION (LINEAR)"
        badge_class = "badge-active"
        icon = "🟡"

    i_c_ma = i_c * 1000.0
    i_b_ua = i_b * 1e6
    logic_level = "1 (HIGH)" if v_out > (v_cc / 2.0) else "0 (LOW)"

    # Render Visualizations Column
    with right_col:
        # Status & Metric Cards
        st.html(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <span style="font-size:1.15rem; font-weight:600; color:#f8fafc;">Operating State:</span>
            <span class="badge {badge_class}">{icon} {state} REGION &bull; SWITCH {switch_mode}</span>
        </div>
        """)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.html(f"""
            <div class="metric-pill">
                <div class="label">V_in (Base)</div>
                <div class="value">{v_in:.2f} V</div>
            </div>
            """)
        with m2:
            st.html(f"""
            <div class="metric-pill">
                <div class="label">V_out (Collector)</div>
                <div class="value" style="color:{'#22c55e' if v_out > 2.5 else '#f43f5e'}">{v_out:.2f} V</div>
            </div>
            """)
        with m3:
            st.html(f"""
            <div class="metric-pill">
                <div class="label">I_C (Collector)</div>
                <div class="value">{i_c_ma:.2f} mA</div>
            </div>
            """)
        with m4:
            st.html(f"""
            <div class="metric-pill">
                <div class="label">Digital Logic</div>
                <div class="value">{logic_level}</div>
            </div>
            """)

        # SVG Schematic
        st.markdown("#### ⚡ Dynamic Circuit Schematic")
        svg_code = generate_transistor_circuit_svg(v_in, v_out, i_c_ma, i_b_ua, r_l, v_cc, v_th, state)
        render_svg(svg_code, height=410)

    # Educational Takeaway
    st.html("""
    <div class="glass-card" style="margin-top:20px;">
        <h4 style="color:#38bdf8; margin-bottom:8px;">💡 Physical Bridge to Logic Gates</h4>
        <p style="color:#cbd5e1; font-size:0.95rem; margin-bottom:0;">
            Notice how when the input voltage is <b>LOW (V_in &lt; V_th)</b>, the transistor is completely non-conductive, 
            leaving the output pulled <b>HIGH (V_out ≈ V_CC)</b>. When the input voltage is <b>HIGH (V_in &gt; V_th)</b>, 
            the transistor conducts strongly into saturation, pulling the output down to ground <b>(V_out ≈ 0.2V, LOW)</b>.
            This natural semiconductor inversion is the foundation of the <b>NOT Gate (Inverter)</b>, and combining 
            multiple transistors in series and parallel forms every classical logic gate in Module 2!
        </p>
    </div>
    """)
