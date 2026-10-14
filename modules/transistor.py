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

    # Preset Quick Buttons
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        if st.button("🔴 Set to OFF (Cutoff)", use_container_width=True):
            st.session_state["trans_v_in"] = 0.2
            st.session_state["slider_v_in"] = 0.2
            st.session_state["num_v_in"] = 0.2
            st.rerun()
    with col_p2:
        if st.button("🟢 Set to ON (Saturation)", use_container_width=True):
            st.session_state["trans_v_in"] = 3.3
            st.session_state["slider_v_in"] = 3.3
            st.session_state["num_v_in"] = 3.3
            st.rerun()
    with col_p3:
        if st.button("⚙️ BJT Preset (Vth = 0.7V)", use_container_width=True):
            st.session_state["trans_v_th"] = 0.7
            st.session_state["slider_v_th"] = 0.7
            st.session_state["num_v_th"] = 0.7
            st.session_state["trans_v_in"] = 2.5
            st.session_state["slider_v_in"] = 2.5
            st.session_state["num_v_in"] = 2.5
            st.session_state["trans_r_l"] = 1000.0
            st.session_state["slider_r_l"] = 1000.0
            st.session_state["num_r_l"] = 1000.0
            st.rerun()
    with col_p4:
        if st.button("⚡ MOSFET Preset (Vth = 2.0V)", use_container_width=True):
            st.session_state["trans_v_th"] = 2.0
            st.session_state["slider_v_th"] = 2.0
            st.session_state["num_v_th"] = 2.0
            st.session_state["trans_v_in"] = 4.0
            st.session_state["slider_v_in"] = 4.0
            st.session_state["num_v_in"] = 4.0
            st.session_state["trans_r_l"] = 2000.0
            st.session_state["slider_r_l"] = 2000.0
            st.session_state["num_r_l"] = 2000.0
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

        # 5. Supply Voltage (V_CC)
        st.markdown("**5. Collector Supply Voltage ($V_{CC}$)**")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.slider(
                "Supply Voltage Slider (V)",
                min_value=2.0,
                max_value=12.0,
                value=float(st.session_state["trans_v_cc"]),
                step=0.5,
                key="slider_v_cc",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("v_cc", "slider"),
            )
        with c2:
            st.number_input(
                "Supply Voltage Num (V)",
                min_value=2.0,
                max_value=12.0,
                value=float(st.session_state["trans_v_cc"]),
                step=0.5,
                key="num_v_cc",
                label_visibility="collapsed",
                on_change=sync_param,
                args=("v_cc", "num"),
            )

    # Physics Calculation Engine
    v_in = float(st.session_state["trans_v_in"])
    v_th = float(st.session_state["trans_v_th"])
    r_l = float(st.session_state["trans_r_l"])
    v_cc = float(st.session_state["trans_v_cc"])
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

    # Section: Real-time Characteristic Plots
    st.markdown("---")
    st.markdown("### 📈 Analytical Characteristics & Load Line Analysis")
    
    tab1, tab2 = st.tabs(["📊 Voltage Transfer Characteristic (VTC)", "📉 DC Load Line & Q-Point"])

    with tab1:
        # Plot VTC: V_out vs V_in
        v_in_range = np.linspace(0.0, 6.0, 300)
        v_out_curve = []
        for v in v_in_range:
            if v <= v_th:
                v_out_curve.append(v_cc)
            else:
                ib_sim = (v - v_th) / r_b
                ic_sim = min(beta * ib_sim, i_c_max_allowed)
                v_out_curve.append(max(v_ce_sat, v_cc - ic_sim * r_l))

        fig, ax = plt.subplots(figsize=(10, 3.8), facecolor="#090d16")
        ax.set_facecolor("#0f172a")

        # Color regions
        ax.axvspan(0.0, v_th, alpha=0.15, color="#ef4444", label="Cutoff (OFF)")
        # Find saturation boundary
        v_sat_boundary = v_th + (i_c_max_allowed / beta) * r_b
        if v_sat_boundary < 6.0:
            ax.axvspan(v_th, v_sat_boundary, alpha=0.15, color="#f59e0b", label="Active (Linear)")
            ax.axvspan(v_sat_boundary, 6.0, alpha=0.15, color="#22c55e", label="Saturation (ON)")
        else:
            ax.axvspan(v_th, 6.0, alpha=0.15, color="#f59e0b", label="Active (Linear)")

        ax.plot(v_in_range, v_out_curve, color="#38bdf8", linewidth=2.8, label="V_out vs V_in (Inverting Transfer)")
        # Current Operating Point
        ax.scatter([v_in], [v_out], color="#00f0ff", s=130, zorder=5, edgecolor="#ffffff", linewidth=2, label="Current Q-Point")
        ax.axvline(v_in, color="#00f0ff", linestyle=":", alpha=0.6)
        ax.axhline(v_out, color="#00f0ff", linestyle=":", alpha=0.6)

        ax.set_title("Transistor Inverter Voltage Transfer Characteristic (VTC)", color="#f8fafc", fontsize=12, fontweight="bold")
        ax.set_xlabel("Input Base Voltage V_in (V)", color="#94a3b8", fontsize=11)
        ax.set_ylabel("Output Collector Voltage V_out (V)", color="#94a3b8", fontsize=11)
        ax.tick_params(colors="#cbd5e1")
        ax.grid(True, linestyle="--", alpha=0.2, color="#ffffff")
        ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", loc="upper right")
        ax.set_ylim(-0.2, v_cc + 0.8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with tab2:
        # Plot DC Load Line on IC vs VCE
        v_ce_axis = np.linspace(0.0, v_cc, 100)
        # Load line: I_C = (V_CC - V_CE) / R_L
        ic_load_line = ((v_cc - v_ce_axis) / r_l) * 1000.0  # in mA

        fig2, ax2 = plt.subplots(figsize=(10, 3.8), facecolor="#090d16")
        ax2.set_facecolor("#0f172a")

        # Family of transistor curves for different I_B
        sample_ib = [0.0, 10.0, 25.0, 50.0, 80.0, 120.0]  # uA
        for ib_val in sample_ib:
            ic_active_val = min((beta * ib_val * 1e-6) * 1000.0, (v_cc / r_l) * 1000.0 * 1.2)
            # simulate slight slope
            v_sat_knee = 0.3
            curve = [ic_active_val * (1 - np.exp(-v / v_sat_knee)) for v in v_ce_axis]
            ax2.plot(v_ce_axis, curve, color="#475569", linestyle="--", alpha=0.5)

        # Plot DC Load Line
        ax2.plot(v_ce_axis, ic_load_line, color="#f59e0b", linewidth=2.8, label=f"DC Load Line (Slope = -1/{r_l:.0f}Ω)")
        
        # Plot Q-point
        q_vce = v_out
        q_ic_ma = i_c_ma
        ax2.scatter([q_vce], [q_ic_ma], color="#22c55e", s=140, zorder=5, edgecolor="#ffffff", linewidth=2, label=f"Q-Point: ({q_vce:.2f}V, {q_ic_ma:.2f}mA)")
        ax2.axvline(q_vce, color="#22c55e", linestyle=":", alpha=0.6)
        ax2.axhline(q_ic_ma, color="#22c55e", linestyle=":", alpha=0.6)

        # Cutoff and Saturation points labels
        ax2.scatter([v_cc], [0], color="#ef4444", s=70, label=f"Cutoff Pt (V_CC={v_cc:.1f}V)")
        ax2.scatter([0], [(v_cc / r_l) * 1000.0], color="#38bdf8", s=70, label=f"Max Saturation ({(v_cc/r_l)*1000.0:.1f}mA)")

        ax2.set_title("DC Load Line & Operating Q-Point on Transistor Output Plane", color="#f8fafc", fontsize=12, fontweight="bold")
        ax2.set_xlabel("Collector-Emitter Voltage V_CE (V)", color="#94a3b8", fontsize=11)
        ax2.set_ylabel("Collector Current I_C (mA)", color="#94a3b8", fontsize=11)
        ax2.tick_params(colors="#cbd5e1")
        ax2.grid(True, linestyle="--", alpha=0.2, color="#ffffff")
        ax2.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", loc="upper right")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

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
