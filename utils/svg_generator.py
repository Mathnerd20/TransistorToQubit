"""
SVG Circuit Generator for Transistor and Classical Logic Gate visualizations.
Produces crisp, modern vector graphics with dynamic wire states, glowing paths, and labels.
"""

import streamlit.components.v1 as components


def clean_svg(svg_str: str) -> str:
    """Strips leading and trailing whitespace from every line so Markdown or HTML never treats SVG as code."""
    lines = [line.strip() for line in svg_str.splitlines() if line.strip()]
    return "\n".join(lines)


def render_svg(svg_str: str, height: int = 480):
    """
    Renders an SVG diagram in an isolated canvas using components.html with:
    - High-performance vector scaling to fill available space
    - Interactive Zoom & Pan (mouse wheel zoom, drag to pan, double-click to reset)
    - Floating control toolbar with Zoom In (+), Zoom Out (−), Reset (↺), and Fit (⛶)
    - Live zoom percentage indicator
    """
    cleaned_svg = clean_svg(svg_str)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      user-select: none;
    }}
    html, body {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: transparent;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    .circuit-container {{
      width: 100%;
      height: 100%;
      background: #030712;
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 12px;
      position: relative;
      overflow: hidden;
      box-shadow: inset 0 2px 12px rgba(0, 0, 0, 0.7), 0 0 20px rgba(56, 189, 248, 0.1);
    }}
    .zoom-toolbar {{
      position: absolute;
      top: 8px;
      right: 10px;
      z-index: 30;
      display: flex;
      align-items: center;
      gap: 4px;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 20px;
      padding: 4px 8px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6);
    }}
    .zoom-btn {{
      background: transparent;
      border: none;
      color: #94a3b8;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 16px;
      font-weight: bold;
      transition: all 0.15s ease;
      touch-action: manipulation;
    }}
    .zoom-btn:hover {{
      background: rgba(56, 189, 248, 0.25);
      color: #38bdf8;
      transform: scale(1.1);
    }}
    .zoom-btn:active {{
      transform: scale(0.95);
    }}
    .zoom-val {{
      color: #38bdf8;
      font-size: 12px;
      font-weight: 700;
      font-family: monospace;
      min-width: 42px;
      text-align: center;
      padding: 0 2px;
    }}
    .viewport {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      cursor: grab;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      touch-action: none;
    }}
    .viewport.grabbing {{
      cursor: grabbing;
    }}
    .svg-wrapper {{
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      transform-origin: center center;
      will-change: transform;
    }}
    .svg-wrapper svg {{
      width: 100%;
      height: 100%;
      max-width: 100%;
      max-height: 100%;
      display: block;
    }}
    .hint-bar {{
      position: absolute;
      bottom: 8px;
      left: 12px;
      z-index: 20;
      pointer-events: none;
      font-size: 10px;
      color: #64748b;
      font-family: monospace;
      background: rgba(3, 7, 18, 0.7);
      padding: 2px 8px;
      border-radius: 6px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }}
  </style>
</head>
<body>
  <div class="circuit-container" id="circuitBox">
    <div class="zoom-toolbar">
      <button class="zoom-btn" id="btnZoomIn" title="Zoom In (+)">+</button>
      <span class="zoom-val" id="zoomVal">100%</span>
      <button class="zoom-btn" id="btnZoomOut" title="Zoom Out (−)">−</button>
      <button class="zoom-btn" id="btnReset" title="Reset (↺)">↺</button>
      <button class="zoom-btn" id="btnFit" title="Fit to Box (⛶)">⛶</button>
    </div>
    
    <div class="viewport" id="viewport">
      <div class="svg-wrapper" id="svgWrapper">
        {cleaned_svg}
      </div>
    </div>
    
    <div class="hint-bar">🔍 Scroll/pinch to zoom · Drag to pan · Double-tap to reset</div>
  </div>

  <script>
    (function() {{
      let scale = 1.0;
      let panX = 0;
      let panY = 0;
      let isPanning = false;
      let startX = 0;
      let startY = 0;
      let initialPinchDist = null;
      let lastTapTime = 0;

      const wrapper = document.getElementById('svgWrapper');
      const viewport = document.getElementById('viewport');
      const zoomVal = document.getElementById('zoomVal');

      function applyTransform() {{
        wrapper.style.transform = `translate(${{panX}}px, ${{panY}}px) scale(${{scale}})`;
        zoomVal.textContent = Math.round(scale * 100) + '%';
      }}

      function zoom(factor, clientX, clientY) {{
        const oldScale = scale;
        let newScale = Math.min(Math.max(scale * factor, 0.5), 4.5);
        if (newScale === oldScale) return;

        if (clientX !== undefined && clientY !== undefined) {{
          const rect = viewport.getBoundingClientRect();
          const offsetX = clientX - rect.left - rect.width / 2;
          const offsetY = clientY - rect.top - rect.height / 2;
          panX = offsetX - (offsetX - panX) * (newScale / oldScale);
          panY = offsetY - (offsetY - panY) * (newScale / oldScale);
        }}
        scale = newScale;
        applyTransform();
      }}

      function reset() {{
        scale = 1.0;
        panX = 0;
        panY = 0;
        applyTransform();
      }}

      // Mouse wheel zoom
      viewport.addEventListener('wheel', function(e) {{
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.15 : 0.87;
        zoom(factor, e.clientX, e.clientY);
      }}, {{ passive: false }});

      // Mouse drag pan
      viewport.addEventListener('mousedown', function(e) {{
        if (e.button !== 0) return;
        isPanning = true;
        startX = e.clientX - panX;
        startY = e.clientY - panY;
        viewport.classList.add('grabbing');
      }});

      window.addEventListener('mousemove', function(e) {{
        if (!isPanning) return;
        panX = e.clientX - startX;
        panY = e.clientY - startY;
        applyTransform();
      }});

      window.addEventListener('mouseup', function() {{
        if (isPanning) {{
          isPanning = false;
          viewport.classList.remove('grabbing');
        }}
      }});

      viewport.addEventListener('dblclick', function() {{
        reset();
      }});

      // Touch events for Mobile & Tablets
      viewport.addEventListener('touchstart', function(e) {{
        if (e.touches.length === 1) {{
          isPanning = true;
          startX = e.touches[0].clientX - panX;
          startY = e.touches[0].clientY - panY;
          viewport.classList.add('grabbing');
        }} else if (e.touches.length === 2) {{
          isPanning = false;
          const t1 = e.touches[0];
          const t2 = e.touches[1];
          initialPinchDist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
        }}
      }}, {{ passive: false }});

      window.addEventListener('touchmove', function(e) {{
        if (e.touches.length === 1 && isPanning) {{
          e.preventDefault();
          panX = e.touches[0].clientX - startX;
          panY = e.touches[0].clientY - startY;
          applyTransform();
        }} else if (e.touches.length === 2 && initialPinchDist) {{
          e.preventDefault();
          const t1 = e.touches[0];
          const t2 = e.touches[1];
          const dist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
          if (dist > 10) {{
            const factor = dist / initialPinchDist;
            const midX = (t1.clientX + t2.clientX) / 2;
            const midY = (t1.clientY + t2.clientY) / 2;
            zoom(factor, midX, midY);
            initialPinchDist = dist;
          }}
        }}
      }}, {{ passive: false }});

      window.addEventListener('touchend', function(e) {{
        if (e.touches.length < 2) {{
          initialPinchDist = null;
        }}
        if (e.touches.length === 0) {{
          isPanning = false;
          viewport.classList.remove('grabbing');

          const now = Date.now();
          if (now - lastTapTime < 300) {{
            reset();
          }}
          lastTapTime = now;
        }}
      }});

      document.getElementById('btnZoomIn').addEventListener('click', function(e) {{
        e.stopPropagation();
        zoom(1.25);
      }});

      document.getElementById('btnZoomOut').addEventListener('click', function(e) {{
        e.stopPropagation();
        zoom(0.8);
      }});

      document.getElementById('btnReset').addEventListener('click', function(e) {{
        e.stopPropagation();
        reset();
      }});

      document.getElementById('btnFit').addEventListener('click', function(e) {{
        e.stopPropagation();
        reset();
      }});
    }})();
  </script>
