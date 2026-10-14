"""
Comprehensive test script for TransistorToQubit application.
Validates:
1. Module imports
2. Transistor physics calculations
3. Classical logic gates and SVGs
4. Qiskit circuits, statevector calculations, Bloch sphere plotting, and Aer simulation
"""

import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.svg_generator import (
    generate_transistor_circuit_svg,
    generate_logic_gate_symbol_svg,
    generate_transistor_logic_circuit_svg,
)
from modules.logic_gates import compute_gate_output
from utils.quantum_helpers import (
    build_single_qubit_circuit,
    build_two_qubit_cnot_circuit,
    format_statevector_latex,
    draw_circuit_mpl,
    draw_bloch_sphere,
    run_aer_simulation,
)
from qiskit.quantum_info import Statevector


def test_transistor_svg():
    print("Testing Transistor Circuit SVG...")
    svg = generate_transistor_circuit_svg(3.3, 0.2, 4.8, 260.0, 1000.0, 5.0, 0.7, "SATURATION")
    assert "<svg" in svg and "</svg>" in svg
    assert "SATURATION" in svg
    print("✅ Transistor SVG test passed.")


def test_logic_gates():
    print("Testing Classical Logic Gates truth values & SVGs...")
    expected_outputs = {
        "NOT": {(0,): 1, (1,): 0},
        "AND": {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1},
        "OR": {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 1},
        "NAND": {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0},
        "NOR": {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 0},
        "XOR": {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0},
    }

    for gate, table in expected_outputs.items():
        for inputs, expected_q in table.items():
            if len(inputs) == 1:
                q = compute_gate_output(gate, inputs[0])
            else:
                q = compute_gate_output(gate, inputs[0], inputs[1])
            assert q == expected_q, f"Gate {gate} failed for inputs {inputs}: got {q}, expected {expected_q}"

        # Test SVGs across all input combinations
        for inputs, expected_q in table.items():
            in_a = inputs[0]
            in_b = inputs[1] if len(inputs) > 1 else 0
            sym_svg = generate_logic_gate_symbol_svg(gate, in_a, in_b, expected_q)
            assert "<svg" in sym_svg and "</svg>" in sym_svg, f"Symbol SVG invalid for {gate} {inputs}"
            ckt_svg = generate_transistor_logic_circuit_svg(gate, in_a, in_b, expected_q)
            assert "<svg" in ckt_svg and "</svg>" in ckt_svg, f"Circuit SVG invalid for {gate} {inputs}"
            assert "T1" in ckt_svg, f"T1 transistor missing in {gate} circuit SVG"
            if gate in ["AND", "OR", "NAND", "NOR", "XOR"]:
                assert "T2" in ckt_svg, f"T2 transistor missing in {gate} circuit SVG"

    print("✅ Classical Logic Gates test passed.")


def test_quantum_circuits():
    print("Testing Quantum Circuits, Statevectors, and Aer Simulator...")
    
    # 1. Single Qubit Gates: X, H, Z, M
    for gate in ["X", "H", "Z", "M"]:
        for init_state in ["|0⟩", "|1⟩"]:
            qc_state, qc_meas = build_single_qubit_circuit(init_state, gate, with_measurement=True)
            sv = Statevector.from_instruction(qc_state)
            latex = format_statevector_latex(sv, num_qubits=1)
            assert len(latex) > 0
            fig_circ = draw_circuit_mpl(qc_meas)
            assert fig_circ is not None
            fig_bloch = draw_bloch_sphere(sv)
            assert fig_bloch is not None
            counts, fig_hist = run_aer_simulation(qc_meas, shots=256)
            assert len(counts) > 0
            import matplotlib.pyplot as plt
            plt.close("all")
            
    # Verify specific physics: X|0> -> |1>
    qc_x, _ = build_single_qubit_circuit("|0⟩", "X", False)
    sv_x = Statevector.from_instruction(qc_x)
    assert abs(sv_x.data[1]) > 0.99, "X gate failed to flip |0> to |1>"

    # Verify specific physics: H|0> -> 1/sqrt(2) (|0> + |1>)
    qc_h, _ = build_single_qubit_circuit("|0⟩", "H", False)
    sv_h = Statevector.from_instruction(qc_h)
    assert abs(abs(sv_h.data[0])**2 - 0.5) < 0.01, "H gate failed to create equal superposition"

    # 2. Two Qubit CNOT & Bell State
    qc_bell, qc_bell_meas = build_two_qubit_cnot_circuit("|0⟩", "|0⟩", superpose_ctrl=True, with_measurement=True)
    sv_bell = Statevector.from_instruction(qc_bell)
    # Bell state has amplitudes at |00> and |11> only
    p00 = abs(sv_bell.data[0])**2
    p11 = abs(sv_bell.data[3])**2
    assert abs(p00 - 0.5) < 0.01 and abs(p11 - 0.5) < 0.01, "Bell state generation failed"
    
    counts_bell, _ = run_aer_simulation(qc_bell_meas, shots=500)
    # Should only observe 00 and 11
    assert "00" in counts_bell and "11" in counts_bell
    assert "01" not in counts_bell and "10" not in counts_bell

    print("✅ Quantum Circuits, Gates, and Bell State tests passed.")


if __name__ == "__main__":
    test_transistor_svg()
    test_logic_gates()
    test_quantum_circuits()
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")
