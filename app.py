"""
TransistorToQubit: The Evolution of Computing
Main Streamlit application entry point.
"""

import os
import streamlit as st
import qiskit
import matplotlib

from config import APP_TITLE, APP_ICON, APP_SUBTITLE, MODULES
from modules.transistor import render_transistor_module
from modules.logic_gates import render_logic_gates_module
from modules.quantum import render_quantum_module
from modules.comparison import render_comparison_module


def load_custom_css():
    """Loads and injects custom CSS for sleek modern dark styling."""
    css_path = os.path.join(os.path.dirname(__file__), "styles", "custom.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Transistor to Qubit",
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="auto",
    )

    load_custom_css()

    # Sidebar Navigation & Branding
    with st.sidebar:
        st.html(f"""
        <div style="padding:10px 0 16px 0;">
            <div style="font-size:1.8rem; font-weight:800; color:#73d0ff; display:flex; align-items:center; gap:8px;">
                <span>{APP_ICON}</span> <span>TransistorToQubit</span>
            </div>
            <div style="font-size:0.85rem; color:#a6acb8; margin-top:4px;">
                Interactive Computing Architecture Lab
            </div>
        </div>
        """)

        st.markdown("### 🧭 Navigation")
        # Initialise navigation target if not already set
        if "nav_module" not in st.session_state:
            st.session_state["nav_module"] = "module1"
        selected_module_key = st.radio(
            "Select Module:",
            options=list(MODULES),
            format_func=lambda k: MODULES[k]["title"],
            label_visibility="collapsed",
            key="nav_module",
        )

        st.markdown("---")
        st.markdown("### 🗺️ The Computing Continuum")
        st.markdown("""
        1. **Physical Layer**  
           _Transistor Switch_  
           Cutoff vs Saturation
        2. **Gate Layer**  
           _Classical Gates_  
           NOT, AND, OR, NAND, NOR, XOR
        3. **Quantum Layer**  
           _Qubits & Superposition_  
           |0⟩, |1⟩, X, H, Z, CNOT, M
        4. **Comparison**  
           _Classical ↔ Quantum_  
           Concept map, levels & noise
        """)

        import sys
        st.markdown("---")
        st.markdown("### ⚙️ System Environment")
        st.caption(f"""
        - **Python Version:** `{sys.version.split()[0]}`
        - **Qiskit Version:** `{qiskit.__version__}`
        - **Streamlit Version:** `{st.__version__}`
        - **Matplotlib:** `{matplotlib.__version__}`
        """)

    # Main Area Routing
    if selected_module_key == "module1":
        render_transistor_module()
    elif selected_module_key == "module2":
        render_logic_gates_module()
    elif selected_module_key == "module3":
        render_quantum_module()
    elif selected_module_key == "module4":
        render_comparison_module()


if __name__ == "__main__":
    main()