</body>
</html>"""
    components.html(html_content, height=height)


def generate_transistor_circuit_svg(v_in, v_out, i_c_ma, i_b_ua, r_l, v_cc, v_th, state):
    """
    Generates an SVG schematic for an NPN transistor switch circuit.
    Displays:
    - V_CC rail and load resistor R_L
    - Output probe point V_out
    - Transistor NPN symbol with active conduction channel
    - Base resistor R_B and input source V_in
    - Dynamic current flow glow and state-dependent LED indicator
    """
    is_on = state == "SATURATION"
    is_active = state == "ACTIVE"
    
    # Wire colors based on electrical state
    wire_vcc_col = "#38bdf8"
    wire_in_col = "#22c55e" if v_in >= v_th else "#64748b"
    wire_out_col = "#22c55e" if v_out > 2.5 else "#64748b"
    transistor_glow = "#22c55e" if is_on else ("#f59e0b" if is_active else "#475569")
    
    # Current flow opacity and dash animation
    ic_flow_opacity = "1.0" if (is_on or is_active) else "0.15"
    current_dash = 'stroke-dasharray="6,4"' if (is_on or is_active) else ""

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 480" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style="background:#090d16; border-radius:12px; font-family:'JetBrains Mono', monospace;">
      <defs>
        <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="4" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="glow-green" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="5" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <linearGradient id="grad-on" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#22c55e" stop-opacity="0.8"/>
          <stop offset="100%" stop-color="#15803d" stop-opacity="0.3"/>
        </linearGradient>
      </defs>

      <!-- Grid Background Pattern -->
      <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
      </pattern>
      <rect width="100%" height="100%" fill="url(#grid)" />

      <!-- Title / Status Bar inside SVG -->
      <text x="30" y="38" fill="#94a3b8" font-size="13" font-family="'Outfit', sans-serif">NPN BIPOLAR JUNCTION TRANSISTOR (COMMON EMITTER SWITCH)</text>
      <rect x="540" y="20" width="190" height="28" rx="14" fill="rgba(30,41,59,0.8)" stroke="{transistor_glow}" stroke-width="1.5"/>
      <circle cx="555" cy="34" r="5" fill="{transistor_glow}"/>
      <text x="568" y="38" fill="#f8fafc" font-size="12" font-weight="bold">{state}</text>

      <!-- V_CC Power Supply Rail Top -->
      <line x1="420" y1="70" x2="420" y2="110" stroke="{wire_vcc_col}" stroke-width="3"/>
      <circle cx="420" cy="70" r="5" fill="{wire_vcc_col}" filter="url(#glow-cyan)"/>
      <text x="432" y="75" fill="#38bdf8" font-size="14" font-weight="bold">V_CC = +{v_cc:.1f} V</text>

      <!-- Collector Load Resistor R_L -->
      <rect x="406" y="110" width="28" height="65" rx="3" fill="#1e293b" stroke="{wire_vcc_col}" stroke-width="2.5"/>
      <line x1="406" y1="125" x2="434" y2="125" stroke="#475569" stroke-width="1.5"/>
      <line x1="406" y1="140" x2="434" y2="140" stroke="#475569" stroke-width="1.5"/>
      <line x1="406" y1="155" x2="434" y2="155" stroke="#475569" stroke-width="1.5"/>
      <text x="445" y="146" fill="#cbd5e1" font-size="13" font-weight="bold">R_L = {r_l:,.0f} Ω</text>
      <text x="445" y="162" fill="#94a3b8" font-size="11">Load Resistor</text>

      <!-- Wire from R_L to Collector Node -->
      <line x1="420" y1="175" x2="420" y2="240" stroke="{wire_vcc_col}" stroke-width="3"/>

      <!-- Node Junction above Collector (V_out probe point) -->
      <circle cx="420" cy="210" r="5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
      <!-- Line to V_out Output Terminal -->
      <line x1="420" y1="210" x2="570" y2="210" stroke="{wire_out_col}" stroke-width="3" {current_dash}/>
      <circle cx="570" cy="210" r="6" fill="{wire_out_col}"/>
      <!-- Output Readout Box -->
      <rect x="585" y="185" width="145" height="50" rx="8" fill="#0f172a" stroke="{wire_out_col}" stroke-width="2"/>
      <text x="597" y="206" fill="#94a3b8" font-size="11">OUTPUT V_out</text>
      <text x="597" y="226" fill="{wire_out_col}" font-size="16" font-weight="bold">{v_out:.2f} V</text>
      <text x="680" y="226" fill="#94a3b8" font-size="13">({"HIGH (1)" if v_out > 2.0 else "LOW (0)"})</text>

      <!-- Collector Current Flow Indicator Arrow -->
      <g opacity="{ic_flow_opacity}">
        <line x1="395" y1="185" x2="395" y2="235" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)" stroke-dasharray="4,3"/>
        <text x="315" y="215" fill="#38bdf8" font-size="12">I_C = {i_c_ma:.2f} mA ↓</text>
      </g>

      <!-- Base Input Circuit (V_in Source & R_B) -->
      <!-- Input Source Terminal -->
      <circle cx="90" cy="275" r="6" fill="{wire_in_col}"/>
      <text x="50" y="255" fill="{wire_in_col}" font-size="13" font-weight="bold">V_in (Base)</text>
      <text x="50" y="275" fill="#f8fafc" font-size="15" font-weight="bold">{v_in:.2f} V</text>
      <text x="50" y="295" fill="#94a3b8" font-size="11">Thresh: {v_th:.2f}V</text>

      <!-- Wire to Base Resistor R_B -->
      <line x1="96" y1="275" x2="190" y2="275" stroke="{wire_in_col}" stroke-width="3"/>

      <!-- Base Resistor R_B -->
      <rect x="190" y="263" width="60" height="24" rx="3" fill="#1e293b" stroke="{wire_in_col}" stroke-width="2"/>
      <text x="195" y="250" fill="#cbd5e1" font-size="12">R_B = 10 kΩ</text>

      <!-- Wire from R_B to Transistor Base -->
      <line x1="250" y1="275" x2="330" y2="275" stroke="{wire_in_col}" stroke-width="3"/>
      <!-- Base Current Indicator -->
      <text x="255" y="300" fill="#94a3b8" font-size="11">I_B = {i_b_ua:.1f} µA →</text>

      <!-- TRANSISTOR NPN SYMBOL -->
      <!-- Transistor Circle Enclosure -->
      <circle cx="390" cy="275" r="50" fill="#0b1120" stroke="{transistor_glow}" stroke-width="2.5" filter="url(#glow-green)"/>

      <!-- Base Bar -->
      <line x1="365" y1="245" x2="365" y2="305" stroke="#f8fafc" stroke-width="4.5" stroke-linecap="round"/>
      <!-- Connection from Base lead to Bar -->
      <line x1="330" y1="275" x2="365" y2="275" stroke="{wire_in_col}" stroke-width="3"/>

      <!-- Collector Lead (Slanted) -->
      <line x1="365" y1="255" x2="420" y2="225" stroke="{wire_vcc_col}" stroke-width="3"/>
      <line x1="420" y1="225" x2="420" y2="240" stroke="{wire_vcc_col}" stroke-width="3"/>

      <!-- Emitter Lead (Slanted with Arrow for NPN pointing outwards) -->
      <line x1="365" y1="295" x2="420" y2="325" stroke="#94a3b8" stroke-width="3"/>
      <!-- NPN Arrow on Emitter -->
      <polygon points="402,311 416,323 397,322" fill="#38bdf8"/>

      <!-- Transistor Labels -->
      <text x="345" y="240" fill="#94a3b8" font-size="11">B</text>
      <text x="425" y="238" fill="#94a3b8" font-size="11">C</text>
      <text x="425" y="325" fill="#94a3b8" font-size="11">E</text>
      <text x="375" y="278" fill="#cbd5e1" font-size="11" font-weight="bold">NPN</text>

      <!-- SWITCH CONDUCTION CHANNEL VISUALIZER -->
      <rect x="361" y="255" width="8" height="40" fill="{'#22c55e' if is_on else ('#f59e0b' if is_active else '#334155')}" rx="4"/>

      <!-- Emitter Connection to Ground -->
      <line x1="420" y1="325" x2="420" y2="400" stroke="#94a3b8" stroke-width="3"/>
      <!-- Ground Symbol -->
      <line x1="400" y1="400" x2="440" y2="400" stroke="#94a3b8" stroke-width="3.5"/>
      <line x1="407" y1="408" x2="433" y2="408" stroke="#94a3b8" stroke-width="2.5"/>
      <line x1="414" y1="416" x2="426" y2="416" stroke="#94a3b8" stroke-width="2"/>
      <text x="445" y="412" fill="#94a3b8" font-size="12">GND (0V)</text>

      <!-- SWITCH STATUS DIAGRAM INSET (Bottom-Right) -->
      <rect x="540" y="320" width="190" height="110" rx="10" fill="#0f172a" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
      <text x="555" y="342" fill="#94a3b8" font-size="11">EQUIVALENT SWITCH</text>
      <!-- Equivalent Switch Contacts -->
      <circle cx="580" cy="380" r="5" fill="#38bdf8"/>
      <circle cx="650" cy="380" r="5" fill="#38bdf8"/>
      <!-- Switch Blade -->
      {'<line x1="580" y1="380" x2="650" y2="380" stroke="#22c55e" stroke-width="4" stroke-linecap="round"/>' if is_on else '<line x1="580" y1="380" x2="635" y2="355" stroke="#ef4444" stroke-width="3.5" stroke-linecap="round"/>'}
      <text x="565" y="415" fill="{'#4ade80' if is_on else '#f87171'}" font-size="12" font-weight="bold">
        {"SWITCH: CLOSED (ON)" if is_on else ("SWITCH: PARTIAL (ACTIVE)" if is_active else "SWITCH: OPEN (OFF)")}
      </text>
    </svg>
    """
    return clean_svg(svg)


