"""
Module D: Classical-to-Quantum Comparison Framework.
Implements the concept-mapping table from the assignment document and a
side-by-side noise comparison (transistor noise vs quantum decoherence).
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------------------------
# The concept mapping rows exactly as defined in the document
# ------------------------------------------------------------------
CONCEPT_MAP = [
    {
        "classical_concept": "Transistor",
        "student_knows":     "Electronic switching device",
        "quantum_counterpart":"Qubit as quantum information unit",
        "classical_icon": "🔌",
        "quantum_icon":   "⚛️",
    },
    {
        "classical_concept": "ON / OFF",
        "student_knows":     "Binary voltage levels  (0 V / 5 V)",
        "quantum_counterpart":"Measurement collapses to 0 or 1",
        "classical_icon": "⭕ 🟢",
        "quantum_icon":   "📏",
    },
    {
        "classical_concept": "Voltage / Current State",
        "student_knows":     "Physical representation of information",
        "quantum_counterpart":"Quantum state / Probability amplitude",
        "classical_icon": "⚡",
        "quantum_icon":   "🌊",
    },
    {
        "classical_concept": "Logic Gate (NOT, AND, OR…)",
        "student_knows":     "Deterministic Boolean operation",
        "quantum_counterpart":"Quantum Gate (X, H, Z, CNOT…)",
        "classical_icon": "🔲",
        "quantum_icon":   "🔷",
    },
    {
        "classical_concept": "NOT Gate",
        "student_knows":     "Inverts 0 ↔ 1",
        "quantum_counterpart":"X Gate performs a quantum bit-flip",
        "classical_icon": "🔲",
        "quantum_icon":   "✖️",
    },
    {
        "classical_concept": "Digital Circuit",
        "student_knows":     "Combination of classical logic gates",
        "quantum_counterpart":"Quantum Circuit (sequence of quantum gates)",
        "classical_icon": "🖥️",
        "quantum_icon":   "🔬",
    },
    {
        "classical_concept": "Classical Bit",
        "student_knows":     "b ∈ {0, 1}  — always definite",
        "quantum_counterpart":"|ψ⟩ = α|0⟩ + β|1⟩  (superposition)",
        "classical_icon": "🔢",
        "quantum_icon":   "🌀",
    },
    {
        "classical_concept": "Noise",
        "student_knows":     "Disturbs transistor voltage signal",
        "quantum_counterpart":"Decoherence / Quantum noise",
        "classical_icon": "📡",
        "quantum_icon":   "💫",
    },
    {
        "classical_concept": "Measurement",
        "student_knows":     "Reading circuit output — non-destructive",
        "quantum_counterpart":"Quantum measurement collapses the state irreversibly",
        "classical_icon": "📊",
        "quantum_icon":   "🎲",
    },
    {
        "classical_concept": "Deterministic",
        "student_knows":     "Same input always gives same output",
        "quantum_counterpart":"Probabilistic — outcome governed by Born rule",
        "classical_icon": "✅",
        "quantum_icon":   "🎲",
    },
]

# Four progressive learning levels
LEVELS = [
    {
        "id": 1,
        "title": "Level 1 — Transistor Switch",
        "color": "#22c55e",
        "classical": "Transistor circuit: Vin → Transistor → LED\nVin = 0  →  OFF (Logic 0)\nVin = 1  →  ON  (Logic 1)",
        "transition": "The transistor is the physical embodiment of a classical bit. Two voltage levels represent 0 and 1.",
        "quantum": "The qubit is the quantum equivalent — it can be |0⟩ or |1⟩, but unlike the transistor it can also be in a superposition of both.",
    },
    {
        "id": 2,
        "title": "Level 2 — Logic Gate",
        "color": "#38bdf8",
        "classical": "NOT Gate:\n  0 → 1\n  1 → 0",
        "transition": "The classical NOT gate inverts a bit. The quantum X gate does the same thing but on a qubit.",
        "quantum": "X Gate (Quantum NOT):\n  X|0⟩ = |1⟩\n  X|1⟩ = |0⟩",
    },
    {
        "id": 3,
        "title": "Level 3 — Bit → Qubit (Superposition)",
        "color": "#a855f7",
        "classical": "Classical bit:\n  b ∈ {0, 1}\n  Always 0 or always 1.",
        "transition": "The Hadamard gate has no classical analogue. It creates genuine quantum superposition — the qubit is in BOTH states simultaneously until measured.",
        "quantum": "Qubit state:\n  |ψ⟩ = α|0⟩ + β|1⟩\n\nHadamard gate:\n  H|0⟩ = (|0⟩ + |1⟩)/√2\n  → P(0) = 50%, P(1) = 50%",
    },
    {
        "id": 4,
        "title": "Level 4 — Classical Circuit vs Quantum Circuit",
        "color": "#f59e0b",
        "classical": "Transistors → Logic Gates → Digital Output\nDeterministic, fast, scalable.\nOutput is always a definite 0 or 1.",
        "transition": "Both perform computation through sequences of operations. But quantum circuits exploit superposition and entanglement for exponential parallelism.",
        "quantum": "Qubits → Quantum Gates → Measurement\nProbabilistic outcomes.\nOutput depends on probability amplitudes.",
    },
]


def render_comparison_module():
    """Renders Module D: Classical-to-Quantum Comparison Framework."""

    st.html("""
    <div class="hero-banner">
        <div class="hero-title">Module D: Classical ↔ Quantum Comparison</div>
        <div class="hero-subtitle">
            A structured framework mapping familiar semiconductor and digital concepts
            to their quantum computing counterparts — bridging the conceptual gap
            from <b>transistors</b> to <b>qubits</b>.
        </div>
    </div>
    """)

    tab_map, tab_levels, tab_noise = st.tabs([
        "🗺️ Concept Mapping Table",
        "📈 4-Level Learning Progression",
        "📡 Noise: Classical vs Quantum",
    ])

    # ── Tab 1: Concept Mapping Table ──────────────────────────────────
    with tab_map:
        st.markdown("### 🗺️ Classical Electronics → Quantum Computing: Concept Map")
        st.caption(
            "Every concept you already understand from transistors and logic gates "
            "has a direct quantum counterpart. Use this table as your conceptual bridge."
        )

        # Header row
        st.html("""
        <div class="concept-map-header">
            <div style="color:#38bdf8; font-weight:700; font-size:0.9rem;">⚡ Classical Concept</div>
            <div style="color:#94a3b8; font-weight:700; font-size:0.9rem; text-align:center;">🎓 What You Already Know</div>
            <div style="color:#a855f7; font-weight:700; font-size:0.9rem; text-align:right;">⚛️ Quantum Counterpart</div>
        </div>
        """)

        for i, row in enumerate(CONCEPT_MAP):
            bg = "rgba(15,23,42,0.6)" if i % 2 == 0 else "rgba(22,33,53,0.6)"
            st.html(f"""
            <div class="concept-map-row" style="background:{bg};">
                <div class="concept-col-classical">
                    <span style="font-size:1.1rem;">{row['classical_icon']}</span>
                    <span style="margin-left:6px;">{row['classical_concept']}</span>
                </div>
                <div class="concept-col-bridge">
                    {row['student_knows']}
                </div>
                <div class="concept-col-quantum">
                    <span style="font-size:1.1rem;">{row['quantum_icon']}</span>
                    <span style="margin-left:6px;">{row['quantum_counterpart']}</span>
                </div>
            </div>
            """)

        # Key differences summary
        st.markdown("---")
        st.markdown("#### 🔑 The Three Most Important Conceptual Leaps")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.html("""
            <div class="glass-card" style="padding:16px; text-align:center;">
                <div style="font-size:2rem;">🌀</div>
                <div style="color:#a855f7; font-weight:700; margin:8px 0;">Superposition</div>
                <div style="color:#94a3b8; font-size:0.85rem;">
                    A qubit can be 0 AND 1 simultaneously, unlike a transistor which must be
                    fully ON or fully OFF.
                </div>
            </div>
            """)
        with c2:
            st.html("""
            <div class="glass-card" style="padding:16px; text-align:center;">
                <div style="font-size:2rem;">🔗</div>
                <div style="color:#38bdf8; font-weight:700; margin:8px 0;">Entanglement</div>
                <div style="color:#94a3b8; font-size:0.85rem;">
                    Two qubits can be correlated instantly over any distance — no classical
                    circuit analogue exists.
                </div>
            </div>
            """)
        with c3:
            st.html("""
            <div class="glass-card" style="padding:16px; text-align:center;">
                <div style="font-size:2rem;">🎲</div>
                <div style="color:#f59e0b; font-weight:700; margin:8px 0;">Measurement Collapse</div>
                <div style="color:#94a3b8; font-size:0.85rem;">
                    Measuring a qubit destroys its superposition — the outcome is
                    probabilistic (Born rule), not deterministic.
                </div>
            </div>
            """)

    # ── Tab 2: 4-Level Progression ────────────────────────────────────
    with tab_levels:
        st.markdown("### 📈 The 4-Level Transistor-to-Qubit Learning Progression")
        st.caption("Each level builds on what you already know and introduces one new quantum concept.")

        for lvl in LEVELS:
            st.html(f"""
            <div style="border-left: 4px solid {lvl['color']}; padding: 0 0 0 16px; margin-bottom: 24px;">
                <div style="font-size:1.1rem; font-weight:700; color:{lvl['color']}; margin-bottom:12px;">
                    {lvl['title']}
                </div>
            </div>
            """)
            col_c, col_arrow, col_q = st.columns([2, 1, 2])
            with col_c:
                st.html(f"""
                <div style="background:rgba(34,197,94,0.08); border:1px solid rgba(34,197,94,0.3);
                            border-radius:10px; padding:14px; font-family:'JetBrains Mono', monospace;
                            color:#cbd5e1; font-size:0.85rem; white-space:pre-line; min-height:80px;">
