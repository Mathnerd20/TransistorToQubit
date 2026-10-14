# ⚡ TransistorToQubit: The Evolution of Computing

An interactive web application built with **Streamlit**, **Qiskit**, **NumPy**, and **Matplotlib** that visualizes the progression of computation from solid-state semiconductors to classical digital logic and quantum superposition.

---

## 🚀 Quick Start

Activate the conda environment and run the Streamlit app:

```bash
conda activate edc
streamlit run app.py
```

Or run directly with conda:

```bash
conda run -n edc streamlit run app.py
```

The web application will open at `http://localhost:8501`.

---

## 📦 Architecture & Modules

### 🔌 Module 1: Transistor Switching (Physical Layer)
- **Bidirectional Controls**: Synchronized sliders and manual numeric text inputs for:
  - Base/Gate Voltage ($V_{in}$)
  - Collector/Drain Current limit ($I_{C,max}$)
  - Switching Threshold ($V_{th}$, adjustable for BJT at 0.7V or MOSFET at 2.0V)
  - Load Resistance ($R_L$)
  - Collector Supply Voltage ($V_{CC}$)
- **Semiconductor Physics Engine**:
  - **Cutoff (OFF)**: $V_{in} < V_{th}$, $I_C = 0$, $V_{out} = V_{CC}$ (Logic 1 / HIGH), Switch OPEN.
  - **Saturation (ON)**: $V_{in} \ge V_{th}$, $I_C = I_{C,sat}$, $V_{out} \approx 0.2\,\text{V}$ (Logic 0 / LOW), Switch CLOSED.
  - **Active Region**: Linear amplification & transition slope.
- **Visual Circuit Diagram (SVG)**:
  - NPN Common-Emitter switch schematic with dynamic current flow arrows, voltage probes, and equivalent switch diagram.
- **Analytical Plots**:
  - Voltage Transfer Characteristic (VTC: $V_{out}$ vs $V_{in}$) with operating point marker.
  - DC Load Line ($I_C$ vs $V_{CE}$) with dynamic Q-point.

---

### 🔲 Module 2: Classical Logic Gates (Gate Layer)
- **6 Supported Gates**: `NOT`, `AND`, `OR`, `NAND`, `NOR`, `XOR`.
- **Interactive Inputs**: Toggle inputs $A$ and $B$ (0 or 1).
- **Dual Circuit Schematics**:
  1. **IEEE Standard Logic Gate Symbol**: Clean vector graphic with real-time green/slate wire signaling.
  2. **Transistor-Level Silicon Schematic**: Shows actual NPN switching arrangements (series pull-down for NAND, parallel pull-down for NOR, inverter stages, and pass-transistor logic for XOR).
- **Interactive Truth Table**: Dynamically highlights the active row corresponding to current inputs.
- **All-Gate Comparator**: Side-by-side output comparison for all 6 gates simultaneously.

---

### ⚛️ Module 3: Quantum Gates & Circuits (Quantum Layer)
- **Quantum Gates & States**:
  - Input States: $|0\rangle$, $|1\rangle$, $|+\rangle$, $|-\rangle$
  - Single-Qubit Gates: **Pauli-X** (Bit-Flip / Quantum NOT), **Hadamard (H)** (Superposition), **Pauli-Z** (Phase-Flip), **Measurement (M)**
  - Two-Qubit Gates: **CNOT (Controlled-NOT)** with Bell State entanglement generation ($|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$)
- **High-Fidelity Qiskit Visualizations**:
  - Circuit diagrams rendered via `qc.draw('mpl')`.
  - Statevectors in Dirac bra-ket notation ($|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$).
  - **3D Bloch Sphere Representation** (`plot_bloch_multivector`).
  - **AerSimulator Quantum Simulation**: Real-time wave-function collapse sampling (1024 shots) with measurement probability histograms.
- **Custom Circuit Builder**: Add and chain arbitrary quantum gate sequences ($H, X, Z, CNOT, M$).

---

## 🧪 Testing

To run the automated verification suite:

```bash
conda run -n edc python tests/test_app.py
```
