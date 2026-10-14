#set page(
  paper: "a4",
  margin: (top: 2.2cm, bottom: 2.2cm, left: 2.2cm, right: 2.2cm),
  header: align(right)[
    #text(size: 8.5pt, fill: rgb("#64748b"))[
      *TransistorToQubit* | EDC Assignment #2: Research Problem & Practical Implementation
    ]
  ],
  footer: context align(center)[
    #text(size: 8.5pt, fill: rgb("#94a3b8"))[
      Page #counter(page).display("1") of #counter(page).final().first()
    ]
  ]
)

#set text(
  font: "DejaVu Sans",
  size: 9.8pt,
  fill: rgb("#0f172a"),
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.65em,
)

#show heading.where(level: 1): it => block(
  above: 1.4em, below: 0.6em,
  text(weight: "bold", size: 14.5pt, fill: rgb("#0284c7"))[#it.body]
)

#show heading.where(level: 2): it => block(
  above: 1.1em, below: 0.45em,
  text(weight: "bold", size: 11.8pt, fill: rgb("#0f766e"))[#it.body]
)

#show heading.where(level: 3): it => block(
  above: 0.9em, below: 0.35em,
  text(weight: "bold", size: 10.2pt, fill: rgb("#334155"))[#it.body]
)

// Document Header
#align(center)[
  #block(width: 100%, stroke: (bottom: 2pt + rgb("#0284c7")), inset: (bottom: 14pt))[
    #text(size: 20pt, weight: "bold", fill: rgb("#0f172a"))[
      From Transistors to Qubits
    ] \
    #v(4pt)
    #text(size: 13pt, weight: "medium", fill: rgb("#0284c7"))[
      A Hybrid Learning Framework for Understanding Quantum Computing through Semiconductor Concepts
    ] \
    #v(8pt)
    #text(size: 9.5pt, fill: rgb("#475569"))[
      *Course Context:* EDC Assignment #2 | *Date:* October 2026 \
      *Tech Stack:* Python 3, Streamlit, Qiskit 1.x, Qiskit Aer, NumPy, Matplotlib, SVG
    ]
  ]
]

#v(8pt)

// Abstract Callout Box
#rect(
  width: 100%,
  fill: rgb("#f0f9ff"),
  stroke: 1pt + rgb("#bae6fd"),
  radius: 6pt,
  inset: 12pt,
)[
  #text(weight: "bold", size: 10.5pt, fill: rgb("#0369a1"))[Executive Summary & Abstract] \
  #v(3pt)
  #text(size: 9.2pt, fill: rgb("#1e293b"))[
    Students possessing foundational knowledge of semiconductor devices and classical digital circuits often experience a substantial conceptual gap when transitioning to quantum computing. Classical computing education grounds information in deterministic voltage rails ($0" V"$ vs $5" V"$), macroscopic transistor switches, and non-destructive measurement. Conversely, quantum mechanics introduces non-orthogonal vector superpositions, complex probability amplitudes, unitary transformations, irreversible projective collapse, and quantum entanglement.

    This report presents the design, mathematical modeling, and evaluation of *TransistorToQubit* — an interactive software and pedagogical framework. The platform provides a direct, level-by-level bridge from bipolar junction transistor (NPN BJT) switching and canonical logic gates (NOT, AND, OR, NAND, NOR, XOR) to quantum states ($|0⟩$, $|1⟩$, $|+⟩$), quantum logic gates ($X$, $H$, $Z$, $"CNOT"$), 3D Bloch sphere geometry, and Aer measurement simulations. Furthermore, a deep comparative analysis of classical additive noise versus quantum decoherence and the 3-qubit bit-flip Quantum Error Correction (QEC) code is formulated and evaluated.
  ]
]

#v(8pt)

= 1. Pedagogical Problem & 4-Level Progression Framework

== 1.1 The Classical-to-Quantum Learning Chasm
Engineering curricula traditionally educate students in a bottom-up physical hierarchy:
$ "Semiconductor Materials" --> "BJT / MOSFET Switches" --> "Logic Gates" --> "Digital Systems" $
In this paradigm, information is represented as a macroscopic physical voltage $V(t)$. Measuring this voltage with a high-impedance oscilloscope probe does not perturb the circuit state. 

