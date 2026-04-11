import os

def save_svg(name, content):
    path = f"03_Branding/MultiEntregas/VECTOR_ASSETS/{name}.svg"
    with open(path, "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">\n{content}\n</svg>')
    print(f"Generated: {path}")

# --- ARCHETYPE A: THE MONOLITH (Square Grid M) ---
# A massive, solid M representing industrial scale and stability.
logo_a = """
<rect x="20" y="40" width="30" height="120" fill="black" />
<rect x="150" y="40" width="30" height="120" fill="black" />
<path d="M50 40 L100 90 L150 40 L150 70 L100 120 L50 70 Z" fill="black" />
"""

# --- ARCHETYPE B: VECTOR PATH (Dynamic Precision) ---
# Two sharp arrows forming an M, representing speed and directional cold chain.
logo_b = """
<path d="M30 160 L70 40 L100 100 L130 40 L170 160 L140 160 L120 80 L100 120 L80 80 L60 160 Z" fill="black" />
"""

# --- ARCHETYPE C: COLD CRYSTAL (Hexagonal/Ice structure) ---
# An M built from geometric prisms, suggesting thermal integrity.
logo_c = """
<path d="M40 160 L40 40 L80 40 L100 80 L120 40 L160 40 L160 160 L130 160 L130 80 L100 120 L70 80 L70 160 Z" fill="black" stroke-linejoin="bevel" />
"""

# --- ARCHETYPE D: PRECISION ARC (Minimalist Circle Cut) ---
# Minimal lines with a perfect circular intersection for high-end elegance.
logo_d = """
<path d="M40 160 V40 H160 V160 H130 V70 L100 110 L70 70 V160 Z" fill="black" />
<circle cx="100" cy="70" r="15" fill="white" />
"""

# --- ARCHETYPE E: THE FORTRESS (Solid Bridge) ---
# A heavy M that looks like a protective arch or a specialized crate.
logo_e = """
<path d="M20 160 H60 V80 L100 120 L140 80 V160 H180 V40 H140 L100 80 L60 40 H20 Z" fill="black" />
"""

# --- ARCHETYPE F: INFINITE FLUX (Single Line Purity) ---
# A masterfully simple line that flows from delivery to thermal control.
logo_f = """
<path d="M30 160 V40 L100 130 L170 40 V160" fill="none" stroke="black" stroke-width="25" stroke-linecap="square" />
"""

if __name__ == "__main__":
    os.makedirs("03_Branding/MultiEntregas/VECTOR_ASSETS", exist_ok=True)
    save_svg("A_Monolith", logo_a)
    save_svg("B_Vector", logo_b)
    save_svg("C_Crystal", logo_c)
    save_svg("D_Precision", logo_d)
    save_svg("E_Fortress", logo_e)
    save_svg("F_Flux", logo_f)
