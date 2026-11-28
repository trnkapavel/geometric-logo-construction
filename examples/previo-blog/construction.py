#!/usr/bin/env python3
"""Construction sheet (1200×1500) + applications sheet for concept A."""
from math import sqrt, cos, sin, radians
from pathlib import Path
import re
from build import concept_a, f

OUT = Path(__file__).parent / "svg"
RED = "#B50000"
LINE = "#7A7468"
LABEL = "#5E584D"
FONT_R = "file:///Users/paveltrnka/.claude/skills/previo-brand/fonts/Inter-Regular.ttf"
FONT_M = "file:///Users/paveltrnka/.claude/skills/previo-brand/fonts/Inter-Medium.ttf"
STYLE = (f"<style>@font-face{{font-family:IR;src:url({FONT_R})}}@font-face{{font-family:IM;src:url({FONT_M})}}"
         ".l{font-family:IR,Inter,sans-serif;font-size:14px;fill:%s}"
         ".h{font-family:IM,Inter,sans-serif}</style>" % LABEL)
PHI = (1 + 5 ** 0.5) / 2

d, k = concept_a()
R, m, r, cx, cy, top, bottom, w = (k[n] for n in ("R", "m", "r", "cx", "cy", "top", "bottom", "w"))
S = 2.0  # mark units → sheet px
OX, OY = 600 - cx * S, 580 - 256 * S


def X(x): return OX + x * S
def Y(y): return OY + y * S


def circ(x, y, rad, dash=False, w_=1):
    da = ' stroke-dasharray="5 5"' if dash else ""
    return (f'<circle cx="{f(X(x))}" cy="{f(Y(y))}" r="{f(rad * S)}" fill="none" stroke="{LINE}" stroke-width="{w_}"{da}/>'
            f'<circle cx="{f(X(x))}" cy="{f(Y(y))}" r="3" fill="{LINE}"/>')


def line(x1, y1, x2, y2, dash=False, w_=0.9):
    da = ' stroke-dasharray="5 5"' if dash else ""
    return f'<line x1="{f(X(x1))}" y1="{f(Y(y1))}" x2="{f(X(x2))}" y2="{f(Y(y2))}" stroke="{LINE}" stroke-width="{w_}"{da}/>'


def label(px, py, tx, ty, text, anchor="start"):
    """px,py in mark units (target); tx,ty sheet px (text position)."""
    lx = tx - 14 if anchor == "start" else tx + 14
    lines = text.split("\n")
    t = "".join(f'<tspan x="{f(tx)}" dy="{0 if i == 0 else 20}">{s}</tspan>' for i, s in enumerate(lines))
    return (f'<line x1="{f(X(px))}" y1="{f(Y(py))}" x2="{f(lx)}" y2="{f(ty - 5)}" stroke="{RED}" stroke-width="0.9"/>'
            f'<circle cx="{f(X(px))}" cy="{f(Y(py))}" r="3.5" fill="{RED}"/>'
            f'<text class="l" x="{f(tx)}" y="{f(ty)}" text-anchor="{anchor}">{t}</text>')


def on(rad, deg):
    return cx + rad * cos(radians(deg)), cy + rad * sin(radians(deg))


