#!/usr/bin/env python3
"""Build a static ByteByteGo-style tech-stack poster (SVG→PNG) for vrplayer Blueprint A.

Designed for phone fit-to-width: 1080×2400 source so ~390 CSS px viewport still
keeps captions ≥ ~11 px and logos identifiable.
"""

from __future__ import annotations

import base64
import html
import re
from pathlib import Path

ASSETS = Path(__file__).parent / "tech-stack" / "assets"
OUT_SVG = Path(__file__).parent / "tech-stack-diagram.svg"
OUT_PNG = Path(__file__).parent / "tech-stack-diagram.png"


def read_svg(name: str) -> str:
    return (ASSETS / name).read_text(encoding="utf-8")


def data_uri(svg_text: str) -> str:
    svg_text = re.sub(r"<\?xml[^?]*\?>", "", svg_text).strip()
    b64 = base64.b64encode(svg_text.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{b64}"


def wrap_lines(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = w if not cur else f"{cur} {w}"
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]


def item_svg(
    it: dict,
    cx: float,
    cy: float,
    logos: dict[str, str],
    ink: str,
    muted: str,
    pending: str,
    *,
    compact: bool = False,
    chip_w: float | None = None,
) -> str:
    if it["kind"] == "logo":
        logo_key = it["logo"]
        wide = it.get("wide", False)
        # Phone-first mark sizes (shrink ~0.36 on 390px viewport)
        iw, ih = (110, 40) if wide else (64, 64)
        name_size = 20 if compact else 22
        name_y = cy + (ih / 2) + 24
        img_y = cy - ih / 2 - 10
        name_lines = it["name"].split("\n")
        name_ts = []
        for li, line in enumerate(name_lines):
            dy = 0 if li == 0 else name_size + 2
            name_ts.append(
                f'<tspan x="{cx:.1f}" dy="{dy}">{html.escape(line)}</tspan>'
            )
        return f'''
  <image href="{logos[logo_key]}" x="{cx - iw/2:.1f}" y="{img_y:.1f}"
    width="{iw}" height="{ih}" preserveAspectRatio="xMidYMid meet"/>
  <text x="{cx:.1f}" y="{name_y:.1f}" text-anchor="middle" fill="{ink}"
    font-size="{name_size}" font-weight="700">{"".join(name_ts)}</text>
'''

    if chip_w is None:
        chip_w = 200 if compact else 300
    chip_h = 88 if compact else 92
    x = cx - chip_w / 2
    y = cy - chip_h / 2
    name = html.escape(it["name"])
    hint = html.escape(it.get("hint", ""))
    pending_mark = ""
    if it.get("pending"):
        pending_mark = (
            f'<tspan fill="{pending}" font-size="16" font-weight="600"> · open</tspan>'
        )
    name_size = 20 if chip_w < 230 else 24
    hint_size = 17 if chip_w < 230 else 20
    return f'''
  <rect x="{x:.1f}" y="{y:.1f}" width="{chip_w}" height="{chip_h}" rx="14" ry="14"
    fill="#0e1118" stroke="#3a4150" stroke-width="1.5"/>
  <text x="{x + 12:.1f}" y="{y + 34:.1f}" fill="{ink}" font-size="{name_size}" font-weight="700">{name}{pending_mark}</text>
  <text x="{x + 12:.1f}" y="{y + 64:.1f}" fill="{muted}" font-size="{hint_size}">{hint}</text>
'''


def main() -> None:
    logos = {
        "unity": data_uri(read_svg("unity.svg")),
        "openxr": data_uri(read_svg("openxr.svg")),
        "meta": data_uri(read_svg("meta.svg")),
        "vulkan": data_uri(read_svg("vulkan.svg")),
        "kotlin": data_uri(read_svg("kotlin.svg")),
        "gha": data_uri(read_svg("githubactions.svg")),
    }

    # Taller poster so phone fit-to-width keeps type readable
    # At 390 CSS px width, source font F ≈ F * 390/1080 CSS px.
    W, H = 1080, 2680
    MARGIN_X = 36
    LEFT_W = 292
    GAP = 16
    RAIL = 52
    TRAY_X = MARGIN_X + LEFT_W + RAIL
    TRAY_W = W - TRAY_X - MARGIN_X

    BG = "#0b0c0f"
    TRAY = "#161922"
    TRAY_B = "#2a2f3a"
    INK = "#f4f5f7"
    DIM = "#c4cad6"
    MUTED = "#9aa3b2"
    PENDING = "#e8c56a"
    ACCENTS = [
        "#39ff88",
        "#3db8ff",
        "#b06bff",
        "#2ee6d6",
        "#7dff6b",
        "#4f8cff",
        "#ff6bcb",
    ]

    layers = [
        {
            "title": "Interaction / shell",
            "sub": "controller-first UI host",
            "items": [
                {"kind": "logo", "logo": "unity", "name": "Unity"},
                {"kind": "logo", "logo": "openxr", "name": "OpenXR", "wide": True},
                {"kind": "logo", "logo": "meta", "name": "Meta XR\nCore SDK"},
            ],
        },
        {
            "title": "Projection / render",
            "sub": "resolver picks direct vs mesh",
            "items": [
                {
                    "kind": "text",
                    "name": "OVROverlay",
                    "hint": "external-surface layer",
                },
                {"kind": "text", "name": "Unity URP", "hint": "render pipeline"},
                {"kind": "logo", "logo": "vulkan", "name": "Vulkan"},
                {
                    "kind": "text",
                    "name": "Equirect",
                    "hint": "direct layer · 180/360",
                },
                {
                    "kind": "text",
                    "name": "Fisheye mesh",
                    "hint": "190 / MKX200 · least proven",
                },
            ],
        },
        {
            "title": "Playback",
            "sub": "session + media clock around Media3",
            "items": [
                {
                    "kind": "text",
                    "name": "Media3 ExoPlayer",
                    "hint": "AndroidX media engine",
                },
                {
                    "kind": "text",
                    "name": "MediaCodec",
                    "hint": "hardware decode only",
                },
                {"kind": "logo", "logo": "kotlin", "name": "Kotlin"},
            ],
        },
        {
            "title": "Bridge",
            "sub": "one JNI seam",
            "items": [
                {"kind": "text", "name": "JNI", "hint": "Unity <-> Kotlin"},
                {
                    "kind": "text",
                    "name": "AndroidJavaProxy",
                    "hint": "Unity-side Java callbacks",
                },
            ],
        },
        {
            "title": "Sources",
            "sub": "local + home first · SMB later",
            "items": [
                {
                    "kind": "text",
                    "name": "Local storage",
                    "hint": "on-headset files",
                },
                {
                    "kind": "text",
                    "name": "Home server",
                    "hint": "pairing · HTTP range · prefetch",
                },
            ],
        },
        {
            "title": "Platform",
            "sub": "on-device runtime",
            "items": [
                {"kind": "text", "name": "Horizon OS", "hint": "Meta Quest OS"},
                {"kind": "logo", "logo": "meta", "name": "Quest 3"},
            ],
        },
        {
            "title": "Verify",
            "sub": "hands-off QA loop",
            "items": [
                {
                    "kind": "text",
                    "name": "QA_EVENT probe",
                    "hint": "drops only — not presented",
                },
                {
                    "kind": "text",
                    "name": "adb broker",
                    "hint": "deny-by-default wrapper",
                    "pending": True,
                },
                {"kind": "logo", "logo": "gha", "name": "GitHub Actions"},
                {
                    "kind": "text",
                    "name": "Pegasus runner",
                    "hint": "self-hosted CI",
                },
            ],
        },
    ]

    header_h = 236
    footer_h = 96
    usable = H - header_h - footer_h - 12
    row_h = int((usable - GAP * (len(layers) - 1)) / len(layers))

    parts: list[str] = []
    parts.append(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
  width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
  aria-label="vrplayer Blueprint A tech stack diagram">
<title>vrplayer · Blueprint A · Tech stack</title>
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>
  </pattern>
  <radialGradient id="glow" cx="50%" cy="0%" r="70%">
    <stop offset="0%" stop-color="#3db8ff" stop-opacity="0.10"/>
    <stop offset="55%" stop-color="#0b0c0f" stop-opacity="0"/>
  </radialGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#000" flood-opacity="0.35"/>
  </filter>
'''
    )
    for i, accent in enumerate(ACCENTS):
        parts.append(
            f'''  <pattern id="hatch-{i}" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
    <line x1="0" y1="0" x2="0" y2="8" stroke="{accent}" stroke-opacity="0.20" stroke-width="1"/>
  </pattern>
'''
        )
    parts.append(
        f'''</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#grid)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
'''
    )

    parts.append(
        f'''
<g id="header" font-family="IBM Plex Sans, Segoe UI, Helvetica Neue, Arial, sans-serif">
  <text x="{MARGIN_X}" y="58" fill="{MUTED}" font-size="22"
    font-family="IBM Plex Mono, ui-monospace, monospace"
    letter-spacing="2.6" font-weight="700">VRPLAYER · BLUEPRINT A</text>
  <rect x="{MARGIN_X + 330}" y="32" rx="10" ry="10" width="220" height="38"
    fill="rgba(232,197,106,0.12)" stroke="{PENDING}" stroke-width="1.6" stroke-dasharray="5 4"/>
  <text x="{MARGIN_X + 440}" y="57" text-anchor="middle" fill="{PENDING}" font-size="18"
    font-family="IBM Plex Mono, ui-monospace, monospace" font-weight="700">D26 pending merge</text>
  <text x="{MARGIN_X}" y="118" fill="{INK}" font-size="54" font-weight="700" letter-spacing="-1">Tech stack</text>
  <text x="{MARGIN_X}" y="166" fill="{DIM}" font-size="26">
    <tspan x="{MARGIN_X}" dy="0">Unity shell talks to Kotlin Media3 over JNI; Meta direct</tspan>
    <tspan x="{MARGIN_X}" dy="34">compositor layer for equirect 180/360; Unity mesh path for fisheye.</tspan>
  </text>
</g>
'''
    )

    y0 = header_h
    for i, layer in enumerate(layers):
        accent = ACCENTS[i]
        y = y0 + i * (row_h + GAP)

        # Left chip title + wrapped subtitle
        title = html.escape(layer["title"])
        sub_lines = wrap_lines(layer["sub"], 22)
        title_y = y + row_h / 2 - (10 if len(sub_lines) == 1 else 18)
        sub_block = []
        for li, line in enumerate(sub_lines):
            sub_block.append(
                f'<tspan x="{MARGIN_X + 18}" dy="{0 if li == 0 else 24}">{html.escape(line)}</tspan>'
            )
        sub_y = title_y + 30

        parts.append(
            f'''
<g id="row-{i}" font-family="IBM Plex Sans, Segoe UI, Helvetica Neue, Arial, sans-serif">
  <rect x="{MARGIN_X}" y="{y}" width="{LEFT_W}" height="{row_h}" rx="16" ry="16"
    fill="#12141a" stroke="{accent}" stroke-width="2.5" filter="url(#soft)"/>
  <rect x="{MARGIN_X}" y="{y}" width="{LEFT_W}" height="{row_h}" rx="16" ry="16"
    fill="{accent}" fill-opacity="0.12"/>
  <rect x="{MARGIN_X}" y="{y}" width="{LEFT_W}" height="{row_h}" rx="16" ry="16" fill="url(#hatch-{i})"/>
  <text x="{MARGIN_X + 18}" y="{title_y:.1f}" fill="{INK}" font-size="26" font-weight="700">{title}</text>
  <text x="{MARGIN_X + 18}" y="{sub_y:.1f}" fill="{MUTED}" font-size="20">{"".join(sub_block)}</text>
  <!-- stronger ByteByteGo dotted connector -->
  <line x1="{MARGIN_X + LEFT_W + 10}" y1="{y + row_h/2:.1f}" x2="{TRAY_X - 10}" y2="{y + row_h/2:.1f}"
    stroke="#9aa3b2" stroke-width="3.5" stroke-dasharray="4 9" stroke-linecap="round"/>
  <rect x="{TRAY_X}" y="{y}" width="{TRAY_W}" height="{row_h}" rx="18" ry="18"
    fill="{TRAY}" stroke="{TRAY_B}" stroke-width="1.8"/>
'''
        )

        items = layer["items"]
        n = len(items)
        pad = 14
        if n <= 3:
            cell_w = (TRAY_W - pad * 2) / n
            for j, it in enumerate(items):
                cx = TRAY_X + pad + j * cell_w + cell_w / 2
                cy = y + row_h / 2
                parts.append(
                    item_svg(
                        it,
                        cx,
                        cy,
                        logos,
                        INK,
                        MUTED,
                        PENDING,
                        compact=False,
                        chip_w=min(300, cell_w - 12),
                    )
                )
        elif n == 4:
            cell_w = (TRAY_W - pad * 2) / 2
            cell_h = (row_h - pad * 2) / 2
            for j, it in enumerate(items):
                col, row = j % 2, j // 2
                cx = TRAY_X + pad + col * cell_w + cell_w / 2
                cy = y + pad + row * cell_h + cell_h / 2
                parts.append(
                    item_svg(
                        it,
                        cx,
                        cy,
                        logos,
                        INK,
                        MUTED,
                        PENDING,
                        compact=True,
                        chip_w=min(300, cell_w - 12),
                    )
                )
        else:
            top = items[:3]
            bot = items[3:]
            cell_w_t = (TRAY_W - pad * 2) / 3
            cell_w_b = (TRAY_W - pad * 2) / 2
            cell_h = (row_h - pad * 2) / 2
            for j, it in enumerate(top):
                cx = TRAY_X + pad + j * cell_w_t + cell_w_t / 2
                cy = y + pad + cell_h / 2
                parts.append(
                    item_svg(
                        it,
                        cx,
                        cy,
                        logos,
                        INK,
                        MUTED,
                        PENDING,
                        compact=True,
                        chip_w=min(210, cell_w_t - 10),
                    )
                )
            for j, it in enumerate(bot):
                cx = TRAY_X + pad + j * cell_w_b + cell_w_b / 2
                cy = y + pad + cell_h + cell_h / 2
                parts.append(
                    item_svg(
                        it,
                        cx,
                        cy,
                        logos,
                        INK,
                        MUTED,
                        PENDING,
                        compact=True,
                        chip_w=min(300, cell_w_b - 12),
                    )
                )

        parts.append("</g>\n")

    fy = H - footer_h + 34
    parts.append(
        f'''
<g id="footer" font-family="IBM Plex Sans, Segoe UI, Helvetica Neue, Arial, sans-serif">
  <rect x="{MARGIN_X}" y="{fy - 14}" width="18" height="18" rx="3" fill="none" stroke="{PENDING}" stroke-width="2"/>
  <text x="{MARGIN_X + 30}" y="{fy + 2}" fill="{DIM}" font-size="22">D26 engine (Blueprint A) lightly pending until ONTOLOGY merge</text>
  <text x="{MARGIN_X}" y="{fy + 40}" fill="{MUTED}" font-size="20">Text chips where no distinct official product mark ships</text>
</g>
</svg>
'''
    )

    OUT_SVG.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUT_SVG} ({OUT_SVG.stat().st_size} bytes)")

    import cairosvg

    cairosvg.svg2png(
        url=str(OUT_SVG),
        write_to=str(OUT_PNG),
        output_width=W,
        output_height=H,
    )
    print(f"Wrote {OUT_PNG} ({OUT_PNG.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
