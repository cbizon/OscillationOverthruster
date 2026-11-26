"""Draw L0015's pinned phase diagram (lines/L0015/pinned/phase-diagram.svg).

Every condition the nudge fast pass ran, Gamma against f*, from recorded data only:
  - evidence/E0065-results.json: the Mac loops (start 3.0, down to the floor, up
    to the wall), with the pattern amplitude A per hold from loop_analysis.py;
  - evidence/E0089-step-table.json: the Hatteras continuations above the wall
    (no amplitude computed for these steps: only counters were brought back).
Steps on the way down are drawn left of the frequency's column, steps on the
way up right of it. No pattern type (stripes, squares, hexagons) is drawn: the
fast pass recorded ring spectra only, so the type cannot be told; the colour is
the amplitude, a measure of how strongly patterned the layer is.

Usage: python3 tools/l0015_phase_diagram.py lines/L0015/pinned/phase-diagram.svg
"""
import json
import math
import sys

E65 = "evidence/E0065-results.json"
E89 = "evidence/E0089-step-table.json"
CYC = "evidence/E0089-cycle-table.json"

# Sequential blue ramp (light -> dark) for amplitude bins.
BINS = [(0.0, 0.1, "#cde2fb"), (0.1, 0.2, "#86b6ef"), (0.2, 0.4, "#3987e5"),
        (0.4, 0.8, "#1c5cab"), (0.8, 99, "#0d366b")]
INK, MUTED, GRID, STOP = "#1f1f1d", "#6b6b66", "#e4e3df", "#c0392b"

W, H = 980, 720
X0, X1, Y0, Y1 = 90, 700, 110, 650           # plot box
G_LO, G_HI = 1.65, 4.7
F_LO, F_HI = 0.25, 0.92


def gx(f):
    return X0 + (math.log(f) - math.log(F_LO)) / (math.log(F_HI) - math.log(F_LO)) * (X1 - X0)


def gy(g):
    return Y1 - (g - G_LO) / (G_HI - G_LO) * (Y1 - Y0)


def colour(a):
    for lo, hi, c in BINS:
        if lo <= a < hi:
            return c


