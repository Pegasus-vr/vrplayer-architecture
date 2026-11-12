#!/usr/bin/env python3
"""vrplayer C4-style container / deployment poster (landscape).

Runtime truth only: who owns decode, who owns the surface, what crosses JNI,
what the compositor sees, what is off-headset. Blueprint A / D26 lightly.
No logo trays, no site chrome, no marketing.
"""

from __future__ import annotations

from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
OUT_SVG = OUT_DIR / "architecture-diagram.svg"
OUT_PNG = OUT_DIR / "architecture-diagram.png"

W, H = 1920, 1180

C = {
    "bg": "#0f1218",
    "panel": "#161b24",
    "panel2": "#1b2230",
    "ink": "#e8edf5",
    "dim": "#a8b0bf",
    "muted": "#7d8798",
    "line": "#3a4456",
    "bound": "#c9d0dc",
    "app": "#d7c4a3",
    "video": "#e2a83a",
    "control": "#3aa0e8",
    "measure": "#3ccf7a",
    "pending": "#c9a227",
    "warn": "#c97a3a",
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
        rx: float = 8,
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
                f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width * 3.2:.1f}" '
                f'stroke-opacity="0.16" stroke-linecap="round" stroke-linejoin="round"/>'
            )
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#{marker})"' if marker else ""
        op = f' stroke-opacity="{opacity}"' if opacity != 1.0 else ""
        self.a(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{da}{mk}{op}/>'
        )

    def label_tag(
        self,
        x: float,
        y: float,
        s: str,
        *,
        fill_bg: str,
        ink: str,
        w: float | None = None,
    ) -> None:
        tw = w if w is not None else max(72.0, 11.0 * len(s) + 28)
        self.rect(x, y, tw, 26, fill=fill_bg, stroke=C["bound"], sw=1.2, rx=4, stroke_opacity=0.45)
        self.text(x + tw / 2, y + 17.5, s, 12, ink, weight=700, anchor="middle", mono=True, ls=1.6)

    def box(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        title: str,
        sub: str,
        *,
        owns: str | None = None,
        stroke: str | None = None,
        fill: str | None = None,
        title_size: float = 20,
    ) -> None:
        self.rect(
            x,
            y,
            w,
            h,
            fill=fill or C["panel2"],
            stroke=stroke or C["line"],
            sw=1.6,
            rx=6,
        )
        self.text(x + 16, y + 28, title, title_size, C["ink"], weight=700)
        self.text(x + 16, y + 50, sub, 14, C["dim"], weight=500)
        if owns:
            self.text(x + 16, y + h - 16, owns, 13, C["muted"], weight=500, mono=True)