⚡ CLASSICAL
{lvl['classical']}
                </div>
                """)
            with col_arrow:
                st.html(f"""
                <div class="level-arrow-box">
                    <div class="level-arrow-symbol" style="color:{lvl['color']};">→</div>
                    <div style="color:#94a3b8; font-size:0.75rem; margin-top:4px; font-style:italic;">
                        {lvl['transition']}
                    </div>
                </div>
                """)
            with col_q:
                st.html(f"""
                <div style="background:rgba(168,85,247,0.08); border:1px solid rgba(168,85,247,0.3);
                            border-radius:10px; padding:14px; font-family:'JetBrains Mono', monospace;
                            color:#d8b4fe; font-size:0.85rem; white-space:pre-line; min-height:80px;">
⚛️ QUANTUM
{lvl['quantum']}
                </div>
                """)
            # Level 2 doc guideline: link to quantum equivalent of NOT gate
            if lvl["id"] == 2:
                if st.button("⚛️ Explore X Gate (Quantum NOT) in Module 3 →", key="btn_lvl2_to_x"):
                    st.session_state["nav_module"] = "module3"
                    st.session_state["quantum_mode"] = "🔬 Single-Qubit Gate Explorer (X, H, Z, M)"
                    st.session_state["quantum_gate_choice"] = "X"
                    st.rerun()
            st.markdown("")

    # ── Tab 3: Noise Comparison ───────────────────────────────────────
    with tab_noise:
        _render_noise_tab()


def _render_noise_tab():
    """Renders the Classical vs Quantum Noise comparison section."""

    st.markdown("### 📡 Noise: Classical Transistor vs Quantum Decoherence")
    st.caption(
        "Both classical and quantum systems suffer from noise. "
        "But the nature of noise and its effects are fundamentally different."
    )

    # ── Section A: Classical transistor noise ─────────────────────────
    st.markdown("---")
    st.markdown("#### ⚡ Classical Noise: $V_{out} = V_{ideal} + n(t)$")

    col_ctrl, col_plot = st.columns([1, 2])
    with col_ctrl:
        st.markdown("**Noise Parameters:**")
        noise_sigma = st.slider(
            "Noise Standard Deviation σ (V)",
            min_value=0.0, max_value=1.5, value=0.25, step=0.05,
            key="noise_sigma",
        )
        v_ideal = st.select_slider(
            "Ideal Output Voltage (V)",
            options=[0.2, 2.5, 5.0],
            value=5.0,
            key="noise_videal",
        )
        n_samples = st.slider(
            "Number of Time Samples",
            min_value=50, max_value=400, value=150, step=50,
            key="noise_samples",
        )
        st.markdown("---")
        state_label = "HIGH (Logic 1)" if v_ideal > 2.5 else ("LOW (Logic 0)" if v_ideal < 1.0 else "Transition")
        logic_ok = noise_sigma < 1.0
        st.html(f"""
        <div class="glass-card" style="padding:12px 14px;">
            <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:4px;">Ideal State</div>
            <div style="color:#22c55e; font-weight:700; font-size:1rem;">{state_label}</div>
            <div style="color:#94a3b8; font-size:0.8rem; margin-top:8px; margin-bottom:4px;">Noise Immunity</div>
            <div style="color:{'#22c55e' if logic_ok else '#f43f5e'}; font-weight:700;">
                {'✅ Signal Intact (σ < 1V)' if logic_ok else '❌ Signal Corrupted (σ ≥ 1V)'}
            </div>
            <div style="color:#94a3b8; font-size:0.8rem; margin-top:8px;">
                Classical noise adds directly to voltage. Logic thresholds provide noise margins.
            </div>
        </div>
        """)

    with col_plot:
        np.random.seed(42)
        t = np.linspace(0, 1, n_samples)
        noise = np.random.normal(0, noise_sigma, n_samples)
        v_noisy = v_ideal + noise

        fig, ax = plt.subplots(figsize=(9, 3.2), facecolor="#090d16")
        ax.set_facecolor("#0f172a")
        ax.axhline(v_ideal, color="#38bdf8", linewidth=2, linestyle="--", label=f"V_ideal = {v_ideal:.1f} V", alpha=0.85)
        ax.fill_between(t, v_ideal - noise_sigma, v_ideal + noise_sigma,
                        color="#38bdf8", alpha=0.08, label=f"±σ = ±{noise_sigma:.2f} V noise band")
        ax.plot(t, v_noisy, color="#22c55e", linewidth=1.2, alpha=0.85, label="V_out = V_ideal + n(t)")
        ax.axhline(2.5, color="#f43f5e", linewidth=1.2, linestyle=":", alpha=0.7, label="Logic threshold (2.5 V)")
        ax.set_xlabel("Time (normalised)", color="#94a3b8", fontsize=10)
        ax.set_ylabel("Output Voltage (V)", color="#94a3b8", fontsize=10)
        ax.set_title("Classical Transistor Output with Additive Gaussian Noise", color="#f8fafc", fontsize=11, fontweight="bold")
        ax.legend(facecolor="#1e293b", edgecolor="#475569", labelcolor="#f8fafc", fontsize=9, loc="upper right")
        ax.tick_params(colors="#cbd5e1")
        ax.grid(True, linestyle="--", alpha=0.15, color="#ffffff")
        ax.set_ylim(-0.5, 6.5)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── Section B: Quantum noise / decoherence ────────────────────────
    st.markdown("---")
    st.markdown("#### ⚛️ Quantum Noise & Decoherence — Error Types")

    st.html("""
    <div style="background:rgba(168,85,247,0.07); border:1px solid rgba(168,85,247,0.25);
                border-radius:10px; padding:14px 18px; margin-bottom:16px; color:#cbd5e1; font-size:0.9rem;">
        In quantum systems, noise doesn't just add voltage — it rotates the qubit's state on the Bloch sphere,
        or destroys the phase coherence needed for superposition. This process is called <b>decoherence</b>
        and it is the primary reason why building large-scale quantum computers is so hard.
    </div>
    """)

    noise_cols = st.columns(3)
    noise_types = [
        {
            "name": "Bit-Flip Error",
            "symbol": "X",
            "color": "#f43f5e",
            "icon": "🔀",
            "description": "Randomly flips |0⟩ → |1⟩ or |1⟩ → |0⟩ with probability p.\nAnalogous to a glitch flipping a bit in RAM.",
            "formula": r"|\psi\rangle \xrightarrow{p} X|\psi\rangle",
            "classical_analogue": "Bit error in DRAM / cosmic-ray SEU",
        },
        {
            "name": "Phase-Flip Error",
            "symbol": "Z",
            "color": "#38bdf8",
            "icon": "🔄",
            "description": "Randomly applies a phase flip: |+⟩ → |−⟩.\nHas NO classical analogue — purely quantum.",
            "formula": r"|\psi\rangle \xrightarrow{p} Z|\psi\rangle",
            "classical_analogue": "No direct classical equivalent",
        },
        {
            "name": "Depolarising Noise",
            "symbol": "D",
            "color": "#f59e0b",
            "icon": "💫",
            "description": "With probability p, replaces qubit with a completely random mixed state.\nMost general single-qubit error channel.",
            "formula": r"\rho \xrightarrow{p} (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)",
            "classical_analogue": "Thermal noise destroying all signal information",
        },
    ]

    for col, nt in zip(noise_cols, noise_types):
        with col:
            st.html(f"""
            <div class="glass-card" style="padding:16px; border-left:3px solid {nt['color']}; min-height:220px;">
                <div style="font-size:1.5rem;">{nt['icon']}</div>
                <div style="color:{nt['color']}; font-weight:700; font-size:0.95rem; margin:6px 0;">
                    {nt['name']}
                </div>
                <div style="color:#94a3b8; font-size:0.8rem; margin-bottom:8px; white-space:pre-line;">
                    {nt['description']}
                </div>
                <div style="color:#64748b; font-size:0.75rem; font-style:italic;">
                    Classical analogue: {nt['classical_analogue']}
                </div>
            </div>
            """)

    # ── Section C: Probability under bit-flip noise ───────────────────
    st.markdown("---")
    st.markdown("#### 📊 Interactive: How Bit-Flip Probability Shifts Measurement Outcomes")

    col_l, col_r = st.columns([1, 2])
    with col_l:
        p_error = st.slider(
            "Bit-Flip Error Probability p",
            min_value=0.0, max_value=0.5, value=0.1, step=0.01,
            key="q_noise_p",
        )
        init_q = st.radio(
            "Initial Qubit State:",
            ["|0⟩", "|1⟩", "|+⟩ (superposition)"],
            key="q_noise_init",
        )
        shots = st.slider("Shots", 200, 2000, 1000, 100, key="q_noise_shots")

        p0_ideal = {"0": 1.0, "1": 0.0}  # ideal P(0)
        if init_q == "|0⟩":
            p0_noiseless = 1.0
        elif init_q == "|1⟩":
            p0_noiseless = 0.0
        else:
            p0_noiseless = 0.5

        # With bit-flip noise of probability p:
        # P'(0) = (1-p)*P_noiseless(0) + p*P_noiseless(1)
        p1_noiseless = 1.0 - p0_noiseless
        p0_noisy = (1 - p_error) * p0_noiseless + p_error * p1_noiseless
        p1_noisy = 1.0 - p0_noisy

        st.html(f"""
        <div class="glass-card" style="padding:12px 14px; margin-top:8px;">
            <div style="color:#94a3b8; font-size:0.78rem; margin-bottom:6px;">Without noise:</div>
            <div style="color:#22c55e; font-size:0.85rem;">P(|0⟩) = {p0_noiseless*100:.0f}%
             &nbsp; P(|1⟩) = {p1_noiseless*100:.0f}%</div>
            <div style="color:#94a3b8; font-size:0.78rem; margin-top:8px; margin-bottom:6px;">With p={p_error:.2f} noise:</div>
            <div style="color:#f59e0b; font-size:0.85rem;">P(|0⟩) = {p0_noisy*100:.1f}%
             &nbsp; P(|1⟩) = {p1_noisy*100:.1f}%</div>
            <div style="color:#64748b; font-size:0.75rem; margin-top:6px;">
                At p = 0.5, all information is destroyed (50/50).
            </div>
        </div>
        """)

    with col_r:
        np.random.seed(123)
        rng = np.random.default_rng(123)
        # Simulate ideal shots
        outcomes_ideal = rng.choice(["0", "1"], size=shots,
                                     p=[p0_noiseless, p1_noiseless] if p0_noiseless + p1_noiseless == 1
                                     else [0.5, 0.5])
        # Apply bit-flip noise
        flipped = rng.random(shots) < p_error
        outcomes_noisy = np.where(
            flipped,
            np.where(outcomes_ideal == "0", "1", "0"),
            outcomes_ideal,
        )

        c_ideal = {"0": int(np.sum(outcomes_ideal == "0")), "1": int(np.sum(outcomes_ideal == "1"))}
        c_noisy = {"0": int(np.sum(outcomes_noisy == "0")), "1": int(np.sum(outcomes_noisy == "1"))}

        fig, axes = plt.subplots(1, 2, figsize=(9, 3.2), facecolor="#090d16")
        for ax, counts, title, col in zip(
            axes,
            [c_ideal, c_noisy],
            ["Without Noise (Ideal)", f"With Bit-Flip Noise (p={p_error:.2f})"],
            ["#22c55e", "#f59e0b"],
        ):
            ax.set_facecolor("#0f172a")
            bars = ax.bar(["0", "1"], [counts.get("0", 0), counts.get("1", 0)],
                          color=col, edgecolor="#f8fafc", alpha=0.85, width=0.4)
            for bar in bars:
                h = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.0, h + 5,
                        f"{h/shots*100:.1f}%", ha="center", color="#f8fafc",
                        fontweight="bold", fontsize=10)
            ax.set_title(title, color="#f8fafc", fontsize=10, fontweight="bold")
            ax.set_ylabel("Counts", color="#94a3b8", fontsize=9)
            ax.set_ylim(0, shots * 1.2)
            ax.tick_params(colors="#cbd5e1")
            ax.grid(axis="y", linestyle="--", alpha=0.15, color="#ffffff")
        plt.suptitle("Quantum Measurement: Ideal vs Noisy", color="#f8fafc", fontsize=11, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    # ── Section D: Summary comparison table ──────────────────────────
    st.markdown("---")
    st.markdown("#### 📋 Classical Noise vs Quantum Noise — Side-by-Side")

    rows = [
        ("Type",           "Additive voltage noise: $V = V_{ideal} + n(t)$", "State rotation / decoherence on Bloch sphere"),
        ("Source",         "Thermal (Johnson), shot noise, electromagnetic interference", "Photons, phonons, stray magnetic fields, cosmic rays"),
        ("Effect",         "Shifts output voltage — may cross logic threshold", "Rotates qubit state — destroys superposition / phase"),
        ("Correction",     "Noise margins, filtering, shielding, error-checking", "Quantum error correction (Shor, Steane, surface codes)"),
        ("Reversible?",    "Mostly — can filter/amplify the signal", "No — measurement / decoherence collapse is irreversible"),
        ("Key metric",     "Signal-to-Noise Ratio (SNR)", "T₁ (relaxation time), T₂ (coherence time)"),
    ]
    header_style = "background:rgba(30,41,59,0.95); color:#cbd5e1; padding:8px 12px; font-weight:700; font-size:0.85rem; border-bottom:1px solid rgba(148,163,184,0.3);"
    row_styles   = [
        "background:rgba(15,23,42,0.7); padding:8px 12px; font-size:0.85rem; color:#94a3b8; border-bottom:1px solid rgba(255,255,255,0.05);",
        "background:rgba(22,33,53,0.7); padding:8px 12px; font-size:0.85rem; color:#94a3b8; border-bottom:1px solid rgba(255,255,255,0.05);",
    ]

    table_html = f"""
    <table style="width:100%; border-collapse:separate; border-spacing:0; border-radius:10px;
                  overflow:hidden; border:1px solid rgba(148,163,184,0.2);">
      <thead>
        <tr>
          <th style="{header_style}">Property</th>
          <th style="{header_style}; color:#22c55e;">⚡ Classical (Transistor) Noise</th>
          <th style="{header_style}; color:#a855f7;">⚛️ Quantum Noise / Decoherence</th>
        </tr>
      </thead>
      <tbody>
    """
    for i, (prop, cl, qu) in enumerate(rows):
        rs = row_styles[i % 2]
        table_html += f"""
        <tr>
          <td style="{rs} color:#38bdf8; font-weight:600;">{prop}</td>
          <td style="{rs} color:#22c55e;">{cl}</td>
          <td style="{rs} color:#a855f7;">{qu}</td>
        </tr>
        """
    table_html += "</tbody></table>"
    st.html(table_html)

    # ── Section E: Quantum Error Correction (3-Qubit Code) ───────────
    st.markdown("---")
    st.markdown("#### 🛡️ Quantum Error Correction: The 3-Qubit Bit-Flip Code")
    st.caption("How quantum computers overcome decoherence without violating the No-Cloning Theorem.")

    st.html("""
    <div style="background:rgba(56,189,248,0.06); border:1px solid rgba(56,189,248,0.25); border-radius:10px; padding:16px 20px; margin-bottom:18px;">
        <h5 style="color:#38bdf8; margin:0 0 8px 0;">Why Classical Error Correction Fails in Quantum Systems:</h5>
        <ul style="color:#cbd5e1; font-size:0.9rem; margin-bottom:0; padding-left:20px; line-height:1.6;">
            <li><b>No-Cloning Theorem:</b> You cannot make a copy of an unknown quantum state <code>|ψ⟩ → |ψ⟩|ψ⟩</code>.</li>
            <li><b>Measurement Destroys Information:</b> You cannot directly inspect a qubit to check for errors without collapsing its superposition.</li>
            <li><b>The Quantum Solution:</b> Instead of copying, we <i>entangle</i> the logical qubit with helper qubits: <code>|ψ⟩|00⟩ → α|000⟩ + β|111⟩</code>. 
            We measure only <b>syndrome parities</b> between qubits to locate the error without learning the state itself!</li>
        </ul>
    </div>
    """)

    col_qec_ctrl, col_qec_disp = st.columns([1, 2], gap="large")

    with col_qec_ctrl:
        st.markdown("**1. Select Logical Qubit Input:**")
        qec_input = st.radio(
            "Logical Input State:",
            ["|0⟩ (α=1, β=0)", "|1⟩ (α=0, β=1)", "|+⟩ (Equal Superposition)"],
            key="qec_input_state",
        )

        st.markdown("**2. Inject Noise Channel (Bit-Flip):**")
        noise_target = st.selectbox(
            "Bit-Flip Error Location:",
            ["None (No Noise)", "Flip Qubit 0 (q₀)", "Flip Qubit 1 (q₁)", "Flip Qubit 2 (q₂)"],
            key="qec_error_target",
        )

        st.markdown("---")
        st.markdown("**Syndrome Lookup Table:**")
        st.html("""
        <table style="width:100%; font-family:monospace; font-size:0.8rem; background:#0b1120; border:1px solid #334155; border-radius:6px;">
            <tr style="color:#94a3b8; border-bottom:1px solid #1e293b;">
                <th style="padding:4px 8px;">Syndrome (s₁s₂)</th>
                <th style="padding:4px 8px;">Diagnosis</th>
                <th style="padding:4px 8px;">Action</th>
            </tr>
            <tr style="color:#22c55e;">
                <td style="padding:4px 8px;">0 0</td>
                <td style="padding:4px 8px;">No Error</td>
                <td style="padding:4px 8px;">Do nothing</td>
            </tr>
            <tr style="color:#38bdf8;">
                <td style="padding:4px 8px;">1 0</td>
                <td style="padding:4px 8px;">Error on q₀</td>
                <td style="padding:4px 8px;">Apply X(q₀)</td>
            </tr>
            <tr style="color:#f59e0b;">
                <td style="padding:4px 8px;">1 1</td>
                <td style="padding:4px 8px;">Error on q₁</td>
                <td style="padding:4px 8px;">Apply X(q₁)</td>
            </tr>
            <tr style="color:#ec4899;">
                <td style="padding:4px 8px;">0 1</td>
                <td style="padding:4px 8px;">Error on q₂</td>
                <td style="padding:4px 8px;">Apply X(q₂)</td>
            </tr>
        </table>
        """)

    with col_qec_disp:
        # Determine syndrome and state progression
        if "None" in noise_target:
            error_q = -1
            syndrome = "00"
            diag = "No error detected"
            action = "None needed"
            badge_c = "#22c55e"
        elif "q₀" in noise_target:
            error_q = 0
            syndrome = "10"
            diag = "Bit-flip on Qubit 0 (q₀)"
            action = "Apply X gate to q₀"
            badge_c = "#38bdf8"
        elif "q₁" in noise_target:
            error_q = 1
            syndrome = "11"
            diag = "Bit-flip on Qubit 1 (q₁)"
            action = "Apply X gate to q₁"
            badge_c = "#f59e0b"
        else:
            error_q = 2
            syndrome = "01"
            diag = "Bit-flip on Qubit 2 (q₂)"
            action = "Apply X gate to q₂"
            badge_c = "#ec4899"

        # Format Dirac representations
        if "|0⟩" in qec_input:
            encoded_str = "|000⟩"
            if error_q == 0:
                noisy_str = "|100⟩"
            elif error_q == 1:
                noisy_str = "|010⟩"
            elif error_q == 2:
                noisy_str = "|001⟩"
            else:
                noisy_str = "|000⟩"
            recovered_str = "|000⟩ (Decodes to |0⟩)"
        elif "|1⟩" in qec_input:
            encoded_str = "|111⟩"
            if error_q == 0:
                noisy_str = "|011⟩"
            elif error_q == 1:
                noisy_str = "|101⟩"
            elif error_q == 2:
                noisy_str = "|110⟩"
            else:
                noisy_str = "|111⟩"
            recovered_str = "|111⟩ (Decodes to |1⟩)"
        else:
            encoded_str = "(|000⟩ + |111⟩)/√2"
            if error_q == 0:
                noisy_str = "(|100⟩ + |011⟩)/√2"
            elif error_q == 1:
                noisy_str = "(|010⟩ + |101⟩)/√2"
            elif error_q == 2:
                noisy_str = "(|001⟩ + |110⟩)/√2"
            else:
                noisy_str = "(|000⟩ + |111⟩)/√2"
            recovered_str = "(|000⟩ + |111⟩)/√2 (Decodes to |+⟩)"

        st.html(f"""
        <div class="glass-card" style="padding:18px 22px;">
            <div style="font-size:0.85rem; color:#94a3b8; text-transform:uppercase; margin-bottom:12px;">Step-by-Step Quantum Error Correction Pipeline</div>
            
            <div style="display:flex; flex-direction:column; gap:12px; font-family:'JetBrains Mono', monospace; word-break:break-word;">
                <div style="background:rgba(30,41,59,0.7); padding:10px 14px; border-radius:8px; border-left:3px solid #38bdf8;">
                    <span style="color:#94a3b8; font-size:0.8rem;">1. ENCODING (CNOT gates):</span><br/>
                    <b style="color:#38bdf8; font-size:1.1rem;">|ψ_encoded⟩ = {encoded_str}</b>
                </div>
                
                <div style="background:rgba(30,41,59,0.7); padding:10px 14px; border-radius:8px; border-left:3px solid {'#22c55e' if error_q == -1 else '#f43f5e'};">
                    <span style="color:#94a3b8; font-size:0.8rem;">2. NOISY CHANNEL (Bit-flip strike):</span><br/>
                    <b style="color:{'#22c55e' if error_q == -1 else '#f43f5e'}; font-size:1.1rem;">|ψ_noisy⟩ = {noisy_str}</b>
                </div>

                <div style="background:rgba(30,41,59,0.7); padding:10px 14px; border-radius:8px; border-left:3px solid {badge_c};">
                    <span style="color:#94a3b8; font-size:0.8rem;">3. SYNDROME MEASUREMENT (Ancilla parities):</span><br/>
                    <span style="color:#f8fafc;">Measured syndrome <b>s₁s₂ = {syndrome}</b> &rarr; <span style="color:{badge_c}; font-weight:bold;">{diag}</span></span>
                </div>

                <div style="background:rgba(34,197,94,0.12); padding:10px 14px; border-radius:8px; border:1px solid rgba(34,197,94,0.5);">
                    <span style="color:#94a3b8; font-size:0.8rem;">4. RECOVERY CORRECTION (Targeted Pauli-X):</span><br/>
                    <span style="color:#cbd5e1; font-size:0.85rem;">Action: {action}</span><br/>
                    <b style="color:#4ade80; font-size:1.15rem;">|ψ_recovered⟩ = {recovered_str} &bull; 100% RECOVERED! 🎉</b>
                </div>
            </div>
        </div>
        """)
