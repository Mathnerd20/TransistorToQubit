"""
Module 2: Classical Logic Gates.
Interactive exploration of NOT, AND, OR, NAND, NOR, and XOR gates.
Shows logic symbols, transistor-level RTL/CMOS schematics, live truth tables, and boolean outputs.
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.svg_generator import (
    generate_logic_gate_symbol_svg,
    generate_transistor_logic_circuit_svg,
    render_svg,
)

# Logic Gate Definitions
GATE_INFO = {
    "NOT": {
        "title": "NOT Gate (Inverter)",
        "inputs": 1,
        "formula": "Q = A'",
        "boolean": "Q = \\neg A",
        "description": "Inverts the input signal. Built from a single transistor switch: HIGH input activates transistor, pulling output LOW to Ground.",
        "transistor_topology": "Single NPN Common-Emitter with Pull-Up Resistor",
    },
    "AND": {
        "title": "AND Gate",
        "inputs": 2,
        "formula": "Q = A · B",
        "boolean": "Q = A \\land B",
        "description": "Output is HIGH (1) only if BOTH inputs are HIGH. Built by taking a NAND gate (two transistors in series) followed by a NOT inverter stage.",
        "transistor_topology": "Two NPN transistors in Series (NAND stage) + Inverter stage",
    },
    "OR": {
        "title": "OR Gate",
        "inputs": 2,
        "formula": "Q = A + B",
        "boolean": "Q = A \\lor B",
        "description": "Output is HIGH (1) if AT LEAST ONE input is HIGH. Built by taking a NOR gate (two transistors in parallel) followed by a NOT inverter stage.",
        "transistor_topology": "Two NPN transistors in Parallel (NOR stage) + Inverter stage",
    },
    "NAND": {
        "title": "NAND Gate (Universal)",
        "inputs": 2,
        "formula": "Q = (A · B)'",
        "boolean": "Q = \\neg(A \\land B)",
        "description": "Universal Gate: Output is LOW only if BOTH inputs are HIGH. Built naturally in silicon with two series transistors pulling down to Ground.",
        "transistor_topology": "Two NPN transistors in Series directly to Ground with Pull-Up",
    },
    "NOR": {
        "title": "NOR Gate (Universal)",
        "inputs": 2,
        "formula": "Q = (A + B)'",
        "boolean": "Q = \\neg(A \\lor B)",
        "description": "Universal Gate: Output is HIGH only if BOTH inputs are LOW. Built naturally with two parallel transistors connected to Ground.",
        "transistor_topology": "Two NPN transistors in Parallel directly to Ground with Pull-Up",
    },
    "XOR": {
        "title": "XOR Gate (Exclusive OR)",
        "inputs": 2,
        "formula": "Q = A ⊕ B = A·B' + A'·B",
        "boolean": "Q = A \\oplus B",
        "description": "Output is HIGH if inputs are DIFFERENT (odd parity). Critical for half-adders and binary arithmetic.",
        "transistor_topology": "Dual Series NPN RTL Branches (A·B' + A'·B) with Inverter Stage",
    },
}


def compute_gate_output(gate_name, in_a, in_b=0):
    """Calculates boolean output for the given gate and inputs."""
    a = bool(in_a)
    b = bool(in_b)
    if gate_name == "NOT":
        return int(not a)
    elif gate_name == "AND":
        return int(a and b)
    elif gate_name == "OR":
        return int(a or b)
    elif gate_name == "NAND":
        return int(not (a and b))
    elif gate_name == "NOR":
        return int(not (a or b))
    elif gate_name == "XOR":
        return int(a != b)
    return 0


def render_truth_table_html(gate_name, active_a, active_b=0):
    """Generates styled HTML truth table highlighting current active input state."""
    is_not = (gate_name == "NOT")
    
    th_style = "background:rgba(30,41,59,0.95); color:#cbd5e1; padding:10px 14px; font-weight:700; text-align:center; border-bottom:1px solid rgba(148,163,184,0.3); font-size:0.9rem;"
    td_style_base = "padding:10px 14px; text-align:center; border-bottom:1px solid rgba(148,163,184,0.15); color:#94a3b8; font-size:0.95rem;"
    td_active_style = "padding:10px 14px; text-align:center; background:rgba(56,189,248,0.2); color:#38bdf8; font-weight:bold; border-top:1px solid rgba(56,189,248,0.5); border-bottom:1px solid rgba(56,189,248,0.5); font-size:1.0rem;"
    table_style = "width:100%; border-collapse:separate; border-spacing:0; border-radius:10px; overflow:hidden; border:1px solid rgba(148,163,184,0.25); font-family:'JetBrains Mono', monospace; background:#0b1120;"

    if is_not:
        rows = [(0, compute_gate_output("NOT", 0)),
                (1, compute_gate_output("NOT", 1))]
        row_htmls = []
        for a, q in rows:
            is_active = (a == active_a)
            cur_td = td_active_style if is_active else td_style_base
            indicator = "👉 " if is_active else ""
            q_color = "#34d399" if q else "#64748b"
            row_htmls.append(
                f'<tr class="{"active-row" if is_active else ""}">'
                f'<td style="{cur_td}">{indicator}<b>{a}</b></td>'
                f'<td style="{cur_td} color:{q_color}; font-weight:bold;">{q}</td>'
                f'</tr>'
            )
        return (
            f'<table class="custom-table" style="{table_style}">'
            f'<thead><tr><th style="{th_style}">Input A</th><th style="{th_style}">Output Q (NOT A)</th></tr></thead>'
            f'<tbody>{"".join(row_htmls)}</tbody>'
            f'</table>'
        )
    else:
        combinations = [(0, 0), (0, 1), (1, 0), (1, 1)]
        row_htmls = []
        for a, b in combinations:
            q = compute_gate_output(gate_name, a, b)
            is_active = (a == active_a and b == active_b)
            cur_td = td_active_style if is_active else td_style_base
            indicator = "👉 " if is_active else ""
            q_color = "#34d399" if q else "#64748b"
            row_htmls.append(
                f'<tr class="{"active-row" if is_active else ""}">'
                f'<td style="{cur_td}">{indicator}<b>{a}</b></td>'
                f'<td style="{cur_td}"><b>{b}</b></td>'
                f'<td style="{cur_td} color:{q_color}; font-weight:bold;">{q}</td>'
                f'</tr>'
            )
        return (
            f'<table class="custom-table" style="{table_style}">'
            f'<thead><tr><th style="{th_style}">Input A</th><th style="{th_style}">Input B</th><th style="{th_style}">Output Q ({gate_name})</th></tr></thead>'
            f'<tbody>{"".join(row_htmls)}</tbody>'
            f'</table>'
        )


def render_truth_table(gate_name, active_a, active_b=0):
    """Renders styled truth table in an isolated frame so that HTML is rendered directly by the browser."""
    table_html = render_truth_table_html(gate_name, active_a, active_b)
    frame_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    body {{
      background: transparent;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
  </style>
</head>
<body>
  {table_html}
</body>
</html>"""
    height = 155 if gate_name == "NOT" else 235
    components.html(frame_html, height=height)


