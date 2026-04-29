import os

def save_svg(name, content, size=400, height=None):
    h = height or size
    path = f"03_Branding/MultiEntregas/VECTOR_ASSETS/{name}.svg"
    with open(path, "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<svg width="{size}" height="{h}" viewBox="0 0 {size} {h}" xmlns="http://www.w3.org/2000/svg">\n{content}\n</svg>')
    print(f"Generated: {path}")

# --- LOGO V18: THE GRAVITY SPIKE ---
# An aggressive, hyper-bold silhouette. 
# It combines an 'M' with a directional spike/thermometer.
# Designed for maximum 'Magnetism'.
logo_v18 = """
<rect width="400" height="400" fill="none" />
<!-- The Spike Foundation -->
<path d="M40 340 L120 60 L200 240 L280 60 L360 340" fill="none" stroke="#00FFFF" stroke-width="60" stroke-linejoin="miter" stroke-linecap="square" />
<!-- The Internal Core (Contrast) -->
<path d="M40 340 L120 60 L200 240 L280 60 L360 340" fill="none" stroke="#000000" stroke-width="20" stroke-linejoin="miter" stroke-linecap="square" />
<!-- The Precision Tip (Electric White) -->
<circle cx="200" cy="240" r="15" fill="#FFFFFF" />
"""

# --- TRUCK WRAP PATTERN: NITROGEN FLOW ---
# A dynamic pattern of slanted lines that "wrap" around the fleet.
wrap_pattern = """
<rect width="800" height="400" fill="#050505" />
<path d="M0 400 L200 0 H250 L50 400 Z" fill="#00FFFF" opacity="0.8" />
<path d="M300 400 L500 0 H550 L350 400 Z" fill="#00FFFF" opacity="0.6" />
<path d="M600 400 L800 0 H850 L650 400 Z" fill="#00FFFF" opacity="0.4" />
"""

if __name__ == "__main__":
    os.makedirs("03_Branding/MultiEntregas/VECTOR_ASSETS", exist_ok=True)
    save_svg("V18_Gravity_Spike", logo_v18, size=400)
    save_svg("V18_Fleet_Wrap", wrap_pattern, size=800, height=400)