def main(out):
    e65, e89 = json.load(open(E65)), json.load(open(E89))
    s = []
    add = s.append
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, DejaVu Sans, sans-serif">')
    add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    add(f'<text x="{X0}" y="34" font-size="20" fill="{INK}" font-weight="bold">'
        'L0015 phase diagram: nudge contact method, fast pass</text>')
    add(f'<text x="{X0}" y="58" font-size="13" fill="{MUTED}">Engine: method/nudge 16f3334. '
        'Box 100 x 100 sphere diameters, N 60000, layer depth 5.42, one seed, 25 drive cycles '
        'per Gamma step of 0.05.</text>')
    add(f'<text x="{X0}" y="78" font-size="13" fill="{MUTED}">Data: E0065 (Mac, Nov 17-20; '
        'evidence/E0065-results.json) and E0089 (Hatteras, ended Nov 24-26; '
        'evidence/E0089-step-table.json). Newest data 2026-11-26.</text>')
    # grid and axes
    g = 1.7
    while g <= G_HI + 1e-9:
        y = gy(g)
        if abs(round(g * 10) - g * 10) < 1e-6 and round(g * 10) % 5 == 0:
            add(f'<line x1="{X0}" x2="{X1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
            add(f'<text x="{X0 - 8}" y="{y + 4:.1f}" font-size="12" fill="{MUTED}" text-anchor="end">{g:.1f}</text>')
        g = round(g + 0.05, 2)
    add(f'<line x1="{X0}" x2="{X1}" y1="{Y1}" y2="{Y1}" stroke="{MUTED}"/>')
    add(f'<line x1="{X0}" x2="{X0}" y1="{Y0}" y2="{Y1}" stroke="{MUTED}"/>')
    add(f'<text x="30" y="{(Y0 + Y1) / 2}" font-size="14" fill="{INK}" text-anchor="middle" '
        f'transform="rotate(-90 30 {(Y0 + Y1) / 2})">Gamma (peak plate acceleration / g)</text>')
    add(f'<text x="{(X0 + X1) / 2}" y="{Y1 + 44}" font-size="14" fill="{INK}" text-anchor="middle">'
        'f* (dimensionless drive frequency, log scale)</text>')

    dx = 7  # half-offset: down branch left, up branch right
    r = 3.6
    for loop in e65["loops"]:
        f = loop["f_star"]
        x = gx(f)
        add(f'<text x="{x:.1f}" y="{Y1 + 20}" font-size="12" fill="{MUTED}" text-anchor="middle">{f:.2f}</text>')
        last_up = {}
        for st in loop["steps"]:
            side = -dx if st["direction"] == "down" else dx
            y = gy(st["gamma"])
            tip = f'f* {f}, Gamma {st["gamma"]}, {st["direction"] or "start"}, {st["outcome"]}'
            if st["outcome"] == "completed" and st.get("A") is not None:
                add(f'<circle cx="{x + side:.1f}" cy="{y:.1f}" r="{r}" fill="{colour(st["A"])}" '
                    f'stroke="#ffffff" stroke-width="1"><title>{tip}, A {st["A"]}</title></circle>')
            elif st["outcome"] != "completed":
                add(cross(x + side, y, tip + " (Mac step cap)"))
            if st["direction"] == "up":
                last_up[st["gamma"]] = st
        # E0089 continuation steps on Hatteras (up branch)
        for lp in e89["loops"]:
            if abs(lp["f_star"] - f) > 1e-9:
                continue
            for row in lp["rows"]:
                if row["host"] != "hatteras":
                    continue
                y = gy(row["gamma"])
                tip = f'f* {f}, Gamma {row["gamma"]}, up, E0089 {row["outcome"]}, {row["cycles"]} of 25 cycles'
                if row["outcome"] == "completed":
                    add(f'<circle cx="{x + dx:.1f}" cy="{y:.1f}" r="{r}" fill="#ffffff" stroke="{INK}" '
                        f'stroke-width="1.2"><title>{tip}; amplitude not computed</title></circle>')
                else:
                    add(cross(x + dx, y, tip + " (48 CPU-hour step cap)", big=True))
        if f in (0.27,):
            add(f'<text x="{x:.1f}" y="{gy(3.0) - 12:.1f}" font-size="10" fill="{MUTED}" '
                'text-anchor="middle">first step</text>')
            add(f'<text x="{x:.1f}" y="{gy(3.0) - 1:.1f}" font-size="10" fill="{MUTED}" '
                'text-anchor="middle">not finished</text>')
        if f in (0.3,):
            add(f'<text x="{x + 12:.1f}" y="{gy(4.3) - 10:.1f}" font-size="10" fill="{MUTED}" '
                'text-anchor="middle">record ends</text>')

    # legend
    lx, ly = 730, 130
    add(f'<text x="{lx}" y="{ly}" font-size="13" fill="{INK}" font-weight="bold">Pattern amplitude A</text>')
    add(f'<text x="{lx}" y="{ly + 16}" font-size="11" fill="{MUTED}">(band amplitude of the height field,</text>')
    add(f'<text x="{lx}" y="{ly + 30}" font-size="11" fill="{MUTED}">wavelengths L/3 and shorter, sphere</text>')
    add(f'<text x="{lx}" y="{ly + 44}" font-size="11" fill="{MUTED}">diameters; larger = more patterned)</text>')
    for i, (lo, hi, c) in enumerate(BINS):
        y = ly + 66 + i * 22
        lab = f"{lo:g} to {hi:g}" if hi < 99 else f"{lo:g} and above"
        add(f'<circle cx="{lx + 8}" cy="{y - 4}" r="6" fill="{c}"/>')
        add(f'<text x="{lx + 22}" y="{y}" font-size="12" fill="{INK}">{lab}</text>')
    y = ly + 66 + len(BINS) * 22 + 10
    add(f'<circle cx="{lx + 8}" cy="{y - 4}" r="5" fill="#ffffff" stroke="{INK}" stroke-width="1.2"/>')
    add(f'<text x="{lx + 22}" y="{y}" font-size="12" fill="{INK}">ran all 25 cycles on Hatteras;</text>')
    add(f'<text x="{lx + 22}" y="{y + 14}" font-size="12" fill="{INK}">amplitude not computed</text>')
    y += 40
    add(cross(lx + 8, y - 4, "legend", big=True))
    add(f'<text x="{lx + 22}" y="{y}" font-size="12" fill="{INK}">step stopped by its CPU cap</text>')
    add(f'<text x="{lx + 22}" y="{y + 14}" font-size="12" fill="{INK}">(large: 48 CPU-hours, Hatteras;</text>')
    add(f'<text x="{lx + 22}" y="{y + 28}" font-size="12" fill="{INK}">small: 0.5-4 CPU-hours, Mac)</text>')
    y += 58
    for t in ["In each column, the left marks are",
              "the way down from Gamma 3.0, the",
              "right marks the way back up.",
              "",
              "No loop got above Gamma 4.6: the",
              "cost per cycle rises several times",
              "with each 0.05 step above 4.5; the layer",
              "alternating a cheap and an expensive",
              "cycle (period doubling).",
              "",
              "Pattern type (stripes, squares,",
              "hexagons) is not shown: the pass",
              "kept ring spectra only.",
              "",
              "f* 0.30: the E0065 record ends at",
              "Gamma 4.3 on the way up; it was not",
              "continued in E0089."]:
        add(f'<text x="{lx}" y="{y}" font-size="11.5" fill="{MUTED}">{t}</text>')
        y += 15
    add("</svg>")
    open(out, "w").write("\n".join(s) + "\n")


def cross(x, y, tip, big=False):
    h = 5.5 if big else 3.5
    w = 2.4 if big else 1.6
    return (f'<g stroke="{STOP}" stroke-width="{w}" stroke-linecap="round"><title>{tip}</title>'
            f'<line x1="{x - h:.1f}" y1="{y - h:.1f}" x2="{x + h:.1f}" y2="{y + h:.1f}"/>'
            f'<line x1="{x - h:.1f}" y1="{y + h:.1f}" x2="{x + h:.1f}" y2="{y - h:.1f}"/></g>')


if __name__ == "__main__":
    main(sys.argv[1])