def construction_sheet():
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1500" width="1200" height="1500">{STYLE}',
         '<rect width="1200" height="1500" fill="#F3EFE6"/>']
    # grid: module m, aligned to the mark's left edge; major every 4 m (= R)
    step = m * S
    x0 = X(cx - R)
    i = -20
    while True:
        gx = x0 + i * step
        if gx > 1200: break
        if gx >= 0:
            maj = i % 4 == 0
            o.append(f'<line x1="{f(gx)}" y1="0" x2="{f(gx)}" y2="1160" stroke="{"#D9D2C4" if maj else "#E6E0D4"}" stroke-width="{1 if maj else 0.6}"/>')
        i += 1
    y0 = Y(top)
    i = -20
    while True:
        gy = y0 + i * step
        if gy > 1160: break
        if gy >= 0:
            maj = i % 4 == 0
            o.append(f'<line x1="0" y1="{f(gy)}" x2="1200" y2="{f(gy)}" stroke="{"#D9D2C4" if maj else "#E6E0D4"}" stroke-width="{1 if maj else 0.6}"/>')
        i += 1
    o.append('<rect y="1160" width="1200" height="340" fill="#EBE6DA"/><line x1="0" y1="1160" x2="1200" y2="1160" stroke="#D9D2C4"/>')
    # faint filled mark
    o.append(f'<path transform="translate({f(OX)} {f(OY)}) scale({S})" d="{d}" fill="{RED}" fill-opacity="0.14" fill-rule="evenodd" stroke="{RED}" stroke-opacity="0.5" stroke-width="{0.6 / S}"/>')
    # construction
    o.append(line(cx, top - 2 * m, cx, bottom + 2 * m, dash=True))  # axis
    o.append(line(cx - R - 2 * m, cy, cx + R + 2 * m, cy))
    o.append(line(cx - R, top - 2 * m, cx - R, bottom + 2 * m))
    o.append(line(cx - R - 2 * m, top, cx + R + 2 * m, top))
    o.append(line(cx - R - 2 * m, bottom, cx + R + 2 * m, bottom))
    o.append(line(cx + R, top - m, cx + R, bottom + m, dash=True))  # box 2R × 2Rφ
    o.append(line(cx - R - 2 * m, cy + R, cx + R + 2 * m, cy + R, dash=True))
    # 45° slit lines (and their centre line)
    n = (-(w / 2) / sqrt(2), (w / 2) / sqrt(2))
    for sgn in (-1, 1):
        a = (cx + sgn * n[0] - 0.5 * R, cy + sgn * n[1] - 0.5 * R)
        b = (cx + sgn * n[0] + 1.35 * R, cy + sgn * n[1] + 1.35 * R)
        o.append(line(*a, *b))
    o.append(line(cx - R, cy - R, cx + 1.5 * R, cy + 1.5 * R, dash=True, w_=0.7))
    o.append(circ(cx, cy, R, w_=1.2))
    o.append(circ(cx, cy, r, w_=1.2))
    o.append(circ(cx, cy, R * PHI, dash=True, w_=0.8))  # protection zone
    for (ccx, ccy) in ((cx - R + m, top + m), (cx - R + m, bottom - m), (cx - m, bottom - m)):
        o.append(circ(ccx, ccy, m, w_=0.9))
    # labels (all outside the mark)
    px, py = on(R, -40)
    o.append(label(px, py, 905, 300, "mísa P: kružnice R"))
    px, py = on(R * PHI, -120)
    o.append(label(px, py, 300, 150, "ochranná zóna φR", anchor="end"))
    px, py = on(r, 200)
    o.append(label(px, py, 300, 420, "otvor na kliku: r = R/2  (1 : 2)", anchor="end"))
    px, py = cx + 1.2 * R, cy + 1.2 * R
    o.append(label(px, py, 905, 640, "zářez 45°, šířka m = R/4\n(visačka se nasadí na kliku)"))
    o.append(label(cx, cy + R, 905, 760, "vnitřní roh P: tečna x = střed mísy"))
    o.append(label(cx + R, cy + R * 1.9, 905, 880, "rámeček 2R × 2Rφ  (1 : φ)"))
    o.append(label(cx - R + m - m / sqrt(2), bottom - m + m / sqrt(2), 300, 940, "rohy: kružnice m", anchor="end"))
    o.append(label(cx - R, cy + R * 0.9, 300, 700, "dřík: šířka R = 4 m", anchor="end"))
    o.append(f'<text class="l" x="60" y="1110">modul m = R/4 · rámeček 8 m × 12,94 m · 6 kružnic, 7 přímek</text>')
    o.append('<text class="h" x="600" y="48" text-anchor="middle" font-size="20" fill="#202124">Previo Magazín · konstrukce značky</text>')
    o.append('<text class="l" x="1140" y="48" text-anchor="end">Previo · 2026</text>')
    # concept block
    o.append('<text class="l" x="60" y="1212" letter-spacing="2" font-size="13">KONCEPT</text>')
    o.append('<text class="h" x="60" y="1252" font-size="28" fill="#202124">P, které visí na klice</text>')
    body = ["Visačka na kliku je v logu Previo odjakživa – je to červené i.",
            "Magazín z ní dělá vlastní značku: písmeno P, jehož mísa je otvor",
            "na kliku a zářez pod 45° ho nechá pověsit na dveře. Uvnitř se",
            "navíc skrývá lupa – blog, který pro hoteliéry hledá a vysvětluje.",
            "Jeden symbol pro všechny země, jazyk nese jen slovo vedle něj."]
    for i, t in enumerate(body):
        o.append(f'<text class="l" x="60" y="{1296 + i * 25}" font-size="15">{t}</text>')
    o.append('<rect x="820" y="1190" width="330" height="280" fill="#FAF8F3" stroke="#D9D2C4"/>')
    sc = 230 / 362.44
    o.append(f'<path transform="translate({f(985 - cx * sc)} {f(1330 - 256 * sc)}) scale({f(sc)})" d="{d}" fill="{RED}" fill-rule="evenodd"/>')
    o.append("</svg>")
    return "".join(o)