def generate_logic_gate_symbol_svg(gate_name, in_a, in_b=0, out_val=0):
    """
    Generates an IEEE standard logic gate SVG symbol with live active wires.
    Supported gates: NOT, AND, OR, NAND, NOR, XOR.
    """
    col_high = "#22c55e"
    col_low = "#475569"
    
    col_a = col_high if in_a else col_low
    col_b = col_high if in_b else col_low
    col_out = col_high if out_val else col_low
    
    is_single_input = (gate_name == "NOT")

    svg_header = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 260" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style="background:#090d16; border-radius:12px; font-family:'JetBrains Mono', monospace;">
      <defs>
        <filter id="glow-out" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="5" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>
      
      <!-- Gate Title -->
      <text x="24" y="32" fill="#cbd5e1" font-size="14" font-weight="bold">{gate_name} GATE SYMBOL</text>
      
      <!-- Input A -->
      <line x1="50" y1="{130 if is_single_input else 95}" x2="190" y2="{130 if is_single_input else 95}" stroke="{col_a}" stroke-width="4"/>
      <circle cx="50" cy="{130 if is_single_input else 95}" r="7" fill="{col_a}"/>
      <text x="20" y="{135 if is_single_input else 100}" fill="{col_a}" font-size="14" font-weight="bold">A={in_a}</text>
    """

    svg_input_b = ""
    if not is_single_input:
        svg_input_b = f"""
        <!-- Input B -->
        <line x1="50" y1="165" x2="190" y2="165" stroke="{col_b}" stroke-width="4"/>
        <circle cx="50" cy="165" r="7" fill="{col_b}"/>
        <text x="20" y="170" fill="{col_b}" font-size="14" font-weight="bold">B={in_b}</text>
        """

    shape_svg = ""
    out_wire_start_x = 350
    if gate_name == "NOT":
        shape_svg = """
        <polygon points="190,80 190,180 290,130" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
        <circle cx="302" cy="130" r="10" fill="#090d16" stroke="#38bdf8" stroke-width="3"/>
        """
        out_wire_start_x = 314
    elif gate_name == "AND":
        shape_svg = """
        <path d="M 190 75 L 255 75 A 55 55 0 0 1 255 185 L 190 185 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
        """
        out_wire_start_x = 310
    elif gate_name == "NAND":
        shape_svg = """
        <path d="M 190 75 L 255 75 A 55 55 0 0 1 255 185 L 190 185 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
        <circle cx="320" cy="130" r="10" fill="#090d16" stroke="#38bdf8" stroke-width="3"/>
        """
        out_wire_start_x = 332
    elif gate_name == "OR":
        shape_svg = """
        <path d="M 180 75 Q 225 130 180 185 Q 260 185 320 130 Q 260 75 180 75 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
        """
        out_wire_start_x = 320
    elif gate_name == "NOR":
        shape_svg = """
        <path d="M 180 75 Q 225 130 180 185 Q 260 185 320 130 Q 260 75 180 75 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
        <circle cx="332" cy="130" r="10" fill="#090d16" stroke="#38bdf8" stroke-width="3"/>
        """
        out_wire_start_x = 344
    elif gate_name == "XOR":
        shape_svg = """
        <path d="M 165 75 Q 210 130 165 185" fill="none" stroke="#38bdf8" stroke-width="3"/>
        <path d="M 180 75 Q 225 130 180 185 Q 260 185 320 130 Q 260 75 180 75 Z" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
        """
        out_wire_start_x = 320

    svg_output = f"""
      <!-- Output Wire -->
      <line x1="{out_wire_start_x}" y1="130" x2="430" y2="130" stroke="{col_out}" stroke-width="4"/>
      <circle cx="430" cy="130" r="8" fill="{col_out}" filter="url(#glow-out)"/>
      <text x="450" y="135" fill="{col_out}" font-size="16" font-weight="bold">Q = {out_val}</text>
      
      <!-- State label below output -->
      <text x="450" y="158" fill="#94a3b8" font-size="11">{"(HIGH)" if out_val else "(LOW)"}</text>
    </svg>
    """
    return clean_svg(svg_header + svg_input_b + shape_svg + svg_output)


def draw_npn_bjt(
    cx: int,
    cy: int,
    label: str = "T1",
    is_on: bool = False,
    base_col: str = "#64748b",
    collector_col: str = "#38bdf8",
    emitter_col: str = "#94a3b8",
    r: int = 26,
) -> str:
    """
    Renders an IEEE standard NPN Bipolar Junction Transistor (BJT) schematic symbol.
    - Base terminal on LEFT at (cx - r, cy)
    - Collector terminal on TOP at (cx + 12, cy - r)
    - Emitter terminal on BOTTOM at (cx + 12, cy + r) with standard outward arrow
    - Circle enclosure of radius r centered at (cx, cy)
    - High-contrast styling with white base bar and vivid conduction highlights
    """
    circle_stroke = "#22c55e" if is_on else "#475569"
    circle_fill = "#0f172a"
    arrow_col = "#22c55e" if is_on else "#38bdf8"
    active_channel = (
        f'<line x1="{cx - 8}" y1="{cy - 8}" x2="{cx - 8}" y2="{cy + 8}" stroke="#22c55e" stroke-width="4.5" opacity="0.95"/>'
        if is_on
        else ""
    )

    return f"""
    <!-- NPN Transistor {label} -->
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="{circle_fill}" stroke="{circle_stroke}" stroke-width="2.5"/>
    <!-- Base Bar (Thick White Solid Segment) -->
    <line x1="{cx - 9}" y1="{cy - 16}" x2="{cx - 9}" y2="{cy + 16}" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
    <!-- Base Lead (Left) -->
    <line x1="{cx - r}" y1="{cy}" x2="{cx - 9}" y2="{cy}" stroke="{base_col}" stroke-width="2.5"/>
    <!-- Collector Lead (Top: slants up-right from base bar, then straight up to top edge) -->
    <line x1="{cx - 9}" y1="{cy - 7}" x2="{cx + 12}" y2="{cy - 17}" stroke="{collector_col}" stroke-width="2.5"/>
    <line x1="{cx + 12}" y1="{cy - 17}" x2="{cx + 12}" y2="{cy - r}" stroke="{collector_col}" stroke-width="2.5"/>
    <!-- Emitter Lead (Bottom: slants down-right from base bar, then straight down to bottom edge) -->
    <line x1="{cx - 9}" y1="{cy + 7}" x2="{cx + 12}" y2="{cy + 17}" stroke="{emitter_col}" stroke-width="2.5"/>
    <line x1="{cx + 12}" y1="{cy + 17}" x2="{cx + 12}" y2="{cy + r}" stroke="{emitter_col}" stroke-width="2.5"/>
    <!-- Emitter Outward NPN Arrowhead (points along emitter lead) -->
    <polygon points="{cx + 11},{cy + 16.5} {cx + 3},{cy + 9.5} {cx + 4.5},{cy + 17.5}" fill="{arrow_col}"/>
    {active_channel}
    <!-- Pin Labels: B, C, E -->
    <text x="{cx - 20}" y="{cy - 5}" fill="#94a3b8" font-size="9" font-weight="bold">B</text>
    <text x="{cx + 15}" y="{cy - 14}" fill="#94a3b8" font-size="9" font-weight="bold">C</text>
    <text x="{cx + 15}" y="{cy + 22}" fill="#94a3b8" font-size="9" font-weight="bold">E</text>
    <!-- Transistor Identifier -->
    <text x="{cx - 2}" y="{cy - 2}" fill="{'#4ade80' if is_on else '#f8fafc'}" font-size="10.5" font-weight="bold">{label}</text>
    """


def draw_vcc_rail(x: int, y: int, label: str = "+V_CC (5V)") -> str:
    """Renders a standard V_CC power supply rail terminal."""
    return f"""
    <circle cx="{x}" cy="{y}" r="4" fill="#38bdf8"/>
    <line x1="{x - 12}" y1="{y}" x2="{x + 12}" y2="{y}" stroke="#38bdf8" stroke-width="2.5"/>
    <text x="{x + 16}" y="{y + 4}" fill="#38bdf8" font-size="11" font-weight="bold">{label}</text>
    """


def draw_ground_symbol(x: int, y: int) -> str:
    """Renders an IEEE standard ground symbol."""
    return f"""
    <line x1="{x}" y1="{y}" x2="{x}" y2="{y + 8}" stroke="#94a3b8" stroke-width="2.5"/>
    <line x1="{x - 14}" y1="{y + 8}" x2="{x + 14}" y2="{y + 8}" stroke="#94a3b8" stroke-width="3"/>
    <line x1="{x - 9}" y1="{y + 14}" x2="{x + 9}" y2="{y + 14}" stroke="#94a3b8" stroke-width="2"/>
    <line x1="{x - 4}" y1="{y + 20}" x2="{x + 4}" y2="{y + 20}" stroke="#94a3b8" stroke-width="1.5"/>
    <text x="{x + 16}" y="{y + 15}" fill="#94a3b8" font-size="10">GND (0V)</text>
    """


def draw_resistor(x: int, y: int, w: int, h: int, label: str = "", color: str = "#38bdf8") -> str:
    """Renders an IEC resistor symbol with intelligent label placement avoiding wire collisions."""
    if label:
        if h > w:  # Vertical resistor (pull-up): label placed to the right
            label_markup = f'<text x="{x + w + 7}" y="{y + h // 2 + 4}" fill="#94a3b8" font-size="9.5">{label}</text>'
        else:  # Horizontal resistor: label centered directly above
            label_markup = f'<text x="{x + w // 2}" y="{y - 5}" text-anchor="middle" fill="#94a3b8" font-size="9.5">{label}</text>'
    else:
        label_markup = ""
    return f"""
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="#1e293b" stroke="{color}" stroke-width="1.8"/>
    {label_markup}
    """


def generate_transistor_logic_circuit_svg(gate_name, in_a, in_b=0, out_val=0):
    """
    Generates a transistor-level schematic (RTL / TTL style) showing how physical
    NPN BJT transistors form the logic gate with standard orientation:
    - Base on LEFT, Collector on TOP, Emitter on BOTTOM with outward arrow.
    - NOT: Single NPN switch with pull-up resistor.
    - NAND: 2 NPN switches in series pull-down stack with pull-up.
    - AND: NAND stage (2 series NPNs) followed by Inverter stage (1 NPN).
    - NOR: 2 NPN switches in parallel pull-down with pull-up.
    - OR: NOR stage (2 parallel NPNs) followed by Inverter stage (1 NPN).
    - XOR: 4 NPN dual series-parallel RTL branches (A·B' + A'·B) followed by Inverter stage (T5).
    """
    col_high = "#22c55e"
    col_low = "#64748b"
    col_out = col_high if out_val else col_low

    t_a_on = bool(in_a)
    t_b_on = bool(in_b)

    svg_base = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 5 750 330" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style="background:#090d16; border-radius:12px; font-family:'JetBrains Mono', monospace;">
      <defs>
        <pattern id="grid-logic" width="20" height="20" patternUnits="userSpaceOnUse">
          <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(255,255,255,0.02)" stroke-width="1"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#grid-logic)"/>
    """

    if gate_name == "NOT":
        col_in_a = col_high if in_a else col_low
        svg_content = f"""
          <text x="25" y="24" fill="#cbd5e1" font-size="12" font-weight="bold">TRANSISTOR INVERTER (NOT GATE) SCHEMATIC</text>
          
          <!-- VCC Rail & Pull-Up Resistor -->
          {draw_vcc_rail(372, 50)}
          <line x1="372" y1="50" x2="372" y2="70" stroke="#38bdf8" stroke-width="2.5"/>
          {draw_resistor(360, 70, 24, 45, "R_pullup (1 kΩ)", "#38bdf8")}
          <line x1="372" y1="115" x2="372" y2="184" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Output Node Junction -->
          <circle cx="372" cy="140" r="5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <line x1="372" y1="140" x2="560" y2="140" stroke="{col_out}" stroke-width="3.5"/>
          <circle cx="560" cy="140" r="6" fill="{col_out}"/>
          <text x="575" y="145" fill="{col_out}" font-size="16" font-weight="bold">Q = {out_val}</text>
          <text x="575" y="165" fill="#94a3b8" font-size="11">{"(HIGH: V_CC)" if out_val else "(LOW: 0V)"}</text>
          
          <!-- Input A Terminal & Base Resistor -->
          <circle cx="90" cy="210" r="6" fill="{col_in_a}"/>
          <text x="35" y="215" fill="{col_in_a}" font-size="13" font-weight="bold">IN A={in_a}</text>
          <line x1="96" y1="210" x2="190" y2="210" stroke="{col_in_a}" stroke-width="2.5"/>
          {draw_resistor(190, 202, 45, 16, "R_B (10 kΩ)", col_in_a)}
          <line x1="235" y1="210" x2="334" y2="210" stroke="{col_in_a}" stroke-width="2.5"/>
          
          <!-- Transistor T1 (NPN Standard Orientation: Base Left, Collector Top, Emitter Bottom) -->
          {draw_npn_bjt(360, 210, "T1", t_a_on, col_in_a, "#38bdf8", "#94a3b8")}
          
          <!-- Emitter to Ground -->
          <line x1="372" y1="236" x2="372" y2="305" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(372, 305)}
          
          <!-- Status Explanatory Card -->
          <rect x="520" y="235" width="220" height="85" rx="8" fill="#131d2e" stroke="rgba(255,255,255,0.1)"/>
          <text x="535" y="260" fill="#cbd5e1" font-size="11">Switching Behavior:</text>
          <text x="535" y="282" fill="{'#4ade80' if in_a else '#f87171'}" font-size="11" font-weight="bold">
            {"T1 ON: Pulls output to GND (0)" if in_a else "T1 OFF: R_pullup pulls to VCC (1)"}
          </text>
          <text x="535" y="302" fill="#94a3b8" font-size="10">Standard Common-Emitter Inverter</text>
        """

    elif gate_name == "NAND":
        col_in_a = col_high if in_a else col_low
        col_in_b = col_high if in_b else col_low
        both_on = t_a_on and t_b_on

        svg_content = f"""
          <text x="25" y="30" fill="#cbd5e1" font-size="13" font-weight="bold">TRANSISTOR NAND SCHEMATIC (SERIES NPN STACK)</text>
          
          <!-- VCC Rail & Pull-Up Resistor -->
          {draw_vcc_rail(320, 45)}
          <line x1="320" y1="45" x2="320" y2="70" stroke="#38bdf8" stroke-width="2.5"/>
          {draw_resistor(308, 70, 24, 42, "R_pullup (1 kΩ)", "#38bdf8")}
          <line x1="320" y1="112" x2="320" y2="149" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Output Node Junction -->
          <circle cx="320" cy="130" r="5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <line x1="320" y1="130" x2="560" y2="130" stroke="{col_out}" stroke-width="3.5"/>
          <circle cx="560" cy="130" r="6" fill="{col_out}"/>
          <text x="575" y="135" fill="{col_out}" font-size="16" font-weight="bold">Q = {out_val}</text>
          <text x="575" y="155" fill="#94a3b8" font-size="11">{"(HIGH: Pull-Up)" if out_val else "(LOW: Pulled to GND)"}</text>
          
          <!-- Input A Terminal & Base Resistor -->
          <circle cx="80" cy="175" r="5" fill="{col_in_a}"/>
          <text x="35" y="180" fill="{col_in_a}" font-size="12" font-weight="bold">IN A={in_a}</text>
          <line x1="86" y1="175" x2="170" y2="175" stroke="{col_in_a}" stroke-width="2.5"/>
          {draw_resistor(170, 167, 40, 16, "R_B1", col_in_a)}
          <line x1="210" y1="175" x2="282" y2="175" stroke="{col_in_a}" stroke-width="2.5"/>
          
          <!-- Transistor T1 (Top of Series Stack) -->
          {draw_npn_bjt(308, 175, "T1", t_a_on, col_in_a, "#38bdf8", "#38bdf8")}
          
          <!-- Series Connection: Emitter of T1 (320, 201) to Collector of T2 (320, 224) -->
          <line x1="320" y1="201" x2="320" y2="224" stroke="{'#22c55e' if t_a_on else '#38bdf8'}" stroke-width="2.5"/>
          <circle cx="320" cy="212" r="3" fill="#38bdf8"/>
          <text x="330" y="216" fill="#94a3b8" font-size="10">Series Interstage</text>
          
          <!-- Input B Terminal & Base Resistor -->
          <circle cx="80" cy="250" r="5" fill="{col_in_b}"/>
          <text x="35" y="255" fill="{col_in_b}" font-size="12" font-weight="bold">IN B={in_b}</text>
          <line x1="86" y1="250" x2="170" y2="250" stroke="{col_in_b}" stroke-width="2.5"/>
          {draw_resistor(170, 242, 40, 16, "R_B2", col_in_b)}
          <line x1="210" y1="250" x2="282" y2="250" stroke="{col_in_b}" stroke-width="2.5"/>
          
          <!-- Transistor T2 (Bottom of Series Stack) -->
          {draw_npn_bjt(308, 250, "T2", t_b_on, col_in_b, "#38bdf8", "#94a3b8")}
          
          <!-- Emitter of T2 to Ground -->
          <line x1="320" y1="276" x2="320" y2="315" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(320, 315)}
          
          <!-- Explanatory Operation Card -->
          <rect x="470" y="200" width="265" height="95" rx="8" fill="#131d2e" stroke="rgba(255,255,255,0.1)"/>
          <text x="485" y="225" fill="#cbd5e1" font-size="11">Series Pull-Down Operation:</text>
          <text x="485" y="248" fill="{'#4ade80' if both_on else '#38bdf8'}" font-size="11" font-weight="bold">
            {"BOTH T1 & T2 ON: Complete GND path -> Q = 0" if both_on else "At least one OFF: Path broken -> Q = 1"}
          </text>
          <text x="485" y="272" fill="#94a3b8" font-size="10">T1: Collector(top) Emitter(bottom)</text>
          <text x="485" y="286" fill="#94a3b8" font-size="10">T2: Collector(top) Emitter(bottom to GND)</text>
        """

    elif gate_name == "AND":
        col_in_a = col_high if in_a else col_low
        col_in_b = col_high if in_b else col_low
        both_on = t_a_on and t_b_on
        nand_node_val = 0 if both_on else 1
        col_nand_node = col_high if nand_node_val else col_low

        svg_content = f"""
          <text x="25" y="24" fill="#cbd5e1" font-size="12" font-weight="bold">TRANSISTOR AND SCHEMATIC (NAND STACK + INVERTER STAGE)</text>
          
          <!-- Stage 1 Title (Centered right above the NAND column) -->
          <text x="240" y="38" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="bold">STAGE 1: NAND CORE</text>
          
          <!-- VCC Rail & Pull-Up for NAND Stack -->
          {draw_vcc_rail(240, 52, "+V_CC")}
          <line x1="240" y1="52" x2="240" y2="70" stroke="#38bdf8" stroke-width="2"/>
          {draw_resistor(228, 70, 24, 38, "R_C1", "#38bdf8")}
          <line x1="240" y1="108" x2="240" y2="149" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Intermediate NAND Node -->
          <circle cx="240" cy="130" r="4.5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <text x="250" y="125" fill="#94a3b8" font-size="10">V_NAND={nand_node_val}</text>
          
          <!-- Input A Terminal & Base Resistor -->
          <circle cx="50" cy="175" r="5" fill="{col_in_a}"/>
          <text x="12" y="180" fill="{col_in_a}" font-size="12" font-weight="bold">A={in_a}</text>
          <line x1="56" y1="175" x2="130" y2="175" stroke="{col_in_a}" stroke-width="2.5"/>
          {draw_resistor(130, 167, 36, 16, "R_B1", col_in_a)}
          <line x1="166" y1="175" x2="202" y2="175" stroke="{col_in_a}" stroke-width="2.5"/>
          
          <!-- Transistor T1 (Top of NAND Stack) -->
          {draw_npn_bjt(228, 175, "T1", t_a_on, col_in_a, "#38bdf8", "#38bdf8")}
          
          <!-- Series Connection between T1 and T2 -->
          <line x1="240" y1="201" x2="240" y2="224" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Input B Terminal & Base Resistor -->
          <circle cx="50" cy="250" r="5" fill="{col_in_b}"/>
          <text x="12" y="255" fill="{col_in_b}" font-size="12" font-weight="bold">B={in_b}</text>
          <line x1="56" y1="250" x2="130" y2="250" stroke="{col_in_b}" stroke-width="2.5"/>
          {draw_resistor(130, 242, 36, 16, "R_B2", col_in_b)}
          <line x1="166" y1="250" x2="202" y2="250" stroke="{col_in_b}" stroke-width="2.5"/>
          
          <!-- Transistor T2 (Bottom of NAND Stack) -->
          {draw_npn_bjt(228, 250, "T2", t_b_on, col_in_b, "#38bdf8", "#94a3b8")}
          
          <!-- Emitter of T2 to Ground -->
          <line x1="240" y1="276" x2="240" y2="315" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(240, 315)}
          
          <!-- Coupling Line from NAND Node to Inverter Stage -->
          <line x1="240" y1="130" x2="320" y2="130" stroke="{col_nand_node}" stroke-width="2.5"/>
          {draw_resistor(320, 122, 38, 16, "R_B3", col_nand_node)}
          <line x1="358" y1="130" x2="395" y2="130" stroke="{col_nand_node}" stroke-width="2.5"/>
          <line x1="395" y1="130" x2="395" y2="205" stroke="{col_nand_node}" stroke-width="2.5"/>
          <line x1="395" y1="205" x2="438" y2="205" stroke="{col_nand_node}" stroke-width="2.5"/>
          
          <!-- Stage 2 Title (Centered right above the Inverter column) -->
          <text x="476" y="38" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="bold">STAGE 2: INVERTER (NOT)</text>
          
          <!-- Inverter VCC Rail & Pull-Up -->
          {draw_vcc_rail(476, 52, "+V_CC")}
          <line x1="476" y1="52" x2="476" y2="70" stroke="#38bdf8" stroke-width="2"/>
          {draw_resistor(464, 70, 24, 38, "R_C3", "#38bdf8")}
          <line x1="476" y1="108" x2="476" y2="179" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Inverter Transistor T3 (Base Left, Collector Top, Emitter Bottom) -->
          {draw_npn_bjt(464, 205, "T3", bool(nand_node_val), col_nand_node, "#38bdf8", "#94a3b8")}
          
          <!-- Inverter Emitter to Ground -->
          <line x1="476" y1="231" x2="476" y2="305" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(476, 305)}
          
          <!-- Final AND Output -->
          <circle cx="476" cy="130" r="5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <line x1="476" y1="130" x2="620" y2="130" stroke="{col_out}" stroke-width="3.5"/>
          <circle cx="620" cy="130" r="6" fill="{col_out}"/>
          <text x="635" y="135" fill="{col_out}" font-size="16" font-weight="bold">Q = {out_val}</text>
          <text x="635" y="155" fill="#94a3b8" font-size="11">{"(HIGH: True)" if out_val else "(LOW: False)"}</text>
          
          <!-- Logic Summary -->
          <rect x="520" y="225" width="220" height="75" rx="8" fill="#131d2e" stroke="rgba(255,255,255,0.1)"/>
          <text x="535" y="250" fill="#cbd5e1" font-size="11">Operation:</text>
          <text x="535" y="270" fill="{'#4ade80' if out_val else '#94a3b8'}" font-size="11" font-weight="bold">
            {"NAND 0 -> T3 OFF -> Q = 1" if out_val else "NAND 1 -> T3 ON -> Q = 0"}
          </text>
          <text x="535" y="288" fill="#94a3b8" font-size="10">All NPNs: C up, E down, B left</text>
        """

    elif gate_name == "NOR":
        col_in_a = col_high if in_a else col_low
        col_in_b = col_high if in_b else col_low
        any_on = t_a_on or t_b_on

        svg_content = f"""
          <text x="25" y="30" fill="#cbd5e1" font-size="13" font-weight="bold">TRANSISTOR NOR SCHEMATIC (PARALLEL NPN PULL-DOWN)</text>
          
          <!-- VCC Rail & Pull-Up Resistor -->
          {draw_vcc_rail(310, 45)}
          <line x1="310" y1="45" x2="310" y2="70" stroke="#38bdf8" stroke-width="2.5"/>
          {draw_resistor(298, 70, 24, 42, "R_pullup (1 kΩ)", "#38bdf8")}
          <line x1="310" y1="112" x2="310" y2="150" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Output Node Junction -->
          <circle cx="310" cy="130" r="5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <line x1="310" y1="130" x2="560" y2="130" stroke="{col_out}" stroke-width="3.5"/>
          <circle cx="560" cy="130" r="6" fill="{col_out}"/>
          <text x="575" y="135" fill="{col_out}" font-size="16" font-weight="bold">Q = {out_val}</text>
          <text x="575" y="155" fill="#94a3b8" font-size="11">{"(HIGH: Pull-Up)" if out_val else "(LOW: Pulled to GND)"}</text>
          
          <!-- Parallel Collector Bus (Connects collectors of T1 and T2 together) -->
          <line x1="240" y1="150" x2="380" y2="150" stroke="#38bdf8" stroke-width="2.5"/>
          <line x1="240" y1="150" x2="240" y2="176" stroke="#38bdf8" stroke-width="2.5"/>
          <line x1="380" y1="150" x2="380" y2="176" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Input A Terminal & Branch T1 -->
          <circle cx="50" cy="165" r="5" fill="{col_in_a}"/>
          <text x="12" y="170" fill="{col_in_a}" font-size="12" font-weight="bold">IN A={in_a}</text>
          <line x1="56" y1="165" x2="110" y2="165" stroke="{col_in_a}" stroke-width="2"/>
          <line x1="110" y1="165" x2="110" y2="200" stroke="{col_in_a}" stroke-width="2"/>
          <line x1="110" y1="200" x2="135" y2="200" stroke="{col_in_a}" stroke-width="2"/>
          {draw_resistor(135, 192, 36, 16, "R_B1", col_in_a)}
          <line x1="171" y1="200" x2="202" y2="200" stroke="{col_in_a}" stroke-width="2.5"/>
          
          <!-- Transistor T1 (Branch A: Base Left, Collector Top, Emitter Bottom) -->
          {draw_npn_bjt(228, 200, "T1", t_a_on, col_in_a, "#38bdf8", "#94a3b8")}
          
          <!-- Input B Terminal & Branch T2 -->
          <circle cx="50" cy="270" r="5" fill="{col_in_b}"/>
          <text x="12" y="275" fill="{col_in_b}" font-size="12" font-weight="bold">IN B={in_b}</text>
          <line x1="56" y1="270" x2="280" y2="270" stroke="{col_in_b}" stroke-width="2"/>
          <line x1="280" y1="270" x2="280" y2="200" stroke="{col_in_b}" stroke-width="2"/>
          <line x1="280" y1="200" x2="295" y2="200" stroke="{col_in_b}" stroke-width="2"/>
          {draw_resistor(295, 192, 36, 16, "R_B2", col_in_b)}
          <line x1="331" y1="200" x2="342" y2="200" stroke="{col_in_b}" stroke-width="2.5"/>
          
          <!-- Transistor T2 (Branch B: Base Left, Collector Top, Emitter Bottom) -->
          {draw_npn_bjt(368, 200, "T2", t_b_on, col_in_b, "#38bdf8", "#94a3b8")}
          
          <!-- Parallel Emitter Bus (Connects emitters of T1 and T2 together to GND) -->
          <line x1="240" y1="224" x2="240" y2="250" stroke="#94a3b8" stroke-width="2.5"/>
          <line x1="380" y1="224" x2="380" y2="250" stroke="#94a3b8" stroke-width="2.5"/>
          <line x1="240" y1="250" x2="380" y2="250" stroke="#94a3b8" stroke-width="2.5"/>
          <line x1="310" y1="250" x2="310" y2="305" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(310, 305)}
          
          <!-- Explanatory Operation Card -->
          <rect x="470" y="200" width="265" height="95" rx="8" fill="#131d2e" stroke="rgba(255,255,255,0.1)"/>
          <text x="485" y="225" fill="#cbd5e1" font-size="11">Parallel Pull-Down Operation:</text>
          <text x="485" y="248" fill="{'#f87171' if any_on else '#4ade80'}" font-size="11" font-weight="bold">
            {"Either T1 or T2 ON: Pulls output to 0" if any_on else "Both T1 & T2 OFF: Output pulled to 1"}
          </text>
          <text x="485" y="272" fill="#94a3b8" font-size="10">T1: Collector(top) Emitter(bottom)</text>
          <text x="485" y="286" fill="#94a3b8" font-size="10">T2: Collector(top) Emitter(bottom)</text>
        """

    elif gate_name == "OR":
        col_in_a = col_high if in_a else col_low
        col_in_b = col_high if in_b else col_low
        any_on = t_a_on or t_b_on
        nor_node_val = 0 if any_on else 1
        col_nor_node = col_high if nor_node_val else col_low

        svg_content = f"""
          <text x="25" y="24" fill="#cbd5e1" font-size="12" font-weight="bold">TRANSISTOR OR SCHEMATIC (NOR STAGE + INVERTER STAGE)</text>
          
          <!-- Stage 1 Title (Centered right above NOR core) -->
          <text x="240" y="38" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="bold">STAGE 1: NOR CORE</text>
          
          <!-- NOR VCC Rail & Pull-Up -->
          {draw_vcc_rail(240, 52, "+V_CC")}
          <line x1="240" y1="52" x2="240" y2="70" stroke="#38bdf8" stroke-width="2"/>
          {draw_resistor(228, 70, 24, 38, "R_C1", "#38bdf8")}
          <line x1="240" y1="108" x2="240" y2="150" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Intermediate NOR Node -->
          <circle cx="240" cy="130" r="4.5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <text x="250" y="125" fill="#94a3b8" font-size="10">V_NOR={nor_node_val}</text>
          
          <!-- Parallel Collector Bus for T1 and T2 -->
          <line x1="178" y1="150" x2="298" y2="150" stroke="#38bdf8" stroke-width="2.5"/>
          <line x1="178" y1="150" x2="178" y2="176" stroke="#38bdf8" stroke-width="2.5"/>
          <line x1="298" y1="150" x2="298" y2="176" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Input A Terminal & Branch T1 -->
          <circle cx="35" cy="170" r="5" fill="{col_in_a}"/>
          <text x="8" y="175" fill="{col_in_a}" font-size="12" font-weight="bold">A={in_a}</text>
          <line x1="41" y1="170" x2="90" y2="170" stroke="{col_in_a}" stroke-width="2"/>
          <line x1="90" y1="170" x2="90" y2="200" stroke="{col_in_a}" stroke-width="2"/>
          <line x1="90" y1="200" x2="110" y2="200" stroke="{col_in_a}" stroke-width="2"/>
          {draw_resistor(110, 192, 34, 16, "R_B1", col_in_a)}
          <line x1="144" y1="200" x2="152" y2="200" stroke="{col_in_a}" stroke-width="2.5"/>
          
          <!-- Transistor T1 (Branch A: Base Left, Collector Top, Emitter Bottom) -->
          {draw_npn_bjt(178, 200, "T1", t_a_on, col_in_a, "#38bdf8", "#94a3b8")}
          
          <!-- Input B Terminal & Branch T2 -->
          <circle cx="35" cy="270" r="5" fill="{col_in_b}"/>
          <text x="8" y="275" fill="{col_in_b}" font-size="12" font-weight="bold">B={in_b}</text>
          <line x1="41" y1="270" x2="220" y2="270" stroke="{col_in_b}" stroke-width="2"/>
          <line x1="220" y1="270" x2="220" y2="200" stroke="{col_in_b}" stroke-width="2"/>
          <line x1="220" y1="200" x2="230" y2="200" stroke="{col_in_b}" stroke-width="2"/>
          {draw_resistor(230, 192, 34, 16, "R_B2", col_in_b)}
          <line x1="264" y1="200" x2="272" y2="200" stroke="{col_in_b}" stroke-width="2.5"/>
          
          <!-- Transistor T2 (Branch B: Base Left, Collector Top, Emitter Bottom) -->
          {draw_npn_bjt(298, 200, "T2", t_b_on, col_in_b, "#38bdf8", "#94a3b8")}
          
          <!-- Parallel Emitter Bus to Ground -->
          <line x1="190" y1="224" x2="190" y2="250" stroke="#94a3b8" stroke-width="2.5"/>
          <line x1="310" y1="224" x2="310" y2="250" stroke="#94a3b8" stroke-width="2.5"/>
          <line x1="190" y1="250" x2="310" y2="250" stroke="#94a3b8" stroke-width="2.5"/>
          <line x1="250" y1="250" x2="250" y2="305" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(250, 305)}
          
          <!-- Coupling to Inverter Stage -->
          <line x1="240" y1="130" x2="345" y2="130" stroke="{col_nor_node}" stroke-width="2.5"/>
          {draw_resistor(345, 122, 38, 16, "R_B3", col_nor_node)}
          <line x1="383" y1="130" x2="410" y2="130" stroke="{col_nor_node}" stroke-width="2.5"/>
          <line x1="410" y1="130" x2="410" y2="205" stroke="{col_nor_node}" stroke-width="2.5"/>
          <line x1="410" y1="205" x2="438" y2="205" stroke="{col_nor_node}" stroke-width="2.5"/>
          
          <!-- Stage 2 Title (Centered right above Inverter column) -->
          <text x="476" y="38" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="bold">STAGE 2: INVERTER (NOT)</text>
          
          <!-- Inverter VCC & Pull-Up -->
          {draw_vcc_rail(476, 52, "+V_CC")}
          <line x1="476" y1="52" x2="476" y2="70" stroke="#38bdf8" stroke-width="2"/>
          {draw_resistor(464, 70, 24, 38, "R_C3", "#38bdf8")}
          <line x1="476" y1="108" x2="476" y2="179" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Inverter Transistor T3 (Base Left, Collector Top, Emitter Bottom) -->
          {draw_npn_bjt(464, 205, "T3", bool(nor_node_val), col_nor_node, "#38bdf8", "#94a3b8")}
          
          <!-- Inverter Emitter to Ground -->
          <line x1="476" y1="229" x2="476" y2="305" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(476, 305)}
          
          <!-- Final OR Output -->
          <circle cx="476" cy="130" r="5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <line x1="476" y1="130" x2="620" y2="130" stroke="{col_out}" stroke-width="3.5"/>
          <circle cx="620" cy="130" r="6" fill="{col_out}"/>
          <text x="635" y="135" fill="{col_out}" font-size="16" font-weight="bold">Q = {out_val}</text>
          <text x="635" y="155" fill="#94a3b8" font-size="11">{"(HIGH: True)" if out_val else "(LOW: False)"}</text>
          
          <!-- Logic Summary -->
          <rect x="520" y="225" width="220" height="75" rx="8" fill="#131d2e" stroke="rgba(255,255,255,0.1)"/>
          <text x="535" y="250" fill="#cbd5e1" font-size="11">Operation:</text>
          <text x="535" y="270" fill="{'#4ade80' if out_val else '#94a3b8'}" font-size="11" font-weight="bold">
            {"Either IN=1 -> NOR 0 -> T3 OFF -> Q=1" if out_val else "Both IN=0 -> NOR 1 -> T3 ON -> Q=0"}
          </text>
          <text x="535" y="288" fill="#94a3b8" font-size="10">All NPNs: C up, E down, B left</text>
        """

    else:  # XOR Gate
        # Boolean decomposition: Q = A·B' + A'·B
        # Dual Series-Parallel BJT RTL Architecture:
        # Branch 1 (A · B'): T1 (Base A) in series with T2 (Base B')
        # Branch 2 (A' · B): T3 (Base A') in series with T4 (Base B)
        # Intermediate XNOR node: pulled to GND when A ≠ B, pulled to VCC when A = B.
        # Inverter Stage T5: inverts intermediate node to yield Q = A ⊕ B!
        inv_a = int(not in_a)
        inv_b = int(not in_b)
        
        branch1_on = bool(in_a and inv_b)  # A=1, B=0
        branch2_on = bool(inv_a and in_b)  # A=0, B=1
        xnor_node_low = branch1_on or branch2_on  # pulled to GND if A != B
        xnor_node_val = 0 if xnor_node_low else 1
        
        col_in_a = col_high if in_a else col_low
        col_inv_a = col_high if inv_a else col_low
        col_in_b = col_high if in_b else col_low
        col_inv_b = col_high if inv_b else col_low
        col_xnor = col_high if xnor_node_val else col_low

        svg_content = f"""
          <text x="25" y="30" fill="#cbd5e1" font-size="13" font-weight="bold">TRANSISTOR XOR SCHEMATIC (DUAL SERIES BJT BRANCHES + INVERTER)</text>
          
          <!-- Branch 1 Header -->
          <text x="205" y="38" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="bold">BRANCH 1 (A · B')</text>
          
          <!-- Branch 2 Header -->
          <text x="345" y="38" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="bold">BRANCH 2 (A' · B)</text>
          
          <!-- Common Pull-Up for Dual Branches -->
          {draw_vcc_rail(275, 52, "+V_CC")}
          <line x1="275" y1="52" x2="275" y2="70" stroke="#38bdf8" stroke-width="2"/>
          {draw_resistor(263, 70, 24, 38, "R_C", "#38bdf8")}
          <line x1="275" y1="108" x2="275" y2="135" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- XNOR Intermediate Pull-Down Bus -->
          <line x1="205" y1="135" x2="345" y2="135" stroke="#38bdf8" stroke-width="2.5"/>
          <line x1="205" y1="135" x2="205" y2="146" stroke="#38bdf8" stroke-width="2"/>
          <line x1="345" y1="135" x2="345" y2="146" stroke="#38bdf8" stroke-width="2"/>
          <circle cx="275" cy="120" r="4.5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <text x="285" y="116" fill="#94a3b8" font-size="10">V_XNOR={xnor_node_val}</text>
          
          <!-- Input Indicators on Left -->
          <circle cx="25" cy="140" r="4.5" fill="{col_in_a}"/>
          <text x="36" y="144" fill="{col_in_a}" font-size="11" font-weight="bold">A={in_a}</text>
          <text x="75" y="144" fill="{col_inv_a}" font-size="10">A'={inv_a}</text>
          
          <circle cx="25" cy="220" r="4.5" fill="{col_in_b}"/>
          <text x="36" y="224" fill="{col_in_b}" font-size="11" font-weight="bold">B={in_b}</text>
          <text x="75" y="224" fill="{col_inv_b}" font-size="10">B'={inv_b}</text>
          
          <!-- === BRANCH 1: T1 (Base A) in Series with T2 (Base B') === -->
          <!-- Base line to T1 (Driven by A) -->
          <line x1="105" y1="165" x2="169" y2="165" stroke="{col_in_a}" stroke-width="2"/>
          <!-- Transistor T1 -->
          {draw_npn_bjt(193, 165, "T1", t_a_on, col_in_a, "#38bdf8", "#38bdf8", r=21)}
          <!-- Series Connection between T1 emitter (205, 186) and T2 collector (205, 219) -->
          <line x1="205" y1="186" x2="205" y2="219" stroke="#38bdf8" stroke-width="2.5"/>
          <!-- Base line to T2 (Driven by B') -->
          <line x1="105" y1="240" x2="169" y2="240" stroke="{col_inv_b}" stroke-width="2"/>
          <!-- Transistor T2 -->
          {draw_npn_bjt(193, 240, "T2", bool(inv_b), col_inv_b, "#38bdf8", "#94a3b8", r=21)}
          
          <!-- === BRANCH 2: T3 (Base A') in Series with T4 (Base B) === -->
          <!-- Base line to T3 (Driven by A') -->
          <line x1="105" y1="165" x2="309" y2="165" stroke="{col_inv_a}" stroke-width="2" stroke-dasharray="4,3"/>
          <!-- Transistor T3 -->
          {draw_npn_bjt(333, 165, "T3", bool(inv_a), col_inv_a, "#38bdf8", "#38bdf8", r=21)}
          <!-- Series Connection between T3 emitter (345, 186) and T4 collector (345, 219) -->
          <line x1="345" y1="186" x2="345" y2="219" stroke="#38bdf8" stroke-width="2.5"/>
          <!-- Base line to T4 (Driven by B) -->
          <line x1="105" y1="240" x2="309" y2="240" stroke="{col_in_b}" stroke-width="2" stroke-dasharray="4,3"/>
          <!-- Transistor T4 -->
          {draw_npn_bjt(333, 240, "T4", t_b_on, col_in_b, "#38bdf8", "#94a3b8", r=21)}
          
          <!-- Common Ground Bus for Branch 1 and Branch 2 -->
          <line x1="205" y1="261" x2="205" y2="280" stroke="#94a3b8" stroke-width="2"/>
          <line x1="345" y1="261" x2="345" y2="280" stroke="#94a3b8" stroke-width="2"/>
          <line x1="205" y1="280" x2="345" y2="280" stroke="#94a3b8" stroke-width="2.5"/>
          <line x1="275" y1="280" x2="275" y2="315" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(275, 315)}
          
          <!-- === COUPLING TO STAGE 2: INVERTER TRANSISTOR T5 === -->
          <line x1="275" y1="120" x2="390" y2="120" stroke="{col_xnor}" stroke-width="2.5"/>
          {draw_resistor(390, 112, 36, 16, "R_B5", col_xnor)}
          <line x1="426" y1="120" x2="455" y2="120" stroke="{col_xnor}" stroke-width="2.5"/>
          <line x1="455" y1="120" x2="455" y2="200" stroke="{col_xnor}" stroke-width="2.5"/>
          <line x1="455" y1="200" x2="480" y2="200" stroke="{col_xnor}" stroke-width="2.5"/>
          
          <!-- Stage 2 Header -->
          <text x="516" y="38" text-anchor="middle" fill="#38bdf8" font-size="10.5" font-weight="bold">STAGE 2: INVERTER (T5)</text>
          
          <!-- Inverter VCC & Pull-Up -->
          {draw_vcc_rail(516, 52, "+V_CC")}
          <line x1="516" y1="52" x2="516" y2="70" stroke="#38bdf8" stroke-width="2"/>
          {draw_resistor(504, 70, 24, 38, "R_C5", "#38bdf8")}
          <line x1="516" y1="108" x2="516" y2="176" stroke="#38bdf8" stroke-width="2.5"/>
          
          <!-- Inverter Transistor T5 (Base Left, Collector Top, Emitter Bottom) -->
          {draw_npn_bjt(504, 200, "T5", bool(xnor_node_val), col_xnor, "#38bdf8", "#94a3b8")}
          
          <!-- T5 Emitter to Ground -->
          <line x1="516" y1="224" x2="516" y2="305" stroke="#94a3b8" stroke-width="2.5"/>
          {draw_ground_symbol(516, 305)}
          
          <!-- Final XOR Output Q -->
          <circle cx="516" cy="125" r="5" fill="#f8fafc" stroke="#38bdf8" stroke-width="2"/>
          <line x1="516" y1="125" x2="640" y2="125" stroke="{col_out}" stroke-width="3.5"/>
          <circle cx="640" cy="125" r="6" fill="{col_out}"/>
          <text x="655" y="130" fill="{col_out}" font-size="16" font-weight="bold">Q = {out_val}</text>
          <text x="655" y="150" fill="#94a3b8" font-size="11">{"(A ≠ B: HIGH)" if out_val else "(A = B: LOW)"}</text>
          
          <!-- Explanatory Operation Card -->
          <rect x="560" y="215" width="185" height="95" rx="8" fill="#131d2e" stroke="rgba(255,255,255,0.1)"/>
          <text x="572" y="238" fill="#cbd5e1" font-size="10" font-weight="bold">Active Path Analysis:</text>
          <text x="572" y="258" fill="{'#4ade80' if branch1_on else '#64748b'}" font-size="9.5">
            Branch 1 (A·B'): {"CONDUCTING" if branch1_on else "OFF"}
          </text>
          <text x="572" y="274" fill="{'#4ade80' if branch2_on else '#64748b'}" font-size="9.5">
            Branch 2 (A'·B): {"CONDUCTING" if branch2_on else "OFF"}
          </text>
          <text x="572" y="294" fill="{'#38bdf8' if out_val else '#94a3b8'}" font-size="9.5" font-weight="bold">
            {"→ Output Q = 1 (Odd)" if out_val else "→ Output Q = 0 (Even)"}
          </text>
        """

    return clean_svg(svg_base + svg_content + "</svg>")

