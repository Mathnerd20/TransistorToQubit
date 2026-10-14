# From Transistors to Qubits: A Hybrid Learning Framework for Understanding Quantum Computing through Semiconductor Concepts

**Course / Context:** EDC Assignment #2: Research Problem & Practical Implementation  
**Project Repository:** `TransistorToQubit`  
**Deployment Platform:** Streamlit Cloud & Qiskit Aer Engine  
**Author:** Student Solution & Implementation Report  
**Date:** October 2026  

---

## Executive Summary

Students possessing foundational knowledge in semiconductor devices and classical digital logic frequently encounter an intimidating conceptual chasm when introduced to quantum information processing. Classical computing pedagogy is built on deterministic binary voltages, non-destructive voltage sensing, and static Boolean truth tables. Conversely, quantum mechanics introduces non-orthogonal vector superpositions, complex probability amplitudes, irreversible projective measurement collapse, and quantum entanglement.

This report documents the design, mathematical modeling, and software implementation of **TransistorToQubit** — an educational simulation and conceptual bridging framework. The framework maps familiar electronic concepts (transistor cutoff/saturation, BJT inverter circuits, standard logic gates) directly to their quantum counterparts (qubits, Bloch sphere statevectors, unitary quantum gates, Born-rule measurement, and quantum decoherence).

---

## 1. Pedagogical Problem & 4-Level Learning Progression

### 1.1 The Conceptual Gap in Quantum Education
Conventional quantum computing curricula often approach the subject either through abstract linear algebra or postulate-heavy quantum physics. Engineering students trained in electronics understand:
- A physical transistor operating as an open or closed switch.
- Binary voltage rails ($0\,\text{V} \leftrightarrow \text{Logic } 0$, $5\,\text{V} \leftrightarrow \text{Logic } 1$).
- Deterministic logic operations ($A \land B$, $\neg A$).
- Non-destructive oscilloscope / voltmeter probing.

When presented with quantum computing, these students struggle with:
1. **The physical-to-state transition:** Why a bit is no longer a physical voltage rail, but a complex unit vector $|\psi\rangle \in \mathbb{C}^2$.
2. **The gate transition:** Why quantum gates are unitary matrices ($U^\dagger U = I$) rather than irreversible silicon logic paths.
3. **The measurement paradox:** Why reading an output alters the physical system irrevocably.

### 1.2 The Four-Level Progression Framework
To systematically eliminate this conceptual gap, the platform establishes a structured four-level curriculum:

```
Level 1: Transistor Switch  ───>  Level 2: Logic Gate  ───>  Level 3: Bit to Qubit  ───>  Level 4: Circuits & Systems
(Cutoff vs Saturation             (Inverter NOT Gate            (Superposition                  (Deterministic Gates vs
 0 V vs 5 V)                       Transistor Topology)          |ψ⟩ = α|0⟩ + β|1⟩)              Unitary Ops + Collapse)
```

- **Level 1 — Transistor Switch:** The student observes how varying base voltage $V_{in}$ drives an NPN BJT between Cutoff ($V_{out} \approx 5\,\text{V} \to \text{Logic } 1$) and Saturation ($V_{out} \approx 0.2\,\text{V} \to \text{Logic } 0$), establishing the physical basis of binary abstraction.
- **Level 2 — Logic Gate (NOT $\leftrightarrow$ Pauli-X):** The classical inverter is explored at both the IEEE symbol level and the silicon transistor schematic level. A direct pedagogical bridge links this operation to the quantum Pauli-X bit-flip gate ($X|0\rangle = |1\rangle$, $X|1\rangle = |0\rangle$).
- **Level 3 — Bit $\to$ Qubit (Superposition):** The strict dichotomy $b \in \{0, 1\}$ is generalized into $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ with $|\alpha|^2 + |\beta|^2 = 1$. The Hadamard gate ($H$) is introduced to demonstrate equal-probability superpositions ($50\% / 50\%$) that possess no classical analogue.
- **Level 4 — Classical Circuit vs Quantum Circuit:** Classical deterministic gate cascades are contrasted against quantum circuits where unitary evolution preserves quantum phase until irreversible measurement collapse occurs.

---

## 2. Concept Mapping: Classical Electronics to Quantum Computing

The platform embodies the following 10-point conceptual dictionary:

| # | Classical Electronics Concept | What the Student Knows | Quantum Counterpart | Key Distinction |
|---|---|---|---|---|
| **1** | **Transistor** | Physical electronic switching device | **Qubit** | Transistors are classical physical switches; qubits are 2-level quantum information carriers. |
| **2** | **ON / OFF** | Binary voltage levels ($0\,\text{V}$ / $5\,\text{V}$) | **Measurement Collapse** | Measurement forces a continuous superposition into a discrete classical outcome ($0$ or $1$). |
| **3** | **Voltage / Current State** | Continuous physical signals carrying data | **Statevector / Amplitudes** | Quantum state $|\psi\rangle$ is a complex probability amplitude vector with phase information. |
| **4** | **Logic Gate** | Deterministic Boolean truth-table mapping | **Quantum Gate** | Quantum gates are reversible unitary transformations preserving norm ($U^\dagger U = I$). |
| **5** | **NOT Gate** | Physical inverter ($0 \to 1, 1 \to 0$) | **Pauli-X Gate** | Performs bit-flip on basis states ($X|0\rangle = |1\rangle$, $X|1\rangle = |0\rangle$), but also acts linearly on superpositions. |
| **6** | **Digital Circuit** | Interconnected classical logic gates | **Quantum Circuit** | Sequential unitary operations exploiting superposition and interference prior to measurement. |
| **7** | **Classical Bit** | Definite scalar: $b \in \{0, 1\}$ | **Qubit State** | Unit vector in Hilbert space: $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ with $\alpha, \beta \in \mathbb{C}$. |
| **8** | **Measurement** | Non-destructive readout via voltmeter | **Projective Measurement** | Projective collapse governed by Born's rule ($P(i) = \|\langle i\|\psi\rangle\|^2$); permanently destroys superposition. |
| **9** | **Noise** | Additive voltage fluctuations ($V + n(t)$) | **Decoherence / Quantum Noise** | Non-unitary environmental coupling causing phase damping, bit flips, and state entanglement with the bath. |
| **10** | **Determinism** | Identical inputs strictly yield identical outputs | **Probabilistic Measurement** | Deterministic statevector evolution, but intrinsically probabilistic measurement sampling. |

---

## 3. Platform Architecture & Technical Implementation

The software is implemented in Python utilizing Streamlit for reactive web delivery, pure SVG vector rendering for circuit schematics, and IBM's Qiskit Aer simulator for high-fidelity quantum execution.

### 3.1 Module 1: Transistor Switching Simulation (Physical Layer)
Module 1 models an NPN BJT in common-emitter configuration with a resistive collector pull-up:
- **Base Input Voltage ($V_{in}$):** Adjustable from $0.0\,\text{V}$ to $6.0\,\text{V}$.
- **Switching Threshold ($V_{th} / V_{BE(on)}$):** Nominal $0.7\,\text{V}$ for silicon BJT.
- **Collector Load Resistance ($R_L$):** Variable load from $100\,\Omega$ to $10{,}000\,\Omega$.
- **Current Limit ($I_{C,max}$):** Transistor collector rating ($1.0\,\text{mA}$ to $50.0\,\text{mA}$).
- **Fixed Logic Rail ($V_{CC}$):** Hardcoded to $5.0\,\text{V}$ representing TTL digital rail standards.

#### Mathematical Model
The base current $I_B$ is modeled as:
$$I_B = \begin{cases} 0 & \text{if } V_{in} \le V_{th} \\ \frac{V_{in} - V_{th}}{R_B} & \text{if } V_{in} > V_{th} \end{cases}$$
where $R_B = 10\,\text{k}\Omega$. The active collector current is $I_{C,\text{active}} = \beta \cdot I_B$ ($\beta = 100$). The maximum current allowed by the collector circuit load line is:
$$I_{C,\text{sat}} = \frac{V_{CC} - V_{CE,\text{sat}}}{R_L}$$
with $V_{CE,\text{sat}} = 0.2\,\text{V}$. The operating state is categorized as:
1. **Cutoff ($V_{in} \le V_{th}$):** $I_C = 0\,\text{mA}$, $V_{out} = V_{CC} = 5.0\,\text{V} \implies \text{Logic } 1$ (Open switch).
2. **Active / Transition ($I_{C,\text{active}} < I_{C,\text{sat}}$):** $I_C = I_{C,\text{active}}$, $V_{out} = V_{CC} - I_C R_L$.
3. **Saturation ($I_{C,\text{active}} \ge I_{C,\text{sat}}$):** $I_C = \min(I_{C,\text{sat}}, I_{C,max})$, $V_{out} = V_{CE,\text{sat}} \approx 0.2\,\text{V} \implies \text{Logic } 0$ (Closed switch).

The user interface renders live interactive SVG schematics with color-coded current paths and dynamic status badges.

