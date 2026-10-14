"""
Quantum computing utilities and Qiskit integration for Module 3.
Provides circuit synthesis, statevector extraction, Bloch sphere plotting,
Aer measurement simulation, and mathematical representations.
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit.visualization.bloch import Bloch
from qiskit.visualization.state_visualization import _bloch_multivector_data

try:
    from qiskit_aer import AerSimulator
    AER_AVAILABLE = True
except (ImportError, Exception):
    AerSimulator = None
    AER_AVAILABLE = False

# Gate matrix representations
GATE_MATRICES = {
    "X": {
        "name": "Pauli-X Gate (Bit-Flip / Quantum NOT)",
        "symbol": "X",
        "matrix": np.array([[0, 1], [1, 0]], dtype=complex),
        "latex": r"X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}",
        "formula": r"X|0\rangle = |1\rangle,\quad X|1\rangle = |0\rangle",
        "description": "Performs a π rotation around the X-axis of the Bloch sphere. Flips |0⟩ to |1⟩ and vice versa.",
    },
    "H": {
        "name": "Hadamard Gate (Superposition Creator)",
        "symbol": "H",
        "matrix": np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]], dtype=complex),
        "latex": r"H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}",
        "formula": r"H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle,\quad H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = |-\rangle",
        "description": "Creates an equal superposition state between |0⟩ and |1⟩ with equal probability (50% |0⟩, 50% |1⟩).",
    },
    "Z": {
        "name": "Pauli-Z Gate (Phase-Flip)",
        "symbol": "Z",
        "matrix": np.array([[1, 0], [0, -1]], dtype=complex),
        "latex": r"Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}",
        "formula": r"Z|0\rangle = |0\rangle,\quad Z|1\rangle = -|1\rangle,\quad Z|+\rangle = |-\rangle",
        "description": "Performs a π rotation around the Z-axis of the Bloch sphere. Leaves |0⟩ unchanged and inverts phase of |1⟩ to -|1⟩.",
    },
    "CNOT": {
        "name": "Controlled-NOT Gate (CX / Entangler)",
        "symbol": "CX",
        "matrix": np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex),
        "latex": r"CNOT = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}",
        "formula": r"CNOT|c, t\rangle = |c, t \oplus c\rangle",
        "description": "Two-qubit gate: flips the target qubit if and only if the control qubit is |1⟩. Generates maximal entanglement (Bell states).",
    },
    "M": {
        "name": "Quantum Measurement",
        "symbol": "M",
        "matrix": None,
        "latex": r"\hat{M}_0 = |0\rangle\langle 0|,\quad \hat{M}_1 = |1\rangle\langle 1|",
        "formula": r"P(0) = |\langle 0|\psi\rangle|^2,\quad P(1) = |\langle 1|\psi\rangle|^2",
        "description": "Collapses the quantum superposition state irreversibly into a definite classical computational state |0⟩ or |1⟩.",
    }
}


def build_single_qubit_circuit(initial_state="|0⟩", gate="X", with_measurement=True):
    """
    Constructs a 1-qubit circuit with initial state preparation, applied gate, and optional measurement.
    Returns:
    - qc_state: circuit without measurement (for statevector and Bloch calculation)
    - qc_meas: circuit with measurement (for circuit diagram and Aer simulation)
    """
    qc_state = QuantumCircuit(1)
    
    # State preparation
    if initial_state == "|1⟩":
        qc_state.x(0)
    elif initial_state == "|+⟩":
        qc_state.h(0)
    elif initial_state == "|-⟩":
        qc_state.x(0)
        qc_state.h(0)
        
    # Apply selected gate
    if gate == "X":
        qc_state.x(0)
    elif gate == "H":
        qc_state.h(0)
    elif gate == "Z":
        qc_state.z(0)
    elif gate == "M":
        pass  # Measurement is handled in qc_meas

    # Create circuit copy with measurement
    qc_meas = QuantumCircuit(1, 1)
    if initial_state == "|1⟩":
        qc_meas.x(0)
    elif initial_state == "|+⟩":
        qc_meas.h(0)
    elif initial_state == "|-⟩":
        qc_meas.x(0)
        qc_meas.h(0)

    if gate == "X":
        qc_meas.x(0)
    elif gate == "H":
        qc_meas.h(0)
    elif gate == "Z":
        qc_meas.z(0)
        
    if with_measurement or gate == "M":
        qc_meas.measure(0, 0)

    return qc_state, qc_meas


def build_two_qubit_cnot_circuit(ctrl_state="|0⟩", tgt_state="|0⟩", superpose_ctrl=False, with_measurement=True):
    """
    Constructs a 2-qubit CNOT circuit.
    control qubit = q0, target qubit = q1.
    If superpose_ctrl is True, applies H to q0 to generate Bell State!
    """
    qc_state = QuantumCircuit(2)
    
    # Prepare Control Qubit q0
    if ctrl_state == "|1⟩":
        qc_state.x(0)
    if superpose_ctrl:
        qc_state.h(0)
        
    # Prepare Target Qubit q1
    if tgt_state == "|1⟩":
        qc_state.x(1)
        
    # Apply CNOT: q0 is control, q1 is target
    qc_state.cx(0, 1)

    # Circuit with measurement
    qc_meas = QuantumCircuit(2, 2)
    if ctrl_state == "|1⟩":
        qc_meas.x(0)
    if superpose_ctrl:
        qc_meas.h(0)
    if tgt_state == "|1⟩":
        qc_meas.x(1)
    qc_meas.cx(0, 1)

    if with_measurement:
        qc_meas.measure([0, 1], [0, 1])

    return qc_state, qc_meas


def format_statevector_latex(sv: Statevector, num_qubits=1, as_latex=False):
    """
    Converts a statevector into a formatted Dirac bra-ket string.
    By default returns clean unicode Dirac notation (e.g. |0⟩, |1⟩)
    suitable for direct HTML and markdown rendering.
    """
    terms = []
    data = sv.data
    dim = len(data)
    ket_close = r"\rangle" if as_latex else "⟩"
    
    for idx in range(dim):
        amp = data[idx]
        if np.abs(amp) > 1e-4:
            # Binary string representation
            bin_str = format(idx, f"0{num_qubits}b")
            
            # Format amplitude
            real_part = np.real(amp)
            imag_part = np.imag(amp)
            
            if np.abs(imag_part) < 1e-4:
                coeff = f"{real_part:.3f}"
            elif np.abs(real_part) < 1e-4:
                coeff = f"{imag_part:.3f}i"
            else:
                sign = "+" if imag_part > 0 else "-"
                coeff = f"({real_part:.3f} {sign} {abs(imag_part):.3f}i)"
                
            if coeff == "1.000":
                terms.append(f"|{bin_str}{ket_close}")
            elif coeff == "-1.000":
                terms.append(f"-|{bin_str}{ket_close}")
            else:
                terms.append(f"{coeff}|{bin_str}{ket_close}")
                
    if not terms:
        return f"|0{ket_close}"
    return " + ".join(terms).replace("+ -", "- ")


def draw_circuit_mpl(qc: QuantumCircuit):
    """
    Draws a QuantumCircuit using matplotlib drawer.
    Applies styling for clean visualization.
    """
    style = {
        "backgroundcolor": "#090d16",
        "linecolor": "#94a3b8",
        "textcolor": "#f8fafc",
        "gatetextcolor": "#f8fafc",
        "subtextcolor": "#cbd5e1",
        "dpi": 150,
    }
    try:
        fig = qc.draw(output="mpl", style=style)
        fig.patch.set_facecolor("#090d16")
        return fig
    except Exception as e:
        # Fallback to standard draw
        fig = qc.draw(output="mpl")
        fig.patch.set_facecolor("#090d16")
        return fig


def draw_bloch_sphere(sv: Statevector):
    """
    Renders an aesthetically styled Bloch sphere multivector for the given Statevector.
    Features dark-theme styling and crisp, non-colliding Dirac-notation labels:
    - North Pole: |0⟩ (+z)
    - South Pole: |1⟩ (-z)
    - Equatorial: |+⟩ (+x), |−⟩ (-x), |i⟩ (+y), |-i⟩ (-y)
    """
    try:
        bloch_data = _bloch_multivector_data(sv)
        num = len(bloch_data)
        fig = plt.figure(figsize=(4.8 * num, 4.8), facecolor="#090d16")
        for i, b_vec in enumerate(bloch_data):
            ax = fig.add_subplot(1, num, i + 1, projection="3d")
            ax.set_facecolor("#090d16")

            b = Bloch(axes=ax, font_size=11)
            b.font_color = "#f1f5f9"
            b.frame_color = "#64748b"
            b.sphere_color = "#38bdf8"
            b.sphere_alpha = 0.08
            b.vector_color = ["#00f0ff"]

            # Crystal-clear cardinal labels
            b.zlabel = ["|0⟩ (+z)", "|1⟩ (-z)"]
            b.xlabel = ["|+⟩ (+x)", "|−⟩ (-x)"]
            b.ylabel = ["|i⟩ (+y)", "|-i⟩ (-y)"]

            # Position labels clearly outside the sphere without overlapping
            b.zlpos = [1.28, -1.28]
            b.xlpos = [1.32, -1.32]
            b.ylpos = [1.32, -1.32]

            b.add_vectors(b_vec)
            b.render(title="")
            if num > 1:
                ax.set_title(f"Qubit {i} (q{i})", color="#38bdf8", fontsize=12, fontweight="bold", y=1.18)
        fig.tight_layout()
        return fig
    except Exception:
        # Fallback to default Qiskit plot_bloch_multivector
        fig = plot_bloch_multivector(sv)
        fig.patch.set_facecolor("#090d16")
        for ax in fig.axes:
            ax.set_facecolor("#090d16")
        return fig


def _simulate_with_statevector(qc_meas: QuantumCircuit, shots=1024):
    """Fallback simulation using Statevector sampling when AerSimulator is unavailable."""
    try:
        qc_no_meas = qc_meas.remove_final_measurements(inplace=False)
        sv = Statevector.from_instruction(qc_no_meas)
        raw_counts = sv.sample_counts(shots=shots)
        return {str(k): int(v) for k, v in raw_counts.items()}
    except Exception:
        return {"0": shots}


def run_aer_simulation(qc_meas: QuantumCircuit, shots=1024):
    """
    Executes circuit on AerSimulator (or falls back to Statevector sampling if Aer is unavailable)
    and returns measurement counts dictionary and histogram figure.
    """
    counts = None
    if AER_AVAILABLE and AerSimulator is not None:
        try:
            sim = AerSimulator()
            result = sim.run(qc_meas, shots=shots).result()
            counts = result.get_counts()
        except Exception:
            counts = None

    if counts is None:
        counts = _simulate_with_statevector(qc_meas, shots=shots)
    
    # Custom colored histogram
    fig, ax = plt.subplots(figsize=(6, 3.5), facecolor="#090d16")
    ax.set_facecolor("#0f172a")
    
    labels = sorted(list(counts.keys()))
    values = [counts[k] for k in labels]
    percentages = [v / shots * 100 for v in values]
    
    bars = ax.bar(labels, values, color="#38bdf8", edgecolor="#00f0ff", width=0.45, alpha=0.9)
    
    ax.set_ylabel("Shot Counts", color="#94a3b8", fontsize=11)
    ax.set_title(f"Measurement Outcomes ({shots} Shots)", color="#f8fafc", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#cbd5e1")
    ax.grid(axis="y", linestyle="--", alpha=0.15, color="#ffffff")
    
    # Annotate percentage above bars
    for bar, pct in zip(bars, percentages):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, height + 15, f"{pct:.1f}%",
                ha="center", va="bottom", color="#38bdf8", fontweight="bold", fontsize=10)
        
    ax.set_ylim(0, max(values) * 1.25 + 20)
    plt.tight_layout()
    return counts, fig
