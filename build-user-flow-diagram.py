#!/usr/bin/env python3
"""vrplayer · user flow diagram (Quest wearer / Fanny journey).

Human verbs, left to right. Controllers-first (P4). H0 scope marked proposed.
Programmatic SVG → PNG. No AI image gen.
"""

from __future__ import annotations

from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
OUT_SVG = OUT_DIR / "user-flow-diagram.svg"
OUT_PNG = OUT_DIR / "user-flow-diagram.png"

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
    ) -> None:
        fam = (
            "IBM Plex Mono, ui-monospace, Menlo, Consolas, monospace"
            if mono
            else "IBM Plex Sans, Segoe UI, Helvetica Neue, Arial, sans-serif"
        )
        lsp = f' letter-spacing="{ls}"' if ls is not None else ""
        self.a(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{lsp}>{esc(s)}</text>'
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
    ) -> None:
        attrs = [
            f'x="{x:.1f}"',
            f'y="{y:.1f}"',
            f'width="{w:.1f}"',
            f'height="{h:.1f}"',
            f'rx="{rx}"',
            f'fill="{fill}"',
        ]
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
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
    ) -> None:
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
    accent: str,
    badge: str | None = None,
) -> tuple[float, float, float]:
    s.rect(x, y, w, h, fill=C["panel"], stroke=accent, sw=2.4, rx=16)
    bx, by, br = x + 36, y + 42, 22
    s.circle(bx, by, br, fill=C["chip"], stroke=accent, sw=2.2)
    s.text(bx, by + 8, str(num), 22, accent, weight=700, anchor="middle")
    s.text(x + 70, y + 50, title, 24, C["ink"], weight=700)
    ty = y + 96
    for line in lines:
        s.text(x + 24, ty, line, 15, C["dim"], weight=500, mono=True)
        ty += 28
    if badge:
        s.text(x + 24, y + h - 22, badge, 13, C["warn"], weight=650, mono=True)
    return x, x + w, y + h / 2


def build() -> None:
    s = Svg()
    a = s.a

    a(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"
  role="img" aria-label="User flow: what the Quest wearer does, five human steps">
<title>User flow · what you do</title>
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
</defs>
'''
    )
    s.rect(0, 0, W, H, fill=C["bg"], rx=0)
    a(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

    s.text(56, 58, "USER FLOW · WHAT YOU DO", 38, C["ink"], weight=700, ls=-0.4)
    s.text(
        56,
        96,
        "Quest wearer journey · right controller first (P4) · human verbs",
        20,
        C["dim"],
        weight=500,
    )
    s.rect(1420, 42, 440, 36, fill=C["chip"], stroke=C["warn"], sw=1.4, rx=6, dash="4 3")
    s.text(
        1640,
        66,
        "H0 SCOPE · PROPOSED PRODUCT UI",
        13,
        C["warn"],
        weight=700,
        anchor="middle",
        mono=True,
        ls=0.6,
    )

    # Five wearer steps
    margin_x = 48
    gap = 28
    n = 5
    usable = W - 2 * margin_x - (n - 1) * gap
    box_w = usable / n
    box_h = 300
    box_y = 180
    spine_y = box_y + box_h / 2

    steps = [
        {
            "title": "Open the app",
            "lines": [
                "Put on Quest 3",
                "Launch player / QA build",
            ],
            "accent": C["gold"],
            "badge": "H0: com.vrplayer.qa",
        },
        {
            "title": "Pick a source",
            "lines": [
                "Local file · or home",
                "Library is first surface",
            ],
            "accent": C["gold"],
            "badge": "H0: one synthetic clip",
        },
        {
            "title": "Start the clip",
            "lines": [
                "One action to play",
                "Expect picture in ~1 s",
            ],
            "accent": C["gold"],
            "badge": None,
        },
        {
            "title": "Watch & control",
            "lines": [
                "Play · pause · seek",
                "Right controller, one hand",
            ],
            "accent": C["control"],
            "badge": "P4 · product UI open",
        },
        {
            "title": "Exit or next",
            "lines": [
                "Back · dismiss · resume",
                "Leave when done",
            ],
            "accent": C["gold"],
            "badge": None,
        },
    ]

    centers: list[tuple[float, float, float]] = []
    for i, st in enumerate(steps):
        x = margin_x + i * (box_w + gap)
        left, right, cy = step_box(
            s,
            x,
            box_y,
            box_w,
            box_h,
            i + 1,
            st["title"],
            st["lines"],
            accent=st["accent"],
            badge=st["badge"],
        )
        centers.append((left, right, cy))

    for i in range(n - 1):
        x0 = centers[i][1] + 4
        x1 = centers[i + 1][0] - 4
        color = C["control"] if i == 2 else C["gold"]
        marker = "mc" if i == 2 else "mg"
        # redefine marker colors by using gold for most; control step uses blue path
        s.path(
            f"M{x0:.1f} {spine_y:.1f} H{x1:.1f}",
            color,
            5.0,
            marker=marker,
        )
        if i == 0:
            mid = (x0 + x1) / 2
            s.text(mid, spine_y - 14, "you", 12, C["gold"], weight=700, anchor="middle", mono=True)

    # Decision fork under step 2
    fork_y = box_y + box_h + 28
    s.rect(48, fork_y, W - 96, 72, fill=C["panel_hi"], stroke=C["line"], sw=1.2, rx=8)
    s.text(68, fork_y + 28, "SOURCE CHOICE", 13, C["muted"], weight=700, mono=True, ls=1.0)
    s.text(
        68,
        fork_y + 54,
        "Local URI  ·  Home server (HTTP range)  ·  H0 uses one local synthetic 8K60 clip  ·  SMB later",
        15,
        C["dim"],
        weight=500,
        mono=True,
    )

    # Footnotes
    note_y = fork_y + 110
    s.text(56, note_y, "READ IN SECONDS", 12, C["muted"], weight=700, mono=True, ls=1.2)
    s.text(
        56,
        note_y + 28,
        "This is the person. Not the stack. Controllers drive play/pause/seek when product UI ships (P4).",
        15,
        C["dim"],
        weight=500,
    )
    s.text(
        56,
        note_y + 54,
        "H0 gate: one clip plays and measures itself. Full browse / library UI is still open.",
        15,
        C["warn"],
        weight=500,
    )

    s.path(f"M56 {H - 56} H{W - 56}", C["line"], 1.0, opacity=0.6)
    s.text(
        56,
        H - 28,
        "Wearer journey · proposed · Quest 3 / Horizon OS",
        14,
        C["muted"],
        mono=True,
    )
    s.text(
        W - 56,
        H - 28,
        "open → pick → start → watch → exit",
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
