#!/usr/bin/env python3
"""vrplayer architecture — one-glance story poster (landscape).

How a VR clip gets to your eyes: five numbered steps on one gold spine.
Under each step: 1–2 short software-dev lines (not a C4 maze).
Optional thin control (blue) and measure (green) notes stay subordinate.
Blueprint A · Unity shell + Kotlin Media3 over JNI. No AVPro.
"""

from __future__ import annotations

from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
OUT_SVG = OUT_DIR / "architecture-diagram.svg"
OUT_PNG = OUT_DIR / "architecture-diagram.png"

W, H = 1920, 1080

C = {
    "bg": "#0f1218",
    "panel": "#171c26",
    "panel_hi": "#1e2633",
    "ink": "#f0f3f8",
    "dim": "#b4bcc9",
    "muted": "#7d8798",
    "line": "#3a4456",
    "gold": "#e2a83a",
    "gold_dim": "#9a7428",
    "control": "#3aa0e8",
    "measure": "#3ccf7a",
    "warn": "#c97a3a",
    "chip": "#1a1810",
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class Svg:
    def __init__(self) -> None:
        self.parts: list[str] = []

    def a(self, s: str) -> None:
        self.parts.append(s)

    def text(
        self,
        x: float,
        y: float,
        s: str,
        size: float,
        fill: str,
        *,
        weight: int = 500,
        anchor: str = "start",
        mono: bool = False,
        ls: float | None = None,
        opacity: float = 1.0,
    ) -> None:
        fam = (
            "IBM Plex Mono, ui-monospace, Menlo, Consolas, monospace"
            if mono
            else "IBM Plex Sans, Segoe UI, Helvetica Neue, Arial, sans-serif"
        )
        lsp = f' letter-spacing="{ls}"' if ls is not None else ""
        op = f' fill-opacity="{opacity}"' if opacity != 1.0 else ""
        self.a(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{op}{lsp}>{esc(s)}</text>'
        )

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        fill: str = "none",
        stroke: str | None = None,
        sw: float = 1.5,
        rx: float = 14,
        dash: str | None = None,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
    ) -> None:
        attrs = [
            f'x="{x:.1f}"',
            f'y="{y:.1f}"',
            f'width="{w:.1f}"',
            f'height="{h:.1f}"',
            f'rx="{rx}"',
            f'fill="{fill}"',
        ]
        if fill_opacity is not None:
            attrs.append(f'fill-opacity="{fill_opacity}"')
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        if stroke_opacity is not None:
            attrs.append(f'stroke-opacity="{stroke_opacity}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity != 1.0:
            attrs.append(f'opacity="{opacity}"')
        self.a(f'<rect {" ".join(attrs)}/>')

    def circle(
        self,
        cx: float,
        cy: float,
        r: float,
        *,
        fill: str,
        stroke: str | None = None,
        sw: float = 2.0,
    ) -> None:
        attrs = [f'cx="{cx:.1f}"', f'cy="{cy:.1f}"', f'r="{r:.1f}"', f'fill="{fill}"']
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        self.a(f'<circle {" ".join(attrs)}/>')

    def path(
        self,
        d: str,
        color: str,
        width: float,
        *,
        dash: str | None = None,
        marker: str | None = None,
        opacity: float = 1.0,
        glow: bool = False,
    ) -> None:
        if glow:
            self.a(
                f'<path d="{d}" fill="none" stroke="{color}" '
                f'stroke-width="{width * 3.4:.1f}" stroke-opacity="0.18" '
                f'stroke-linecap="round" stroke-linejoin="round"/>'
            )
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#{marker})"' if marker else ""
        op = f' stroke-opacity="{opacity}"' if opacity != 1.0 else ""
        self.a(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{da}{mk}{op}/>'
        )


def step_box(
    s: Svg,
    x: float,
    y: float,
    w: float,
    h: float,
    num: int,
    title: str,
    lines: list[str],
    *,
    accent: str | None = None,
    note: str | None = None,
    note_color: str | None = None,
) -> tuple[float, float, float, float]:
    """Draw a numbered step. Returns (cx_left, cx_right, cy, center_x)."""
    stroke = accent or C["gold"]
    s.rect(x, y, w, h, fill=C["panel"], stroke=stroke, sw=2.4, rx=16)
    # number badge
    bx, by, br = x + 36, y + 42, 22
    s.circle(bx, by, br, fill=C["chip"], stroke=stroke, sw=2.2)
    s.text(bx, by + 8, str(num), 22, C["gold"], weight=700, anchor="middle")
    # title
    s.text(x + 70, y + 50, title, 26, C["ink"], weight=700)
    # engineering lines (mono, short)
    ty = y + 98
    for line in lines:
        s.text(x + 28, ty, line, 15, C["dim"], weight=500, mono=True)
        ty += 30
    if note:
        s.text(x + 28, y + h - 22, note, 13, note_color or C["warn"], weight=650, mono=True)
    return x, x + w, y + h / 2, x + w / 2


def build() -> None:
    s = Svg()
    a = s.a

    a(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"
  role="img" aria-label="How a VR clip gets to your eyes: five-step Blueprint A pipeline">
<title>How a VR clip gets to your eyes</title>
<defs>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity="0.025" stroke-width="1"/>
  </pattern>
  <marker id="mg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M0 0 10 5 0 10z" fill="{C["gold"]}"/>
  </marker>
  <marker id="mc" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M0 0 10 5 0 10z" fill="{C["control"]}"/>
  </marker>
  <marker id="mm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M0 0 10 5 0 10z" fill="{C["measure"]}"/>
  </marker>
</defs>
'''
    )
    s.rect(0, 0, W, H, fill=C["bg"], rx=0)
    a(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

    # ---- Header ----
    s.text(56, 58, "HOW A VR CLIP GETS TO YOUR EYES", 38, C["ink"], weight=700, ls=-0.4)
    s.text(
        56,
        96,
        "Blueprint A · Unity shell + Kotlin Media3 over JNI",
        20,
        C["dim"],
        weight=500,
    )
    s.rect(1480, 42, 380, 36, fill=C["chip"], stroke=C["gold_dim"], sw=1.4, rx=6, dash="4 3")
    s.text(1670, 66, "DECODE NEVER IN UNITY · NO AVPRO", 13, C["gold"], weight=700, anchor="middle", mono=True, ls=0.8)

    # ---- Five steps on one row ----
    margin_x = 48
    gap = 28
    n = 5
    usable = W - 2 * margin_x - (n - 1) * gap
    box_w = usable / n
    box_h = 280
    box_y = 200
    spine_y = box_y + box_h / 2

    # Titles unchanged; under each: ≤2 short eng lines. Notes stay thin.
    steps = [
        {
            "title": "Video arrives",
            "lines": [
                "HTTP range / local URI",
                "Sources module",
            ],
        },
        {
            "title": "Kotlin decodes",
            "lines": [
                "Media3 ExoPlayer",
                "MediaCodec HW surface",
            ],
            "note": "decode stays in Kotlin",
            "note_color": C["gold"],
        },
        {
            "title": "Cross the bridge",
            "lines": [
                "AndroidJavaProxy",
                "cmds + SurfaceTexture",
            ],
            "note": "one seam",
            "note_color": C["gold"],
        },
        {
            "title": "Unity places it",
            "lines": [
                "OpenXR layer / mesh",
                "Projection resolver pick",
            ],
            "note": "mesh path · least proven",
            "note_color": C["warn"],
        },
        {
            "title": "Eyes see it",
            "lines": [
                "Meta compositor",
                "presented frames (probe ≠ compositor)",
            ],
        },
    ]

    centers: list[tuple[float, float, float, float]] = []
    for i, st in enumerate(steps):
        x = margin_x + i * (box_w + gap)
        left, right, cy, cx = step_box(
            s,
            x,
            box_y,
            box_w,
            box_h,
            i + 1,
            st["title"],
            st["lines"],
            note=st.get("note"),
            note_color=st.get("note_color"),
        )
        centers.append((left, right, cy, cx))

    # Gold spine arrows between steps
    for i in range(n - 1):
        x0 = centers[i][1] + 4
        x1 = centers[i + 1][0] - 4
        mid = (x0 + x1) / 2
        s.path(
            f"M{x0:.1f} {spine_y:.1f} H{x1:.1f}",
            C["gold"],
            5.0,
            marker="mg",
            glow=True,
        )
        if i == 0:
            s.text(mid, spine_y - 14, "video", 12, C["gold"], weight=700, anchor="middle", mono=True)

    # ---- Thin workspace strip (how we build — not a second diagram) ----
    strip_y = box_y + box_h + 36
    s.rect(48, strip_y, W - 96, 44, fill=C["panel_hi"], stroke=C["line"], sw=1.2, rx=8)
    s.text(
        68,
        strip_y + 28,
        "WORKSPACE",
        13,
        C["muted"],
        weight=700,
        mono=True,
        ls=1.0,
    )
    s.text(
        178,
        strip_y + 28,
        "Assets/ Unity shell  ·  core/ vrplayer-core AAR (Media3)  ·  JNI bridge seam  ·  tools/ + .github CI",
        15,
        C["dim"],
        weight=500,
        mono=True,
    )

    # ---- Thin subordinate footnotes (not peers of the spine) ----
    rail_y = strip_y + 88
    s.text(56, rail_y - 22, "SIDE NOTES · not the main story", 12, C["muted"], weight=700, mono=True, ls=1.2)

    c_y = rail_y + 14
    s.circle(68, c_y, 6, fill=C["bg"], stroke=C["control"], sw=2)
    s.path(f"M82 {c_y} H118", C["control"], 2.2, marker="mc")
    s.text(130, c_y + 5, "Control", 15, C["control"], weight=700)
    s.text(
        210,
        c_y + 5,
        "controllers → Unity shell → JNI → Kotlin playback",
        15,
        C["dim"],
        weight=500,
    )

    m_y = rail_y + 48
    s.circle(68, m_y, 6, fill=C["bg"], stroke=C["measure"], sw=2)
    s.path(f"M82 {m_y} H118", C["measure"], 2.2, dash="2 5", marker="mm")
    s.text(130, m_y + 5, "Measure", 15, C["measure"], weight=700)
    s.text(
        220,
        m_y + 5,
        "QA probe → verification bench  ·  never from the compositor",
        15,
        C["dim"],
        weight=500,
    )

    # ---- Footer ----
    s.path(f"M56 {H - 56} H{W - 56}", C["line"], 1.0, opacity=0.6)
    s.text(
        56,
        H - 28,
        "One gold path · five steps · Quest 3 / Horizon OS",
        14,
        C["muted"],
        mono=True,
    )
    s.text(
        W - 56,
        H - 28,
        "file → decode → JNI → place → eyes",
        14,
        C["dim"],
        anchor="end",
        mono=True,
    )

    a("</svg>\n")
    OUT_SVG.write_text("".join(s.parts), encoding="utf-8")
    print(f"Wrote {OUT_SVG} ({OUT_SVG.stat().st_size} bytes)")

    import cairosvg

    cairosvg.svg2png(
        url=str(OUT_SVG),
        write_to=str(OUT_PNG),
        output_width=W * 2,
        output_height=H * 2,
    )
    print(f"Wrote {OUT_PNG} ({OUT_PNG.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