### 3.2 Module 2: Classical Logic Gates (Gate Layer)
Module 2 implements the six canonical gates specified by the project: **NOT, AND, OR, NAND, NOR, and XOR**.
- **Dual Visual Representation:** Users can toggle between standard IEEE 91-1984 logic gate symbols and physical Resistor-Transistor Logic (RTL) transistor-level schematics.
- **Dynamic Truth Tables:** Rendered via isolated HTML iframe components with active-input row highlighting ($A, B \to Q$).
- **Contextual Bridge Navigation:** To maintain pedagogical continuity, when the user selects the NOT gate, an embedded callout card and navigation button appear:
  $$\text{NOT } 0 = 1 \iff X|0\rangle = |1\rangle$$
  Clicking the button programmatically switches the session state to Module 3 with the Pauli-X gate pre-selected.

### 3.3 Module 3: Quantum Gates & Circuits (Quantum Layer)
Module 3 is built directly on Qiskit 1.x and Qiskit Aer:
- **Basis States:** Selectable initial computational basis states $|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$ and $|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$.
- **Quantum Gates:**
  - **Pauli-X (Bit-flip):** $X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$, $X|0\rangle = |1\rangle$, $X|1\rangle = |0\rangle$.
  - **Hadamard (Superposition):** $H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$, $H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle$.
  - **Pauli-Z (Phase-flip):** $Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$, $Z|0\rangle = |0\rangle$, $Z|1\rangle = -|1\rangle$.
  - **Controlled-NOT (CNOT):** $CX = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix}$. When applied to $H|0\rangle \otimes |0\rangle$, it produces the maximally entangled Bell state:
    $$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$
- **Bloch Sphere Geometric Representation:** Renders the 3D Bloch sphere with Dirac notation labels on all cardinal axes ($|0\rangle$ at North Pole, $|1\rangle$ at South Pole, $|+\rangle, |-\rangle, |i\rangle$ along the equatorial plane).
- **Aer Measurement Simulation:** Executes projective measurements over selectable shot budgets ($128$ to $4096$ shots), displaying empirical probability histograms validating the theoretical Born rule:
  $$P(m) = |\langle m|\psi\rangle|^2$$

### 3.4 Module D: Comparison & Noise Analysis Framework
Module D provides the cross-domain comparative framework and deep-dive noise analysis:
- **Concept Map Tab:** Displays the full 10-row bridging table with visual cards for Superposition, Entanglement, and Measurement Collapse.
- **4-Level Learning Progression Tab:** Features step-by-step interactive cards for Levels 1–4, including an inline transition link from Level 2 directly to the X-gate quantum explorer.
- **Classical vs Quantum Noise Tab:**
  - **Classical Model:** Simulates $V_{out}(t) = V_{\text{ideal}} + n(t)$ where $n(t) \sim \mathcal{N}(0, \sigma^2)$. Demonstrates how digital noise margins preserve the logical state until $\sigma \ge 1.0\,\text{V}$.
  - **Quantum Noise Models:** Details bit-flip ($X$), phase-flip ($Z$), and depolarizing error channels:
    $$\rho \to (1-p)\rho + \frac{p}{3}(X\rho X + Y\rho Y + Z\rho Z)$$
  - **Interactive 3-Qubit Bit-Flip Quantum Error Correction (QEC):** Implements an interactive simulator demonstrating how encoding $|\psi\rangle \to \alpha|000\rangle + \beta|111\rangle$ allows syndrome detection ($s_1 s_2$) and targeted recovery ($X_i$) without measuring or collapsing the underlying logical state.

---

## 4. Deep-Dive: Classical Noise vs Quantum Decoherence

### 4.1 Classical Noise Immunity (Noise Margins)
In classical digital electronics, transistors operate in saturation and cutoff to establish wide noise margins:
$$NM_H = V_{OH,\min} - V_{IH,\min}, \quad NM_L = V_{IL,\max} - V_{OL,\max}$$
Voltage perturbations smaller than the noise margin are automatically suppressed at subsequent inverter stages due to the highly non-linear, high-gain transfer curve of the transistor. The system is naturally robust.

### 4.2 Quantum Decoherence & The No-Cloning Barrier
In quantum systems, noise is fundamentally non-additive:
1. **Continuous State Space:** Any infinitesimal phase drift $\theta$ transforms $|\psi\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} \to \frac{|0\rangle + e^{i\theta}|1\rangle}{\sqrt{2}}$, corrupting quantum information continuously.
2. **No-Cloning Theorem:** In classical electronics, signals are amplified and refreshed by copying ($x \to x, x$). In quantum mechanics, an unknown quantum state cannot be duplicated:
   $$U(|\psi\rangle|0\rangle) \neq |\psi\rangle|\psi\rangle \quad \forall |\psi\rangle$$
