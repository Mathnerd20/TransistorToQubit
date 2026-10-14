"""
Module 3: Quantum Gates & Circuits using Qiskit.
Explores qubits |0⟩, |1⟩, Pauli-X, Hadamard (H), Pauli-Z, CNOT, and Measurement.
Provides visual Qiskit circuit diagrams (mpl), statevectors, Bloch spheres,
and Aer measurement simulations.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from utils.quantum_helpers import (
    GATE_MATRICES,
    build_single_qubit_circuit,
    build_two_qubit_cnot_circuit,
    format_statevector_latex,
    draw_circuit_mpl,
    draw_bloch_sphere,
    run_aer_simulation,
)


def render_quantum_module():
    """Renders the Quantum Gates & Circuits module."""
    st.html("""
    <div class="hero-banner">
        <div class="hero-title">Module 3: Quantum Gates & Qubits</div>
        <div class="hero-subtitle">
            Step from classical digital bits into the quantum realm. Explore quantum state preparation 
            <b>|0⟩</b> and <b>|1⟩</b>, quantum gates (<b>X, H, Z, CNOT</b>), <b>Bloch spheres</b>, and <b>quantum measurement collapse</b> using Qiskit.
        </div>
    </div>
    """)

    mode = st.radio(
        "Choose Quantum Exploration Mode:",
        ["🔬 Single-Qubit Gate Explorer (X, H, Z, M)", "⚡ Two-Qubit CNOT & Entanglement (Bell States)"],
        horizontal=True,
        key="quantum_mode",
    )

    if mode.startswith("🔬 Single-Qubit"):
        render_single_qubit_explorer()
    else:
        render_cnot_explorer()


def render_single_qubit_explorer():
    """Single Qubit gate exploration: input states |0⟩, |1⟩, gates X, H, Z, M."""
    col_ctrl, col_viz = st.columns([1.1, 1.9], gap="large")

    with col_ctrl:
        st.markdown("### 🎛️ Circuit Configuration")

        # 1. Input state selection
        st.markdown("**1. Select Initial Quantum State:**")
        initial_state = st.radio(
            "Initial State:",
            ["|0⟩", "|1⟩"],
            horizontal=True,
            index=0,
            key="quantum_init_state",
            help="|0⟩ is the ground state, |1⟩ is the excited state.",
        )

        # 2. Gate selection
        st.markdown("**2. Select Quantum Gate:**")
        gate_choice = st.radio(
            "Quantum Gate:",
            ["X", "H", "Z", "M"],
            horizontal=True,
            index=0,
            key="quantum_gate_choice",
            format_func=lambda g: f"{g} Gate" if g != "M" else "Measurement (M)",
        )


        # 3. Measurement toggle (if gate is not already M)
        with_measurement = True
        if gate_choice != "M":
            with_measurement = st.checkbox("Include Classical Measurement at End", value=True)

        shots = st.slider("Aer Simulation Shots:", min_value=128, max_value=4096, value=1024, step=128)

        # Gate Info Card
        gate_info = GATE_MATRICES[gate_choice]
        st.markdown("---")
        st.markdown(f"#### 📘 {gate_info['name']}")
        st.caption(gate_info["description"])

        st.latex(gate_info["latex"])
        st.latex(gate_info["formula"])

    # Build Qiskit Circuits
    qc_state, qc_meas = build_single_qubit_circuit(initial_state, gate_choice, with_measurement)
    sv = Statevector.from_instruction(qc_state)

    with col_viz:
        st.markdown("### 📐 Qiskit Circuit Diagram")
        fig_circuit = draw_circuit_mpl(qc_meas)
        st.pyplot(fig_circuit)
        plt.close(fig_circuit)

        # Quantum Statevector readout
        st.markdown("#### 🌊 Resulting Quantum Statevector")
        dirac_expr = format_statevector_latex(sv, num_qubits=1)
        
        # Calculate probabilities
        prob_0 = np.abs(sv.data[0]) ** 2
        prob_1 = np.abs(sv.data[1]) ** 2
        
        st.html(f"""
        <div class="glass-card" style="padding:16px 20px;">
            <div style="font-size:0.85rem; color:#94a3b8; text-transform:uppercase; margin-bottom:6px;">Dirac Bra-Ket State |ψ⟩</div>
            <div style="font-size:1.6rem; color:#d8b4fe; font-family:'JetBrains Mono', monospace; font-weight:700;">
                |ψ⟩ = {dirac_expr}
            </div>
            <div style="display:flex; gap:24px; margin-top:12px; font-family:'JetBrains Mono', monospace;">
                <div><span style="color:#94a3b8;">P(|0⟩):</span> <b style="color:#38bdf8;">{prob_0 * 100:.1f}%</b></div>
                <div><span style="color:#94a3b8;">P(|1⟩):</span> <b style="color:#a855f7;">{prob_1 * 100:.1f}%</b></div>
            </div>
        </div>
        """)

        # Visualizations: Bloch Sphere & Measurement Histogram
        tab_bloch, tab_hist = st.tabs(["🌐 Bloch Sphere 3D Representation", "📊 Aer Measurement Simulation"])

        with tab_bloch:
            st.caption("The Bloch Sphere geometrically represents any single-qubit quantum state on the unit sphere:")
            fig_bloch = draw_bloch_sphere(sv)
            st.pyplot(fig_bloch)
            plt.close(fig_bloch)

        with tab_hist:
            if with_measurement or gate_choice == "M":
                st.caption(f"Simulating wave-function collapse on Qiskit Aer ({shots} shots):")
                counts, fig_hist = run_aer_simulation(qc_meas, shots=shots)
                st.pyplot(fig_hist)
                plt.close(fig_hist)
            else:
                st.info("Enable 'Include Classical Measurement at End' to simulate quantum projective measurement.")


def render_cnot_explorer():
    """Two-qubit CNOT gate and Bell state entanglement explorer."""
    col_ctrl, col_viz = st.columns([1.1, 1.9], gap="large")

    with col_ctrl:
        st.markdown("### 🎛️ CNOT 2-Qubit Configuration")

        st.markdown("**1. Control Qubit ($q_0$):**")
        ctrl_state = st.radio("Control Input:", ["|0⟩", "|1⟩"], horizontal=True, key="cnot_ctrl_state")
        superpose_ctrl = st.checkbox("Apply Hadamard to Control (H q₀) → Create Bell State! 🔔", value=True)

        st.markdown("**2. Target Qubit ($q_1$):**")
        tgt_state = st.radio("Target Input:", ["|0⟩", "|1⟩"], horizontal=True, key="cnot_tgt_state")

        shots = st.slider("Aer Simulation Shots:", min_value=128, max_value=4096, value=1024, step=128, key="cnot_shots")

        cnot_info = GATE_MATRICES["CNOT"]
        st.markdown("---")
        st.markdown(f"#### 📘 {cnot_info['name']}")
        st.caption(cnot_info["description"])
        st.latex(cnot_info["latex"])
        st.latex(cnot_info["formula"])

    # Build 2-qubit circuit
    qc_state, qc_meas = build_two_qubit_cnot_circuit(ctrl_state, tgt_state, superpose_ctrl, with_measurement=True)
    sv = Statevector.from_instruction(qc_state)

    with col_viz:
        st.markdown("### 📐 2-Qubit Qiskit Circuit Diagram")
        fig_circuit = draw_circuit_mpl(qc_meas)
        st.pyplot(fig_circuit)
        plt.close(fig_circuit)

        # Statevector Readout
        st.markdown("#### 🌊 2-Qubit Entangled Statevector")
        dirac_expr = format_statevector_latex(sv, num_qubits=2)
        
        # Check if Bell State
        is_bell = superpose_ctrl
        bell_note = "✨ <b>Maximal Entanglement (Bell State)</b> created! Notice how measuring one qubit instantaneously determines the other!" if is_bell else "Unentangled / Product state."

        st.html(f"""
        <div class="glass-card" style="padding:16px 20px;">
            <div style="font-size:0.85rem; color:#94a3b8; text-transform:uppercase; margin-bottom:6px;">2-Qubit State |ψ⟩</div>
            <div style="font-size:1.6rem; color:#d8b4fe; font-family:'JetBrains Mono', monospace; font-weight:700;">
                |ψ⟩ = {dirac_expr}
            </div>
            <div style="margin-top:10px; font-size:0.9rem; color:#cbd5e1;">{bell_note}</div>
        </div>
        """)

        # Tabs for Bloch & Measurement
        tab_meas, tab_bloch2 = st.tabs(["📊 Measurement Correlation Histogram", "🌐 Bloch Spheres (q0 & q1)"])

        with tab_meas:
            st.caption(f"Sampling {shots} shots on Qiskit AerSimulator:")
            counts, fig_hist = run_aer_simulation(qc_meas, shots=shots)
            st.pyplot(fig_hist)
            plt.close(fig_hist)

        with tab_bloch2:
            st.caption("Bloch spheres for both qubits (Note: in maximally entangled states, single-qubit Bloch vectors shrink to the center):")
            fig_bloch = draw_bloch_sphere(sv)
            st.pyplot(fig_bloch)
            plt.close(fig_bloch)



