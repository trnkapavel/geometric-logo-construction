#!/usr/bin/env python3
"""Previo Blog / Magazín — three geometric concepts (circles + straight lines only).

Every curve is an arc of a recorded circle; every straight line is an axis, a
tangent or a 45° cut. Run: python3 build.py  → writes svg/*.svg
"""
from math import sqrt, asin, degrees, radians, cos, sin
from pathlib import Path

OUT = Path(__file__).parent / "svg"
OUT.mkdir(exist_ok=True)
INK = "#000"


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def pt(cx, cy, r, deg):
    return cx + r * cos(radians(deg)), cy + r * sin(radians(deg))


def svg(body, w=512, h=512, fill=INK):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<path fill="{fill}" fill-rule="evenodd" d="{body}"/></svg>\n')


def circle_sub(cx, cy, r):
    return (f"M{f(cx - r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx + r)} {f(cy)}"
            f"A{f(r)} {f(r)} 0 1 0 {f(cx - r)} {f(cy)}Z")


# ── A · „Pověšeno na dveřích“ — P that is a door hanger ─────────────────────
# Bowl = circle R. Counter (doorknob hole) = circle R/2 (1:2), concentric.
# Stem = rectangle R wide, total height 2R·φ (box 1:φ). Slit = band m wide at 45°
# from the counter out through the bowl — the cut that lets it hang on a handle.
def concept_a(R=112, cx=256, w_slit=None):
    PHI = (1 + 5 ** 0.5) / 2
    m = R / 4
    r = R / 2
    w = w_slit if w_slit is not None else m
    H = 2 * R * PHI
    top = (512 - H) / 2
    cy = top + R
    bottom = top + H
    left = cx - R
    k = m  # corner radius
    ho = degrees(asin((w / 2) / R))
    hi = degrees(asin((w / 2) / r))
    o1, o2 = pt(cx, cy, R, 45 - ho), pt(cx, cy, R, 45 + ho)
    i1, i2 = pt(cx, cy, r, 45 - hi), pt(cx, cy, r, 45 + hi)
    d = (f"M{f(left)} {f(top + k)}A{f(k)} {f(k)} 0 0 1 {f(left + k)} {f(top)}"
         f"L{f(cx)} {f(top)}"
         f"A{f(R)} {f(R)} 0 0 1 {f(o1[0])} {f(o1[1])}"
         f"L{f(i1[0])} {f(i1[1])}"
         f"A{f(r)} {f(r)} 0 1 0 {f(i2[0])} {f(i2[1])}"
         f"L{f(o2[0])} {f(o2[1])}"
         f"A{f(R)} {f(R)} 0 0 1 {f(cx)} {f(cy + R)}"
         f"L{f(cx)} {f(bottom - k)}A{f(k)} {f(k)} 0 0 1 {f(cx - k)} {f(bottom)}"
         f"L{f(left + k)} {f(bottom)}A{f(k)} {f(k)} 0 0 1 {f(left)} {f(bottom - k)}Z")
    return d, dict(R=R, m=m, r=r, cx=cx, cy=cy, top=top, bottom=bottom, w=w, H=H)


# ── B · „Klíč, který píše“ — key bow + pen-nib bit ──────────────────────────
# Bow = circle Rb, hole Rb/2 (1:2). Shaft m = Rb/2 wide. Nib = lower half of a
# vesica of two circles ρ = 2Rb (centres ρ apart → height ρ√3/2). Slit m/4 from
# the tip to a breather hole r = m/2. One key tooth m × m on the shaft.
def concept_b(Rb=80, cx=256):
    m = Rb / 2
    rho = Rb * (1 + 5 ** 0.5) / 2
    nib_h = rho * sqrt(3) / 2
    cyb = 56 + Rb
    tip = 456
    yc = tip - nib_h
    s = m / 4
    rbh = m / 2
    yb = yc + m  # breather centre one module under the shoulders
    xl, xr = cx - rho / 2, cx + rho / 2  # vesica circle centres
    yj = cyb + sqrt(Rb ** 2 - (m / 2) ** 2)
    ys = yc + sqrt(rho ** 2 - (s / 2 + rho / 2) ** 2)  # slit edge on lens
    yh = yb + sqrt(rbh ** 2 - (s / 2) ** 2)
    t1, t2 = yj + m * 0.5, yj + m * 1.5
    d = (f"M{f(cx + m / 2)} {f(yj)}"
         f"L{f(cx + m / 2)} {f(t1)}L{f(cx + m / 2 + m)} {f(t1)}L{f(cx + m / 2 + m)} {f(t2)}L{f(cx + m / 2)} {f(t2)}"
         f"L{f(cx + m / 2)} {f(yc)}L{f(xr)} {f(yc)}"
         f"A{f(rho)} {f(rho)} 0 0 1 {f(cx + s / 2)} {f(ys)}"
         f"L{f(cx + s / 2)} {f(yh)}"
         f"A{f(rbh)} {f(rbh)} 0 1 0 {f(cx - s / 2)} {f(yh)}"
         f"L{f(cx - s / 2)} {f(ys)}"
         f"A{f(rho)} {f(rho)} 0 0 1 {f(xl)} {f(yc)}"
         f"L{f(cx - m / 2)} {f(yc)}L{f(cx - m / 2)} {f(yj)}"
         f"A{f(Rb)} {f(Rb)} 0 1 1 {f(cx + m / 2)} {f(yj)}Z"
         + circle_sub(cx, cyb, Rb / 2))
    return d, dict(Rb=Rb, m=m, rho=rho, cyb=cyb, yc=yc, tip=tip)


# ── C · „Cink“ — reception bell built from lines of text ────────────────────
# Dome = semicircle R. Two horizontal cuts m/4 split it into three "lines".
# Knob = circle m/2, base = bar m high, radius m/2, overhang m/2.
def concept_c(R=160, cx=256, cy=316):
    m = R / 4
    g = m / 4
    kr = m / 2
    parts = [f"M{f(cx - R)} {f(cy)}A{f(R)} {f(R)} 0 0 1 {f(cx + R)} {f(cy)}Z",
             circle_sub(cx, cy - R - g - kr, kr)]
    bx0, bx1, by0, by1, br = cx - R - m / 2, cx + R + m / 2, cy + g, cy + g + m, m / 2
    tx = bx0 + m * 1.5  # tail: 45° triangle, legs m·1.5
    parts.append(f"M{f(bx0 + br)} {f(by0)}L{f(bx1 - br)} {f(by0)}A{f(br)} {f(br)} 0 0 1 {f(bx1 - br)} {f(by1)}"
                 f"L{f(tx + m * 1.5)} {f(by1)}L{f(tx)} {f(by1 + m * 1.5)}L{f(tx)} {f(by1)}"
                 f"L{f(bx0 + br)} {f(by1)}A{f(br)} {f(br)} 0 0 1 {f(bx0 + br)} {f(by0)}Z")
    return "".join(parts), dict(R=R, m=m)


if __name__ == "__main__":
    for name, fn in [("a", concept_a), ("b", concept_b), ("c", concept_c)]:
        d, info = fn()
        (OUT / f"concept-{name}.svg").write_text(svg(d))
        print(name, {k: round(v, 2) for k, v in info.items()})
