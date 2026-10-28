---
name: geometric-logo-construction
description: Design a logo mark from circles and straight lines only, with deliberate ratios (1:2, 1:√2, 1:φ, Fibonacci), then present it on a construction sheet with grid, construction circles, ratio labels and a concept block. Use when someone asks for a geometric, "perfect", or constructed logo or symbol, or wants to show how a mark was built. Works with any AI agent plus Figma, any vector editor, or plain SVG code.
---

# Geometric logo construction

Build a logo mark from geometric primitives instead of freehand curves, and show how it was built. The construction is part of the deliverable: anyone should be able to redraw the mark from the sheet.

## The method

### 1. Concept first
Before you draw anything, write 2–4 sentences: what the mark shows, the one idea it carries, and how it should feel. Choose **one dominant gesture**, such as a ring, a diagonal, a curl, or two eyes. Everything else supports that gesture. If you can't name it, the mark isn't ready to draw.

### 2. Modular grid
- Pick a base unit, e.g. the radius **R** of the largest circle, and a grid module (R/4, R/6 or R/8).
- Fix the bounding box, the main axis (usually the vertical symmetry axis) and the key horizontal lines.
- Aim for whole numbers of modules wherever possible.

### 3. Primitives: a few circles and straight lines
- Derive **every curve** from a few circles whose radii have deliberate ratios (see the cheat-sheet below). 3–8 circles is a healthy range.
- Use straight construction lines for tangents, axes and angles of 30°, 45° or 60°.
- Record each circle: centre, radius, and the ratio to R. If a curve isn't on any circle, it doesn't belong in the mark.

### 4. Boolean shapes
- Build the filled mark only from **unions, subtractions and intersections** of those primitives.
- Keep stroke weights and counters consistent.
- Use real vector paths only. No stock icons, icon fonts or traced clip-art.

### 5. Optical correction
Geometry that is exact can still look wrong, so correct it on purpose and **write every deviation down**. Typical corrections:
- Round shapes overshoot flat ones by 1–3 %.
- Points where two curves touch get a small gap so they don't pinch into a dot.
- Thin joins get thickened.
- Pupils, dots and other small details get nudged towards the optical centre.

### 6. Construction sheet
Present the result on one sheet (spec below): the filled mark with every construction circle and line drawn over it, ratio labels, a CONCEPT block and the clean mark in a box.

### 7. Applications
- Large size; light and dark backgrounds; one-colour version.
- Lockup with a wordmark, if there is one.
- Favicons at 64, 32 and 16 px. If details break up at 16 px, make a simplified favicon cut and say so.

### 8. Self-check
Export PNGs and actually look at them:
- Is it legible at 16 px?
- Does it read as an accidental letter, face or object it shouldn't?
- Are the weights consistent? Is the silhouette recognisable when filled black?
- Do the labels collide with the artwork?

Fix what you find and export again.

### 9. Recommend
If you made variants, write each one's rationale in one or two sentences. Mark one as recommended and give the reason.

## Ratio cheat-sheet

| Ratio | Value | Typical use |
|---|---|---|
| 1 : 2 | 0.5 | pupil in an eye, inner and outer ring, half-module details |
| 1 : √2 | 0.707 / 1.414 | the diagonal of a square; height of points, ears, peaks |
| 1 : √3 | 0.577 / 1.732 | the 30/60° triangle; vesica height (two circles of r, centres r apart) |
| 1 : φ | 0.618 / 1.618 | main secondary circles, protection zone |
| 1 : φ² | 0.382 / 2.618 | small features inside a large form, e.g. eyes in a body |
| Fibonacci | 3 : 5, 5 : 8, 8 : 13 | proportions of the bounding box, stroke-to-size |
| Angles | 30°, 45°, 60° | cuts, notches, tangents, beaks, tails |

Rules of thumb:
- Use no more than **3 different ratios** in one mark.
- The **vesica piscis** (intersection of two equal circles) makes a perfect leaf, beak, eye or flame.
- A circle tangent to two lines gives an exact rounded corner.

## Construction-sheet spec

- **Size:** 1200 × 1500 px (portrait). The drawing area is the top 1160 px; the CONCEPT block is the bottom 340 px.
- **Paper:**

  | Element | Colour |
  |---|---|
  | Background | `#F3EFE6` |
  | Grid lines | `#E6E0D4` at 0.6 px |
  | Major grid line (every 4 modules) | `#D9D2C4` at 1 px |

- **Mark:** filled with low opacity (about 15 %) so the construction stays readable on top of it. The accent colour may stay a bit stronger.
- **Construction:**
  - Circles and lines in `#7A7468`, 0.8–1.3 px.
  - Dashed lines for secondary guides (√2, φ, protection zone).
  - A centre dot of 3 px on every circle.
- **Labels:**
  - Sans-serif, 13–14 px, `#5E584D`, all placed **outside** the mark.
  - Each label has a thin accent leader line ending in a dot on the point it describes.
  - Label every circle (`r = R/φ²`), every angle (`30°`), every gap (`R/8`) and every optical correction.
- **CONCEPT block:**
  - Small caps "CONCEPT", then the title of the mark, then the 2–4 sentence concept text.
  - On the right, the clean final mark in a light box (about 330 × 280 px).
- **Optional:** a step strip of 6 panels: grid → key circles → construction lines → boolean result → optical correction → final mark.

## Copy-paste starter prompt

```
Design a geometric logo mark of [MOTIF] for [BRAND / USE].
Follow the geometric-logo-construction method:
1. Write a 2–4 sentence concept with ONE dominant gesture.
2. Set a modular grid (module = R/4) and a bounding box.
3. Build every curve from 3–8 circles with ratios from 1:2, 1:√2, 1:φ, 1:φ², Fibonacci;
   use straight lines only at 30/45/60° or as tangents. List every circle (centre, radius, ratio).
4. Make the filled mark with boolean union/subtract/intersect only, as real vector paths
   (SVG <path> or Figma vector), no icon fonts or stock icons.
5. Apply optical corrections and list each deviation with its value.
6. Produce a construction sheet (1200×1500, off-white grid paper #F3EFE6, thin grey circles
   and lines over the faint filled mark, ratio labels outside the mark with leader lines,
   CONCEPT block, clean mark in a box).
7. Produce applications: large, light and dark, favicons at 64/32/16 px.
8. Export PNGs, inspect them (16 px legibility, accidental shapes, label collisions), fix, re-export.
Colours: [PRIMARY], [ACCENT], [BACKGROUND]. Output: SVG files + PNG previews (+ Figma frames if available).
```

## Tooling notes

- **Code route:** define the primitives in a script, run the booleans with a path library (e.g. Python `skia-pathops`, Paper.js, or the Clipper library), write SVG, render PNGs (`cairosvg`, `resvg`, or a headless browser). For an animation: render one SVG frame per time step, animating `stroke-dasharray` for circles that "draw in", then join the frames with `ffmpeg`.
- **Figma route:** draw the circles as ellipses with exact sizes, use Union / Subtract / Intersect, then flatten. Keep the construction on a separate locked layer at low opacity. Or import the SVG generated by the code route.
- **Keep numbers honest:** label the values you actually used, not rounded "nice" ones. If you corrected something by eye, the label says so.