def render_logic_gates_module():
    """Renders the Classical Logic Gates module."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Module 2: Classical Logic Gates</div>
        <div class="hero-subtitle">
            Explore fundamental digital building blocks constructed from silicon transistors. 
            Toggle inputs <b>0</b> and <b>1</b> to observe outputs, standard gate symbols, and underlying transistor schematics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Gate Selection Tabs / Buttons
    selected_gate = st.radio(
        "Select Logic Gate:",
        ["NOT", "AND", "OR", "NAND", "NOR", "XOR"],
        horizontal=True,
        index=0,
    )

    info = GATE_INFO[selected_gate]

    # Two column layout: Inputs & Truth Table on Left, Circuit Diagrams on Right
    col_left, col_right = st.columns([1.1, 1.9], gap="large")

    with col_left:
        st.markdown(f"### 🎛️ Input Controls: {selected_gate}")
        
        # Input A Switch (with fallback for streamlit < 1.40)
        st.markdown("**Input A:**")
        if hasattr(st, "segmented_control"):
            in_a = st.segmented_control(
                "Input A",
                options=[0, 1],
                default=0,
                key=f"gate_in_a_{selected_gate}",
                label_visibility="collapsed",
            )
            if in_a is None:
                in_a = 0
        else:
            in_a = st.radio(
                "Input A",
                options=[0, 1],
                index=0,
                horizontal=True,
                key=f"gate_in_a_{selected_gate}",
                label_visibility="collapsed",
            )

        # Input B Switch (if not single-input)
        in_b = 0
        if info["inputs"] == 2:
            st.markdown("**Input B:**")
            if hasattr(st, "segmented_control"):
                in_b = st.segmented_control(
                    "Input B",
                    options=[0, 1],
                    default=0,
                    key=f"gate_in_b_{selected_gate}",
                    label_visibility="collapsed",
                )
                if in_b is None:
                    in_b = 0
            else:
                in_b = st.radio(
                    "Input B",
                    options=[0, 1],
                    index=0,
                    horizontal=True,
                    key=f"gate_in_b_{selected_gate}",
                    label_visibility="collapsed",
                )

        # Calculate Output
        out_val = compute_gate_output(selected_gate, in_a, in_b)

        # Output Badge & Callout
        st.markdown("---")
        st.markdown("#### 💡 Output Status")
        out_color = "#22c55e" if out_val else "#64748b"
        out_badge_class = "badge-high" if out_val else "badge-low"
        out_state_str = "HIGH (Logic 1 / 5V)" if out_val else "LOW (Logic 0 / 0V)"
        
        st.html(f"""
        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:12px; padding:18px; text-align:center;">
            <div style="font-size:0.85rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">Boolean Output Q</div>
            <div style="font-size:3rem; font-weight:800; font-family:'JetBrains Mono', monospace; color:{out_color}; line-height:1;">
                {out_val}
            </div>
            <div style="margin-top:10px;">
                <span class="badge {out_badge_class}">{out_state_str}</span>
            </div>
            <div style="margin-top:12px; font-family:'JetBrains Mono', monospace; color:#cbd5e1; font-size:1.05rem;">
                {info['formula']}
            </div>
        </div>
        """)

        # Live Truth Table
        st.markdown("#### 📋 Truth Table")
        st.caption("Active input row highlighted in blue:")
        render_truth_table(selected_gate, in_a, in_b)

        # NOT → X Gate navigation (doc guideline: introduce quantum equivalent)
        if selected_gate == "NOT":
            st.markdown("---")
            st.html("""<div style="background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.3); border-radius:10px; padding:12px 16px;">
                <div style="color:#d4bfff; font-weight:600; margin-bottom:4px;">💡 Classical NOT ↔ Quantum Analogue</div>
                <div style="color:#94a3b8; font-size:0.85rem;">X|0⟩ = |1⟩ &nbsp;·&nbsp; X|1⟩ = |0⟩</div>
            </div>""")
            if st.button("⚛️ Open X Gate in Module 3 →", use_container_width=True, key="btn_goto_x"):
                st.session_state["nav_module"] = "module3"
                st.session_state["quantum_mode"] = "🔬 Single-Qubit Gate Explorer (X, H, Z, M)"
                st.session_state["quantum_gate_choice"] = "X"
                st.rerun()

    with col_right:
        # Gate Description & Silicon Topology
        st.markdown(f"### 📐 {info['title']}")
        st.html(f"""
        <div class="glass-card" style="padding:14px 18px; margin-bottom:14px;">
            <p style="color:#f8fafc; font-size:0.95rem; margin-bottom:6px;">{info['description']}</p>
            <div style="display:flex; gap:16px; font-size:0.85rem; color:#94a3b8;">
                <span><b>Silicon Topology:</b> {info['transistor_topology']}</span>
            </div>
        </div>
        """)

        # Tabs for Gate Symbol vs Transistor Schematic
        tab_symbol, tab_transistor = st.tabs(["🔲 IEEE Logic Gate Symbol", "🔌 Transistor-Level Circuit (Silicon)"])

        with tab_symbol:
            st.caption("Standard circuit representation with live wire logic states:")
            symbol_svg = generate_logic_gate_symbol_svg(selected_gate, in_a, in_b, out_val)
            render_svg(symbol_svg, height=260)

        with tab_transistor:
            st.caption("How physical NPN transistors form this logic gate inside an integrated circuit (IC):")
            trans_svg = generate_transistor_logic_circuit_svg(selected_gate, in_a, in_b, out_val)
            render_svg(trans_svg, height=480)

