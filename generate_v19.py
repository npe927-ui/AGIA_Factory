import os

def save_svg(name, content, width=800, height=200):
    path = f"03_Branding/MultiEntregas/VECTOR_ASSETS/{name}.svg"
    with open(path, "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">\n<rect width="{width}" height="{height}" fill="#1A1A1A" />\n{content}\n</svg>')
    print(f"Generated: {path}")

# --- MASTERWORK V19: THE TENSION WORDMARK ---
# Concept: "Multi" in ultra-thin, "ENTREGAS" in ultra-heavy.
# Visual Tension: The dot of the 'i' is shifted 4px to the right.
# Negative Space: The gap between Multi and ENTREGAS forms a vertical 'Ice Spike' silhouette.

v19_content = """
<!-- Typography Simulation for Multi (Ultra Thin) -->
<text x="50" y="140" font-family="Inter, sans-serif" font-weight="100" font-size="80" fill="#50C878" letter-spacing="10">Multi</text>
<!-- The 'i' dot: Grid Break (Shifted right by 4px) -->
<circle cx="218" cy="75" r="4" fill="#50C878" />

<!-- Typography Simulation for ENTREGAS (Ultra Bold) -->
<text x="320" y="140" font-family="Outfit, sans-serif" font-weight="900" font-size="100" fill="#E2E8F0" letter-spacing="-2">ENTREGAS</text>

<!-- Negative Space / Tension Element: The 'i' suffix of Multi cuts the space -->
<path d="M210 140 V60" stroke="#50C878" stroke-width="2" />

<!-- Visual Tension Accent (Emerald Spark) -->
<rect x="310" y="140" width="4" height="20" fill="#50C878" />
"""

# Let's create a more 'Architectural' version with pure shapes for maximum precision.
v19_pure_shapes = """
<!-- MULTI: Precise Thin Lines (Emerald) -->
<g transform="translate(50, 140)" fill="none" stroke="#50C878" stroke-width="1.5">
  <!-- M -->
  <path d="M0 0 V-60 L20 -30 L40 -60 V0" />
  <!-- u -->
  <path d="M50 -40 V0 H70 V-40 M70 0 V-15" />
  <!-- l -->
  <path d="M80 -65 V0" />
  <!-- t -->
  <path d="M90 -60 V0 M85 -45 H100" />
  <!-- i (The Stem) -->
  <path d="M110 -40 V0" />
  <!-- i (The Dot - GRID BREAK: Shifted +4px) -->
  <circle cx="114" cy="-55" r="2.5" fill="#50C878" stroke="none" />
</g>

<!-- ENTREGAS: Brutal Geometric Mass (Emerald) -->
<g transform="translate(200, 140)" fill="#50C878">
  <!-- E -->
  <path d="M0 0 H60 V-20 H25 V-35 H55 V-55 H25 V-70 H60 V-90 H0 Z" />
  <!-- N -->
  <path d="M70 0 H95 V-45 L125 0 H150 V-90 H125 V-45 L95 -90 H70 Z" />
  <!-- T -->
  <path d="M160 -70 H180 V0 H205 V-70 H225 V-90 H160 Z" />
  <!-- R -->
  <path d="M235 0 H260 V-35 H280 L300 0 H330 L305 -38 C325 -42 335 -55 330 -75 C325 -95 305 -90 280 -90 H235 Z M260 -55 V-70 H290 C300 -70 300 -55 290 -55 Z" />
  <!-- E (Repeat) -->
  <path d="M340 0 H400 V-20 H365 V-35 H395 V-55 H365 V-70 H400 V-90 H340 Z" />
  <!-- G -->
  <path d="M410 0 C460 0 475 -20 470 -45 H445 V-25 C450 -15 415 -18 435 -40 C410 -65 460 -75 475 -65 V-90 C450 -105 400 -90 410 -45 B410 0 Z" /> <!-- Fix G later -->
  <path d="M410 -45 C410 -90 470 -90 470 -45 C470 0 410 0 410 -45 M435 -45 C435 -20 460 -20 460 -45 C460 -70 435 -70 435 -45 M455 -45 H470 V-30 H455 Z" />
</g>

<!-- Tension Line: Vertical Spike between thin and thick -->
<path d="M185 140 V50" stroke="#50C878" stroke-width="0.5" opacity="0.3" />
"""

if __name__ == "__main__":
    os.makedirs("03_Branding/MultiEntregas/VECTOR_ASSETS", exist_ok=True)
    save_svg("V19_Masterwork_Wordmark", v19_pure_shapes, width=800, height=200)