3. **Measurement Collapse:** One cannot inspect a qubit to determine whether an error has occurred without projecting the state and destroying the superposition.

### 4.3 Quantum Error Correction Resolution
The platform illustrates how the 3-qubit bit-flip code resolves this dilemma:
- **Entanglement Encoding:** Ancilla qubits are entangled with the data qubit:
  $$(\alpha|0\rangle + \beta|1\rangle)|00\rangle \xrightarrow{CNOT} \alpha|000\rangle + \beta|111\rangle$$
- **Parity Syndrome Measurement:** Measuring operator observables $Z_0 Z_1$ and $Z_1 Z_2$ extracts the error syndrome $s_1 s_2 \in \{00, 10, 11, 01\}$ without revealing the amplitudes $\alpha$ and $\beta$.
- **Targeted Correction:** A Pauli-X operator is applied to the corrupted qubit, restoring the logical state with $100\%$ fidelity.

---

## 5. Experimental Verification & Results

| Feature / Criterion | Assignment Doc Specification | Implementation Result | Verification Status |
|---|---|---|---|
| **Transistor Input Voltage** | Variable Base/Gate Voltage | $V_{in}$ slider ($0$ to $6\,\text{V}$) with manual numeric box | **Passed** |
| **Switching Threshold** | Variable $V_{th}$ | $V_{th}$ slider ($0.1$ to $4.0\,\text{V}$) | **Passed** |
| **Load Resistance** | Variable $R_L$ | $R_L$ slider ($100\,\Omega$ to $10\,\text{k}\Omega$) | **Passed** |
| **Collector Current Limit** | Variable $I_{C,max}$ | $I_{C,max}$ slider ($1$ to $50\,\text{mA}$) | **Passed** |
| **Canonical Logic Gates** | NOT, AND, OR, NAND, NOR, XOR | All 6 implemented with IEEE symbols & RTL circuits | **Passed** |
| **Quantum Basis States** | $|0\rangle, |1\rangle$ | Selectable in Module 3 | **Passed** |
| **Quantum Gates** | X, H, Z, CNOT, Measurement | Implemented with matrix, statevector, and Aer simulation | **Passed** |
| **Comparison Table** | 7-row Classical $\leftrightarrow$ Quantum Table | Expanded 10-row styled comparison matrix in Module D | **Passed** |
| **4-Level Progression** | Levels 1, 2, 3, 4 defined in doc | Interactive step-by-step learning cards with navigation | **Passed** |
| **Noise & Decoherence** | $V_{out} = V_{ideal} + n(t)$ vs Q-noise | Additive Gaussian sim + Q-noise channels + 3-qubit QEC | **Passed** |

---

## 6. Pedagogical Conclusion

The **TransistorToQubit** platform successfully bridges the pedagogical divide between classical semiconductor electronics and quantum information science. By anchoring every quantum abstraction to a familiar semiconductor mechanism (the BJT switch $\to$ qubit; the NOT inverter $\to$ Pauli-X gate; noise margins $\to$ quantum error correction), students construct an intuitive, resilient mental model of quantum computing.

---

## 7. References

1. **Yanofsky, N. S., & Mannucci, M. A. (2008). *Quantum Computing for Computer Scientists*. Cambridge University Press.**  
   *(Foundational reference for linear-algebraic, computer-science-oriented quantum mechanics, unitary gates, and quantum algorithm modeling without requiring prior quantum physics).*
2. **Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information* (10th Anniversary Edition). Cambridge University Press.**  
   *(Comprehensive standard reference for quantum circuits, Bloch sphere geometry, and quantum error correction).*
3. **Sedra, A. S., Smith, K. C., Carusone, T. C., & Gaudet, V. C. (2015). *Microelectronic Circuits* (7th ed.). Oxford University Press.**  
   *(Standard engineering textbook for BJT switching models, common-emitter inverters, cutoff/saturation regimes, and noise margins).*
4. **Preskill, J. (2018). *Quantum Computing in the NISQ era and beyond*. Quantum, 2, 79.**  
   *(Reference for quantum decoherence, environmental noise channels, and fault-tolerant architectures).*
5. **Qiskit Development Team. (2024). *Qiskit: An Open-Source Framework for Quantum Computing*. Zenodo.**  
   *(Upstream software framework powering the statevector evaluations and Aer circuit simulations in Module 3).*