When entering quantum computing, students encounter axioms that run directly counter to their electronic intuition:
1. *Continuous State Space:* A classical bit is strictly $b in {0, 1}$. A qubit state $|psi⟩ = alpha |0⟩ + beta |1⟩$ lives on the continuous surface of a complex unit sphere (the Bloch sphere), where $alpha, beta in CC$ and $|alpha|^2 + |beta|^2 = 1$.
2. *Linear Unitary Gates:* Quantum gates must be reversible and unitary ($U^dagger U = I$), contrasting with classical gates (e.g., AND, OR) that destroy information.
3. *Observer Effect:* Measuring a qubit is not a benign voltage observation; it is a projective measurement that irrevocably collapses $|psi⟩$ into a computational basis state according to the Born rule ($P(i) = |⟨i|psi⟩|^2$).

== 1.2 The Four-Level Progression Framework
To eliminate this cognitive barrier, the framework organizes learning into four structured stages:

- *Level 1 — Transistor Switch:* The student investigates how base current $I_B$ drives an NPN BJT between *Cutoff* ($V_(i n) <= V_(t h) ==> V_(o u t) approx 5" V"$, Logic 1) and *Saturation* ($V_(i n) > V_(t h) ==> V_(o u t) approx 0.2" V"$, Logic 0). This grounds binary logic in solid-state semiconductor physics.
- *Level 2 — Logic Gate (NOT $arrow.l.r$ Pauli-X):* The classical BJT inverter circuit ($0 -> 1, 1 -> 0$) is linked to the Pauli-X gate ($X|0⟩ = |1⟩$, $X|1⟩ = |0⟩$). The platform provides an in-app navigation button taking the student directly from the classical NOT truth table to the quantum X gate in Module 3.
- *Level 3 — Bit to Qubit (Superposition):* The discrete scalar $b in {0, 1}$ transitions to probability amplitudes $alpha, beta$. The student experiments with the Hadamard gate:
  $ H |0⟩ = 1 / sqrt(2) (|0⟩ + |1⟩) ==> P(0) = 50%, quad P(1) = 50% $
- *Level 4 — Classical Circuit vs Quantum Circuit:* The student contrasts deterministic classical gate pipelines against quantum circuits that manipulate interference and entanglement prior to irreversible projective readout.

#v(8pt)

= 2. Classical Electronics to Quantum Computing Concept Map

The platform implements the following comprehensive 10-point concept dictionary:

#table(
  columns: (1.1fr, 1.4fr, 1.5fr, 1.8fr),
  stroke: (x, y) => if y == 0 { (bottom: 1.5pt + rgb("#0284c7")) } else { 0.5pt + rgb("#e2e8f0") },
  fill: (x, y) => if y == 0 { rgb("#f1f5f9") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  inset: (x, y) => if y == 0 { (top: 7pt, bottom: 7pt, left: 6pt, right: 6pt) } else { (top: 5pt, bottom: 5pt, left: 6pt, right: 6pt) },
  [#text(weight: "bold", size: 8.5pt)[Classical Concept]],
  [#text(weight: "bold", size: 8.5pt)[What Student Knows]],
  [#text(weight: "bold", size: 8.5pt)[Quantum Counterpart]],
  [#text(weight: "bold", size: 8.5pt)[Key Conceptual Distinction]],
  
  [Transistor], [Electronic switching device], [Qubit (2-level quantum system)], [Switch is macroscopic; qubit is a 2-dimensional complex vector space.],
  [ON / OFF], [Binary rails ($0" V"$ / $5" V"$)], [Measurement collapse ($0$ or $1$)], [Classical state is always definite; qubit is continuous until measured.],
  [Voltage/Current], [Physical observable signal], [Quantum statevector $|psi⟩$ / amplitudes], [Amplitudes $alpha, beta in CC$ possess phase; voltage is purely real scalar.],
  [Logic Gate], [Deterministic Boolean gate], [Unitary gate ($X, H, Z, "CNOT"$)], [Quantum gates must be reversible unitary matrices ($U^dagger U = I$).],
  [NOT Gate], [Inverts signal ($0 <-> 1$)], [Pauli-X gate (Quantum NOT)], [$X|0⟩ = |1⟩$, $X|1⟩ = |0⟩$, but acts linearly on superpositions.],
  [Digital Circuit], [Interconnected Boolean gates], [Quantum Circuit], [Exploits superposition and interference across Hilbert space.],
  [Classical Bit], [Scalar $b in {0, 1}$], [Qubit $|psi⟩ = alpha |0⟩ + beta |1⟩$], [Continuous continuum of states on the Bloch sphere surface.],
  [Measurement], [Non-destructive voltmeter probe], [Projective measurement collapse], [Irreversible wave-function collapse governed by Born rule ($P = |alpha|^2$).],
  [Noise], [Additive voltage $V + n(t)$], [Decoherence / Quantum noise], [Quantum noise rotates state vectors and destroys phase coherence.],
  [Determinism], [Same input yields same output], [Probabilistic measurement], [Unitary evolution is deterministic; measurement sampling is stochastic.],
)

#v(8pt)

= 3. System Architecture & Technical Implementation

== 3.1 Module 1: Transistor as an Electronic Switch
Module 1 models an NPN BJT Common-Emitter inverter with a resistive collector pull-up:
- *Base Input Voltage ($V_(i n)$):* Synchronized slider and numeric input from $0.0" V"$ to $6.0" V"$.
- *Switching Threshold ($V_(t h) / V_(B E(o n))$):* Nominal $0.7" V"$ for standard silicon PN junctions.
- *Collector Load Resistance ($R_L$):* Variable resistance from $100 Omega$ to $10{,}000 Omega$.
- *Current Rating ($I_(C,m a x)$):* Maximum collector current limit ($1.0" mA"$ to $50.0" mA"$).
- *Supply Rail ($V_(C C)$):* Hardcoded to $5.0" V"$, representing the universal TTL standard rail.

#block(fill: rgb("#f8fafc"), stroke: 0.5pt + rgb("#cbd5e1"), radius: 4pt, inset: 8pt)[
  *Mathematical Physics Model:*
  The base current $I_B$ is governed by:
  $ I_B = cases(
    0 & "if" V_(i n) <= V_(t h),
    (V_(i n) - V_(t h)) / R_B & "if" V_(i n) > V_(t h)
  ) $
  where $R_B = 10" k"Omega$. In the active region, $I_(C,"active") = beta I_B$ ($\beta = 100$). The maximum current allowed by the DC load line is:
  $ I_(C,"sat") = (V_(C C) - V_(C E,"sat")) / R_L quad (V_(C E,"sat") = 0.2" V") $
  The actual collector current is $I_C = min(I_(C,"active"), I_(C,"sat"), I_(C,m a x))$.
  - *Cutoff ($V_(i n) <= V_(t h)$):* $I_C = 0" mA"$, $V_(o u t) = V_(C C) = 5.0" V" ==> bold("Logic 1")$ (Open switch).
  - *Saturation ($I_(C,"active") >= I_(C,"sat")$):* $I_C = I_(C,"sat")$, $V_(o u t) = V_(C E,"sat") approx 0.2" V" ==> bold("Logic 0")$ (Closed switch).
]

Live visual feedback is rendered through an in-memory dynamic SVG schematic illustrating wire conduction, base activation, collector current flow, and digital output state.

== 3.2 Module 2: Classical Logic Gates
Module 2 provides interactive exploration of the six canonical gates required by the assignment document:
- *Gates Implemented:* NOT, AND, OR, NAND, NOR, and XOR.
- *Dual Visualizations:* Students toggle between standard IEEE 91-1984 logic symbols and Resistor-Transistor Logic (RTL) transistor-level circuit schematics.
- *Dynamic Truth Tables:* Rendered inside an isolated HTML frame with real-time row highlighting based on user switch inputs ($A, B in {0, 1}$).
- *NOT $arrow.r$ X Navigation:* Selecting the NOT gate exposes an interactive card and one-click button:
  $ "NOT "(0) = 1 <==> X|0⟩ = |1⟩ $
  Clicking the button seamlessly routes the session to the Pauli-X gate in Module 3.

== 3.3 Module 3: Quantum Gates & Circuits (Qiskit Engine)
Module 3 is built upon Qiskit 1.x and Qiskit Aer:
- *Initial Computational States:* Selectable ground state $|0⟩ = mat(1; 0)$ and excited state $|1⟩ = mat(0; 1)$.
- *Quantum Operators:*
  $ X = mat(0, 1; 1, 0), quad H = 1/sqrt(2) mat(1, 1; 1, -1), quad Z = mat(1, 0; 0, -1) $
- *Two-Qubit Entanglement (CNOT):* Applies Controlled-NOT:
  $ "CNOT" (H |0⟩ ⊗ |0⟩) = 1 / sqrt(2) (|00⟩ + |11⟩) = |Phi^+⟩ $
- *Annotated 3D Bloch Sphere:* Features cardinal coordinate axes and labeled Dirac points ($|0⟩$ North Pole, $|1⟩$ South Pole, $|+⟩, |-⟩, |i⟩$ along the equatorial plane).
- *Measurement Collapse Simulation:* Executes projective measurements on `AerSimulator` across $128$ to $4096$ shots, producing empirical probability histograms matching theoretical Born rule calculations ($P(m) = |⟨m|psi⟩|^2$).

== 3.4 Module D: Comparison & Noise Framework
Module D unifies the learning experience by providing:
1. The 10-row Classical $arrow.l.r$ Quantum Concept Mapping table.
2. The 4-Level Learning Progression with contextual navigation buttons.
3. The Classical vs Quantum Noise comparison suite.

#v(8pt)

= 4. Deep-Dive: Classical Noise vs Quantum Decoherence

== 4.1 Classical Noise & Voltage Noise Margins
In classical digital electronics, noise is additive voltage fluctuations:
$ V_(o u t)(t) = V_("ideal") + n(t), quad n(t) tilde.op cal(N)(0, sigma^2) $
Digital circuits achieve immense reliability through *noise margins*:
$ N M_H = V_(O H,m i n) - V_(I H,m i n), quad N M_L = V_(I L,m a x) - V_(O L,m a x) $
Because the BJT inverter has a steep, non-linear voltage transfer characteristic, any small fluctuation ($sigma < 1.0" V"$) is attenuated at subsequent stages. Information is refreshed automatically.

== 4.2 Quantum Decoherence & Error Channels
In quantum systems, noise is non-additive and phase-sensitive:
1. *Bit-Flip Error Channel ($X$):* $|psi⟩ arrow.r.long^(p) X|psi⟩$, randomly flipping $|0⟩ <-> |1⟩$.
2. *Phase-Flip Error Channel ($Z$):* $|psi⟩ arrow.r.long^(p) Z|psi⟩$, altering phase without affecting populations ($|+⟩ <-> |-⟩$).
3. *Depolarizing Noise Channel ($cal(E)$):* Replaces the density matrix with the maximally mixed state with probability $p$:
   $ cal(E)(rho) = (1 - p) rho + p/3 (X rho X + Y rho Y + Z rho Z) $

== 4.3 Quantum Error Correction (3-Qubit Bit-Flip Code)
Classical error correction uses simple duplication ($0 -> 000, 1 -> 111$). In quantum computing, the *No-Cloning Theorem* ($U|psi⟩ |0⟩ eq.not |psi⟩ |psi⟩$) forbids copying an unknown state. Furthermore, directly measuring qubits to detect errors collapses their superposition.

The 3-qubit bit-flip code resolves this via entanglement:
1. *Encoding:* Using two CNOT gates, the logical qubit is encoded into an entangled 3-qubit state:
   $ |psi⟩ = alpha |0⟩ + beta |1⟩ ==> |psi_("enc")⟩ = alpha |000⟩ + beta |111⟩ $
2. *Syndrome Measurement:* Parity operators $Z_0 Z_1$ and $Z_1 Z_2$ are measured using ancilla qubits, yielding syndrome bits $s_1 s_2 in {00, 10, 11, 01}$ without revealing $alpha$ or $beta$:
   - $s_1 s_2 = 00 ==> "No error"$
   - $s_1 s_2 = 10 ==> "Bit-flip on " q_0 quad (arrow.r "apply " X_0)$
   - $s_1 s_2 = 11 ==> "Bit-flip on " q_1 quad (arrow.r "apply " X_1)$
   - $s_1 s_2 = 01 ==> "Bit-flip on " q_2 quad (arrow.r "apply " X_2)$
3. *Recovery:* Applying the diagnosed Pauli-X operator restores the original state $|psi⟩$ with $100%$ theoretical fidelity.

#v(8pt)

= 5. Experimental Verification & Results Matrix

#table(
  columns: (1.8fr, 2fr, 1fr),
  stroke: 0.5pt + rgb("#cbd5e1"),
  fill: (x, y) => if y == 0 { rgb("#e0f2fe") } else if calc.even(y) { rgb("#f8fafc") } else { none },
  inset: 6pt,
  [#text(weight: "bold", size: 8.5pt)[Specification / Criterion]],
  [#text(weight: "bold", size: 8.5pt)[Implementation Output]],
  [#text(weight: "bold", size: 8.5pt)[Verification]],

  [Vary Base Input Voltage], [$V_(i n)$ slider + manual numeric input ($0.0" V"$ to $6.0" V"$)], [Passed],
  [Vary Switching Threshold], [$V_(t h)$ slider + numeric input ($0.1" V"$ to $4.0" V"$)], [Passed],
  [Vary Load Resistance], [$R_L$ slider + numeric input ($100 Omega$ to $10" k"Omega$)], [Passed],
  [Vary Collector Current Limit], [$I_(C,m a x)$ slider + numeric input ($1.0" mA"$ to $50.0" mA"$)], [Passed],
  [Observe Transistor Switching], [Dynamic SVG schematic showing Cutoff vs Saturation paths], [Passed],
  [Canonical Logic Gates], [NOT, AND, OR, NAND, NOR, XOR with IEEE symbols & RTL circuits], [Passed],
  [Live Truth Tables], [HTML frame with active-row blue highlight for current inputs], [Passed],
  [Quantum Basis States], [$|0⟩$, $|1⟩$ selectable in Module 3], [Passed],
  [Quantum Gates & Circuits], [$X, H, Z, "CNOT"$, and Measurement with Qiskit 1.x & Aer], [Passed],
  [Bloch Sphere Representation], [3D Bloch sphere with labeled poles ($|0⟩, |1⟩, |+⟩, |-⟩, |i⟩$)], [Passed],
  [Classical $arrow.l.r$ Quantum Comparison], [Dedicated Module D with 10-row mapping table], [Passed],
  [4-Level Progression], [Explicit 4-level sequence with NOT $arrow.r$ X navigation bridge], [Passed],
  [Noise Modeling & QEC], [Classical $n(t)$ sim, bit/phase-flip channels, 3-qubit QEC pipeline], [Passed],
)

#v(8pt)

= 6. Conclusion
The *TransistorToQubit* framework provides a pedagogically sound, mathematically rigorous bridge connecting classical electronic engineering with modern quantum computation. By structuring the learning journey around four progressive levels, anchoring abstract quantum gates in physical transistor switching, and illustrating the fundamental difference between classical noise margins and quantum error correction, the platform substantially accelerates student comprehension of quantum information science.

#v(8pt)

= 7. References

+ *Yanofsky, N. S., & Mannucci, M. A. (2008).* _Quantum Computing for Computer Scientists_. Cambridge University Press.  
  #text(size: 8.5pt, fill: rgb("#475569"))[
    (Fundamental textbook establishing quantum computing via linear algebra, tensor products, unitary transformations, and complex vector spaces tailored for computer scientists and engineers without requiring prior advanced quantum mechanics).
  ]
+ *Nielsen, M. A., & Chuang, I. L. (2010).* _Quantum Computation and Quantum Information_ (10th Anniversary Edition). Cambridge University Press.
+ *Sedra, A. S., Smith, K. C., Carusone, T. C., & Gaudet, V. C. (2015).* _Microelectronic Circuits_ (7th ed.). Oxford University Press.
+ *Preskill, J. (2018).* Quantum Computing in the NISQ era and beyond. _Quantum_, 2, 79.
+ *Qiskit Development Team. (2024).* _Qiskit: An Open-Source Framework for Quantum Computing_. Zenodo. https://doi.org/10.5281/zenodo.2573505