def applications_sheet():
    logo = Path('/Users/paveltrnka/.claude/skills/previo-brand/logo/previo-logo-color.svg').read_text()
    logo_w = Path('/Users/paveltrnka/.claude/skills/previo-brand/logo/previo-logo-white.svg').read_text()
    inner = re.search(r'<svg[^>]*>(.*)</svg>', logo, re.S).group(1)
    inner_w = re.search(r'<svg[^>]*>(.*)</svg>', logo_w, re.S).group(1)
    small, _ = concept_a(w_slit=m * 1.5)  # 16–32 px cut: wider slit

    def mark(x, y, h, fill, path=d):
        sc = h / 362.44
        return f'<path transform="translate({f(x - (cx - R) * sc)} {f(y - top * sc)}) scale({f(sc)})" d="{path}" fill="{fill}" fill-rule="evenodd"/>'

    def lockup(x, y, word, dark=False):
        ink = "#fff" if dark else "#202124"
        return (mark(x, y, 104, RED if not dark else "#fff")
                + f'<g transform="translate({x + 92} {y + 18}) scale(1.25)">{inner_w if dark else inner}</g>'
                + f'<rect x="{x + 232}" y="{y + 30}" width="2" height="48" fill="{ink}" opacity=".5"/>'
                + f'<text class="h" x="{x + 248}" y="{y + 72}" font-size="40" letter-spacing="-1" fill="{ink}">{word}</text>')

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1300" width="1200" height="1300">{STYLE}',
         '<rect width="1200" height="1300" fill="#F3EFE6"/>',
         '<text class="h" x="60" y="70" font-size="28" fill="#202124">Jeden symbol, každá země</text>',
         '<text class="l" x="60" y="100" font-size="15">„Magazín“ zní ve všech jazycích skoro stejně – mění se jen slovo, značka zůstává.</text>']
    countries = [("CZ", "magazín"), ("SK", "magazín"), ("PL", "magazyn"), ("HU", "magazin"), ("DE · AT", "Magazin"), ("EN", "magazine")]
    for i, (cc, word) in enumerate(countries):
        col, row = i % 2, i // 2
        x, y = 60 + col * 560, 140 + row * 170
        o.append(f'<rect x="{x}" y="{y}" width="520" height="150" rx="14" fill="#FAF8F3" stroke="#E0D9CB"/>')
        o.append(f'<text class="l" x="{x + 24}" y="{y + 30}" letter-spacing="1.5" font-size="12">{cc}</text>')
        o.append(lockup(x + 40, y + 34, word))
    # dark + red applications
    y = 680
    o.append(f'<rect x="60" y="{y}" width="520" height="300" rx="14" fill="#202124"/>')
    o.append(lockup(100, y + 100, "magazín", dark=True))
    o.append(f'<rect x="620" y="{y}" width="520" height="300" rx="14" fill="{RED}"/>')
    o.append(mark(820, y + 60, 180, "#fff"))
    # favicons / app icon
    y = 1030
    o.append(f'<text class="h" x="60" y="{y}" font-size="20" fill="#202124">Malé velikosti</text>')
    o.append(f'<text class="l" x="60" y="{y + 26}">Pod 32 px se používá řez se zářezem 1,5 m (optická korekce, aby se neslil).</text>')
    xs = 60
    for sz in (128, 64, 32, 16):
        o.append(f'<rect x="{xs}" y="{y + 60}" width="{sz}" height="{sz}" rx="{sz * 0.22}" fill="{RED}"/>')
        o.append(mark(xs + sz * 0.5 - sz * 0.62 * (2 * R) / 362.44 / 2, y + 60 + sz * 0.19, sz * 0.62, "#fff", small if sz <= 32 else d))
        o.append(f'<text class="l" x="{xs}" y="{y + 220}">{sz} px</text>')
        xs += sz + 40
    # browser-tab mock
    o.append(f'<rect x="560" y="{y + 60}" width="580" height="56" rx="10" fill="#FAF8F3" stroke="#E0D9CB"/>')
    o.append(mark(580, y + 80, 16, RED, small))
    o.append(f'<text class="l" x="606" y="{y + 93}" fill="#202124">Jak zvednout ADR mimo sezónu · Previo Magazín</text>')
    o.append(f'<rect x="560" y="{y + 136}" width="580" height="56" rx="10" fill="#202124"/>')
    o.append(mark(580, y + 156, 16, "#fff", small))
    o.append(f'<text class="l" x="606" y="{y + 169}" style="fill:#e8e6e1">Jak zvednout ADR mimo sezónu · Previo Magazín</text>')
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    (OUT / "construction_sheet.svg").write_text(construction_sheet())
    (OUT / "applications.svg").write_text(applications_sheet())
    small, _ = concept_a(w_slit=m * 1.5)
    from build import svg
    (OUT / "mark-red.svg").write_text(svg(d, fill=RED))
    (OUT / "mark-small.svg").write_text(svg(small, fill=RED))
    print("ok")
