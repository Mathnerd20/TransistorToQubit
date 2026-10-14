"""
Configuration and constants for the TransistorToQubit Streamlit application.
"""

APP_TITLE = "Transistor to Qubit: The Evolution of Computing"
APP_ICON = "⚡"
APP_SUBTITLE = "From Semiconductor Physics to Classical Logic and Quantum Superposition"

# Color Palette (Dark Theme / Cyber-Physical)
THEME_COLORS = {
    "bg_dark": "#0B0F19",
    "bg_card": "rgba(22, 27, 34, 0.75)",
    "border": "rgba(56, 139, 253, 0.25)",
    "accent_cyan": "#00f0ff",
    "accent_blue": "#388bfd",
    "accent_purple": "#a855f7",
    "accent_green": "#22c55e",
    "accent_amber": "#f59e0b",
    "accent_rose": "#f43f5e",
    "text_primary": "#f0f6fc",
    "text_secondary": "#8b949e",
    "high_state": "#22c55e",
    "low_state": "#64748b",
}

# Module Definitions
MODULES = {
    "module1": {
        "title": "Module 1: Transistor Switching",
        "icon": "🔌",
        "description": "Physical Layer: Observe semiconductor switching, cutoff, active & saturation regions with live circuit schematics.",
    },
    "module2": {
        "title": "Module 2: Classical Logic Gates",
        "icon": "🔲",
        "description": "Gate Layer: Interactive NOT, AND, OR, NAND, NOR, and XOR with logic symbols and transistor-level RTL/CMOS circuits.",
    },
    "module3": {
        "title": "Module 3: Quantum Gates & Circuits",
        "icon": "⚛️",
        "description": "Quantum Layer: Qubits |0⟩, |1⟩, Pauli-X, Hadamard, Pauli-Z, CNOT, and Measurement using Qiskit.",
    },
    "module4": {
        "title": "Module D: Classical ↔ Quantum Comparison",
        "icon": "🗺️",
        "description": "Comparison Framework: Concept mapping table, 4-level learning progression, and classical vs quantum noise analysis.",
    },
}