def build() -> None:
    s = Svg()
    a = s.a

    a(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"
  role="img" aria-label="vrplayer architecture Blueprint A C4 container diagram">
<title>vrplayer architecture</title>
<defs>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity="0.028" stroke-width="1"/>
  </pattern>
  <marker id="mv" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M0 0 10 5 0 10z" fill="{C["video"]}"/>
  </marker>
  <marker id="mc" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M0 0 10 5 0 10z" fill="{C["control"]}"/>
  </marker>
  <marker id="mm" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M0 0 10 5 0 10z" fill="{C["measure"]}"/>
  </marker>
</defs>
'''
    )
    s.rect(0, 0, W, H, fill=C["bg"], rx=0)
    a(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

    # ---- Header (sparse) ----
    s.text(48, 42, "C4 · CONTAINER / DEPLOYMENT", 13, C["muted"], weight=700, mono=True, ls=2.2)
    s.rect(1580, 22, 292, 28, fill="#1a1810", stroke=C["pending"], sw=1.3, rx=4, dash="4 3")
    s.text(1726, 41, "D26 PENDING · NO AVPRO", 12, C["pending"], weight=700, anchor="middle", mono=True, ls=1.2)
    s.text(48, 88, "vrplayer architecture", 42, C["ink"], weight=700)
    s.text(
        48,
        118,
        "Proposed Blueprint A · Unity shell + Kotlin Media3 over JNI · one Quest 3 app process",
        17,
        C["dim"],
    )

    # ---- Legend (top right under chip) ----
    lx, ly = 1280, 78
    for i, (col, name, hint, dash, ww) in enumerate(
        [
            (C["video"], "Video frames", "file → decode → eyes", None, 3.5),
            (C["control"], "Control", "controller → core", None, 2.8),
            (C["measure"], "Measure / QA", "probe → bench", "2 6", 2.4),
        ]
    ):
        yy = ly + i * 22
        s.path(f"M{lx} {yy}h36", col, ww, dash=dash)
        s.text(lx + 48, yy + 4, name, 13, C["ink"], weight=650)
        s.text(lx + 158, yy + 4, hint, 12, C["muted"], mono=True)

    # ============================================================
    # OFF-HEADSET (left)
    # ============================================================
    ox, oy, ow, oh = 48, 160, 300, 860
    s.rect(ox, oy, ow, oh, fill=C["panel"], stroke=C["bound"], sw=1.8, rx=8, dash="7 5", stroke_opacity=0.55)
    s.label_tag(ox + 16, oy - 13, "OFF-HEADSET", fill_bg=C["bg"], ink=C["ink"], w=140)

    s.box(
        ox + 20,
        oy + 36,
        ow - 40,
        150,
        "Home server",
        "pairing · HTTP range · prefetch",
        owns="enters over Wi-Fi",
    )
    s.box(
        ox + 20,
        oy + 220,
        ow - 40,
        150,
        "Verification",
        "bench · one QA_EVENT stream",
        owns="D14 · C10 · off device",
    )
    s.text(ox + 20, oy + 420, "Not on the headset.", 14, C["muted"])
    s.text(ox + 20, oy + 442, "Files and probes cross", 14, C["muted"])
    s.text(ox + 20, oy + 464, "the trust boundary.", 14, C["muted"])

    # ============================================================
    # QUEST 3 envelope
    # ============================================================
    qx, qy, qw, qh = 380, 160, 1492, 860
    s.rect(qx, qy, qw, qh, fill=C["panel"], stroke=C["bound"], sw=3.2, rx=10)
    s.label_tag(qx + 20, qy - 13, "QUEST 3  ·  HORIZON OS", fill_bg=C["bg"], ink=C["ink"], w=250)
    s.text(qx + qw - 24, qy + 28, "one device · one trust domain", 13, C["muted"], anchor="end", mono=True)

    # ---- ONE APP PROCESS ----
    ax, ay, aw, ah = qx + 28, qy + 48, qw - 56, 520
    s.rect(ax, ay, aw, ah, fill="#121722", stroke=C["app"], sw=2.4, rx=8)
    s.label_tag(ax + 16, ay - 13, "ONE APP PROCESS", fill_bg="#121722", ink=C["app"], w=180)
    s.text(ax + aw - 20, ay + 24, "Unity | JNI | Kotlin", 13, C["muted"], anchor="end", mono=True)

    # Three containers inside app
    gap = 20
    col_w = (aw - 48 - 2 * gap) / 3
    cy0 = ay + 48
    ch = 360

    # UNITY
    ux = ax + 24
    s.box(
        ux,
        cy0,
        col_w,
        ch,
        "Unity shell",
        "OpenXR · Meta XR · Vulkan",
        owns="owns interaction + mesh surface",
        stroke="#4a5568",
        fill="#182030",
        title_size=22,
    )
    # internal responsibilities
    s.rect(ux + 14, cy0 + 70, col_w - 28, 64, fill="#121722", stroke=C["line"], sw=1.2, rx=4)
    s.text(ux + 28, cy0 + 96, "Interaction", 15, C["ink"], weight=650)
    s.text(ux + 28, cy0 + 116, "controller-first · P4", 12, C["muted"], mono=True)

    s.rect(ux + 14, cy0 + 146, col_w - 28, 64, fill="#121722", stroke="#8b6bb5", sw=1.4, rx=4)
    s.text(ux + 28, cy0 + 172, "Lens mesh", 15, C["ink"], weight=650)
    s.text(ux + 28, cy0 + 192, "fisheye · least proven handoff", 12, C["warn"], mono=True)

    s.rect(ux + 14, cy0 + 222, col_w - 28, 64, fill="#121722", stroke=C["line"], sw=1.2, rx=4)
    s.text(ux + 28, cy0 + 248, "Library UI", 15, C["ink"], weight=650)
    s.text(ux + 28, cy0 + 268, "browse · start playback", 12, C["muted"], mono=True)

    s.text(ux + 14, cy0 + 320, "Meta XR Core SDK on shell", 12, C["muted"], mono=True)
    s.text(ux + 14, cy0 + 340, "(OpenXR / OVR constraint open)", 12, C["muted"], mono=True)

    # JNI BRIDGE
    bx = ux + col_w + gap
    s.rect(bx, cy0, col_w, ch, fill="#1a1524", stroke="#8b6bb5", sw=2.0, rx=6)
    s.text(bx + 16, cy0 + 28, "JNI bridge", 22, C["ink"], weight=700)
    s.text(bx + 16, cy0 + 50, "one seam · Unity ↔ Kotlin", 14, C["dim"])

    # vertical contract strip
    s.rect(bx + 40, cy0 + 90, col_w - 80, 200, fill="#121722", stroke="#8b6bb5", sw=1.6, rx=4, dash="5 4")
    s.text(bx + col_w / 2, cy0 + 140, "CONTRACT", 12, C["muted"], weight=700, anchor="middle", mono=True, ls=2.0)
    s.text(bx + col_w / 2, cy0 + 175, "control cmds", 16, C["ink"], weight=650, anchor="middle")
    s.text(bx + col_w / 2, cy0 + 200, "surface handles", 16, C["ink"], weight=650, anchor="middle")
    s.text(bx + col_w / 2, cy0 + 225, "callbacks / epoch", 16, C["ink"], weight=650, anchor="middle")
    s.text(bx + col_w / 2, cy0 + 260, "AndroidJavaProxy", 13, C["muted"], anchor="middle", mono=True)
    s.text(bx + 16, cy0 + ch - 16, "owns the only cross-runtime port", 13, C["muted"], mono=True)

    # KOTLIN
    kx = bx + col_w + gap
    s.box(
        kx,
        cy0,
        col_w,
        ch,
        "Kotlin Media3 core",
        "ExoPlayer · HW decode only",
        owns="owns decode · session · cadence",
        stroke="#3a5a78",
        fill="#152030",
        title_size=22,
    )
    s.rect(kx + 14, cy0 + 70, col_w - 28, 64, fill="#121722", stroke=C["line"], sw=1.2, rx=4)
    s.text(kx + 28, cy0 + 96, "Sources", 15, C["ink"], weight=650)
    s.text(kx + 28, cy0 + 116, "local storage + home first", 12, C["muted"], mono=True)

    s.rect(kx + 14, cy0 + 146, col_w - 28, 64, fill="#121722", stroke=C["line"], sw=1.2, rx=4)
    s.text(kx + 28, cy0 + 172, "Playback core", 15, C["ink"], weight=650)
    s.text(kx + 28, cy0 + 192, "session · audio master · reopen", 12, C["muted"], mono=True)

    s.rect(kx + 14, cy0 + 222, col_w - 28, 64, fill="#121722", stroke="#8b6bb5", sw=1.4, rx=4)
    s.text(kx + 28, cy0 + 248, "Projection resolver", 15, C["ink"], weight=650)
    s.text(kx + 28, cy0 + 268, "before decode · direct vs mesh", 12, C["muted"], mono=True)

    s.text(kx + 14, cy0 + 320, "MediaCodec configured here;", 12, C["muted"], mono=True)
    s.text(kx + 14, cy0 + 340, "HW decoder runs in Horizon OS", 12, C["muted"], mono=True)

    # App foot note
    s.text(
        ax + 24,
        ay + ah - 18,
        "No AVPro. Decode never lives in Unity. Frames leave Kotlin as a leased surface / buffer.",
        13,
        C["muted"],
    )

    # ---- HORIZON OS PLATFORM band ----
    hx, hy, hw, hh = ax, ay + ah + 36, aw, 200
    s.rect(hx, hy, hw, hh, fill="#141920", stroke=C["bound"], sw=1.8, rx=8, stroke_opacity=0.4)
    s.label_tag(hx + 16, hy - 13, "HORIZON OS PLATFORM", fill_bg=C["panel"], ink=C["ink"], w=210)
    s.text(hx + hw - 20, hy + 22, "OS services · not app code", 12, C["muted"], anchor="end", mono=True)

    pw = (hw - 48 - 2 * gap) / 3
    py = hy + 40
    ph = 120

    # Storage
    s.box(hx + 24, py, pw, ph, "Storage", "on-device files", owns="local media source", stroke=C["line"], fill=C["panel2"])
    # Decoder
    s.box(
        hx + 24 + pw + gap,
        py,
        pw,
        ph,
        "HW Decoder",
        "MediaCodec · HEVC 8K",
        owns="runs under Horizon OS",
        stroke=C["video"],
        fill="#1a1810",
    )
    # Compositor
    s.rect(hx + 24 + 2 * (pw + gap), py, pw, ph, fill="#1a1524", stroke="#8b6bb5", sw=1.8, rx=6)
    s.text(hx + 24 + 2 * (pw + gap) + 16, py + 28, "Meta compositor", 20, C["ink"], weight=700)
    s.text(hx + 24 + 2 * (pw + gap) + 16, py + 50, "what the eyes see", 14, C["dim"])
    s.text(hx + 24 + 2 * (pw + gap) + 16, py + 78, "Direct layer · 180 / 360", 13, C["ink"], weight=600, mono=True)
    s.text(hx + 24 + 2 * (pw + gap) + 16, py + 100, "Eye buffer ← mesh path", 13, C["muted"], mono=True)

    # ============================================================
    # FLOWS (drawn last, on top)
    # Anchors
    # ============================================================
    home_cx = ox + ow / 2
    home_bot = oy + 36 + 150
    ver_top = oy + 220
    ver_cx = ox + ow / 2

    src_cx = kx + 14 + (col_w - 28) / 2
    src_cy = cy0 + 70 + 32
    play_cx = kx + 14 + (col_w - 28) / 2
    play_cy = cy0 + 146 + 32
    resolv_cy = cy0 + 222 + 32

    dec_cx = hx + 24 + pw + gap + pw / 2
    dec_cy = py + ph / 2
    stor_cx = hx + 24 + pw / 2
    stor_cy = py + ph / 2
    comp_cx = hx + 24 + 2 * (pw + gap) + pw / 2
    comp_cy = py + ph / 2

    mesh_cx = ux + 14 + (col_w - 28) / 2
    mesh_cy = cy0 + 146 + 32
    inter_cx = ux + 14 + (col_w - 28) / 2
    inter_cy = cy0 + 70 + 32

    bridge_cx = bx + col_w / 2
    bridge_mid = cy0 + 190

    # rail between off-headset and quest
    rail = qx - 18

    # --- VIDEO solid: Home → Sources → Playback → Decoder → Compositor ---
    s.path(
        f"M{home_cx:.1f} {home_bot:.1f} V{oy + oh - 40:.1f} H{rail:.1f} "
        f"V{src_cy:.1f} H{kx + 14:.1f}",
        C["video"],
        3.2,
        marker="mv",
        glow=True,
    )
    # also local storage → sources
    s.path(
        f"M{stor_cx:.1f} {py:.1f} V{cy0 + ch + 8:.1f} H{src_cx:.1f} V{cy0 + 70 + 64:.1f}",
        C["video"],
        2.6,
        glow=True,
    )
    s.path(f"M{src_cx:.1f} {src_cy + 32:.1f} V{play_cy - 32:.1f}", C["video"], 3.0, marker="mv")
    s.path(
        f"M{play_cx:.1f} {play_cy + 32:.1f} V{hy - 8:.1f} H{dec_cx:.1f} V{py:.1f}",
        C["video"],
        3.2,
        marker="mv",
        glow=True,
    )
    s.path(
        f"M{dec_cx + pw / 2 - 8:.1f} {dec_cy:.1f} H{comp_cx - pw / 2 + 8:.1f}",
        C["video"],
        3.2,
        marker="mv",
        glow=True,
    )
    # label
    s.text(rail + 8, src_cy - 10, "video", 11, C["video"], weight=700, mono=True)

    # --- VIDEO dashed fisheye: Decoder → Lens mesh → Compositor (least proven) ---
    left_inner = ax + 8
    s.path(
        f"M{dec_cx:.1f} {py:.1f} V{cy0 + ch + 20:.1f} H{left_inner:.1f} "
        f"V{mesh_cy:.1f} H{ux + 14:.1f}",
        C["video"],
        2.4,
        dash="3 7",
        marker="mv",
    )
    s.path(
        f"M{mesh_cx:.1f} {mesh_cy + 32:.1f} V{hy - 20:.1f} H{comp_cx:.1f} V{py:.1f}",
        C["video"],
        2.4,
        dash="3 7",
        marker="mv",
    )
    # least proven callout on dashed decoder→mesh edge (not on JNI)
    call_x = left_inner + 24
    call_y = cy0 + ch + 4
    s.rect(call_x, call_y, 168, 22, fill="#1a1810", stroke=C["warn"], sw=1.2, rx=3)
    s.text(call_x + 84, call_y + 15, "DASHED · LEAST PROVEN", 10, C["warn"], weight=700, anchor="middle", mono=True, ls=0.6)

    # --- CONTROL: controller → Interaction → Bridge → Playback ---
    ctrl_x = qx + 12
    ctrl_y = qy + qh - 36
    a(f'<circle cx="{ctrl_x}" cy="{ctrl_y}" r="9" fill="{C["bg"]}" stroke="{C["control"]}" stroke-width="2"/>')
    s.text(ctrl_x + 16, ctrl_y + 4, "controller", 12, C["muted"], mono=True)
    s.path(
        f"M{ctrl_x:.1f} {ctrl_y - 10:.1f} V{inter_cy:.1f} H{ux + 14:.1f}",
        C["control"],
        2.8,
        marker="mc",
    )
    s.path(
        f"M{ux + col_w - 14:.1f} {inter_cy:.1f} H{bridge_cx:.1f} V{bridge_mid:.1f}",
        C["control"],
        2.8,
    )
    s.path(
        f"M{bridge_cx:.1f} {bridge_mid:.1f} H{kx + 14:.1f} V{play_cy:.1f}",
        C["control"],
        2.8,
        marker="mc",
    )
    s.text(bridge_cx + 8, bridge_mid - 10, "control", 11, C["control"], weight=700, mono=True)

    # --- MEASURE: probes in Unity + Kotlin → Verification (NOT compositor) ---
    a(f'<circle cx="{inter_cx + 80:.1f}" cy="{cy0 + 30:.1f}" r="6" fill="{C["bg"]}" stroke="{C["measure"]}" stroke-width="2"/>')
    a(f'<circle cx="{play_cx + 80:.1f}" cy="{cy0 + 30:.1f}" r="6" fill="{C["bg"]}" stroke="{C["measure"]}" stroke-width="2"/>')
    s.text(inter_cx + 92, cy0 + 34, "probe", 11, C["measure"], mono=True)
    s.text(play_cx + 92, cy0 + 34, "probe", 11, C["measure"], mono=True)
    # up and left to verification — avoid compositor
    measure_rail_y = ay - 6
    s.path(
        f"M{inter_cx + 80:.1f} {cy0 + 30:.1f} V{measure_rail_y:.1f} "
        f"H{play_cx + 80:.1f} H{rail:.1f} V{ver_top + 75:.1f} H{ox + ow - 20:.1f}",
        C["measure"],
        2.2,
        dash="2 6",
        marker="mm",
    )
    s.text(rail - 70, measure_rail_y - 8, "QA_EVENT", 11, C["measure"], weight=700, mono=True)
    s.text(ox + ow + 8, ver_top + 70, "no compositor probe", 11, C["muted"], mono=True)
    s.text(ox + ow + 8, ver_top + 88, "(presented-frame open)", 11, C["muted"], mono=True)

    # ============================================================
    # Footer
    # ============================================================
    s.path(f"M48 {H - 52} H{W - 48}", C["line"], 1.0, opacity=0.7)
    s.text(
        48,
        H - 28,
        "Logical deployment / container view · not to scale · sources: architecture-diagram · meta-spec · D26",
        13,
        C["muted"],
        mono=True,
    )
    s.text(
        W - 48,
        H - 28,
        "decode in Kotlin/Media3 → surface across JNI → compositor composites",
        13,
        C["dim"],
        anchor="end",
        mono=True,
    )

    a("</svg>\n")
    OUT_SVG.write_text("".join(s.parts), encoding="utf-8")
    print(f"Wrote {OUT_SVG} ({OUT_SVG.stat().st_size} bytes)")

    import cairosvg

    # 2x for crisp retina on Pages
    cairosvg.svg2png(
        url=str(OUT_SVG),
        write_to=str(OUT_PNG),
        output_width=W * 2,
        output_height=H * 2,
    )
    print(f"Wrote {OUT_PNG} ({OUT_PNG.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
