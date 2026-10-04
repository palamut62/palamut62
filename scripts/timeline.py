"""Generate the Journey timeline SVGs (desktop + mobile, light + dark) into assets/."""

from html import escape
from pathlib import Path

NODES = [
    ("2015", "Joined GitHub", "Account created", ""),
    ("2021", "First repos", "Python · PyQt tools", "2 commits"),
    ("2024", "Desktop tools", "Private PyQt6 apps", "234 commits"),
    ("2025", "All-in on AI", "nootle · tweet bot", "440 commits"),
    ("2026 H1", "Agent tooling", "agent-forge · arasclaw", "1,170 commits"),
    ("2026 H2", "Desktop apps", "termflow · MausCrew", "1,160+ commits"),
]
FIRST_AI = 3  # nodes from this index on are highlighted
THEMES = {
    "light": dict(text="#1f2328", muted="#59636e", line="#d1d9e0", bg="#ffffff", accent="#0969da"),
    "dark": dict(text="#f0f6fc", muted="#9198a1", line="#3d444d", bg="#0d1117", accent="#4493f8"),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
LABEL = "Journey: " + "; ".join(f"{y} {t}" for y, t, _, _ in NODES)
ASSETS = Path(__file__).resolve().parent.parent / "assets"


def text(x, y, s, size, fill, family=SANS, weight="400", anchor="middle"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(s)}</text>')


def node(cx, cy, i, c):
    hot = i >= FIRST_AI
    out = []
    if i == len(NODES) - 1:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="{c["accent"]}" fill-opacity="0.18"/>')
    col = c["accent"] if hot else c["muted"]
    out.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{col if hot else c["bg"]}" '
               f'stroke="{col}" stroke-width="2"/>')
    return out


def frame(w, h, c):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(LABEL)}">',
            f'<title>{escape(LABEL)}</title>',
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="none" '
            f'stroke="{c["line"]}"/>']


def desktop(c):
    w, h, y = 960, 210, 92
    xs = [100 + i * 152 for i in range(len(NODES))]
    p = frame(w, h, c)
    p.append(f'<line x1="40" y1="{y}" x2="{w - 40}" y2="{y}" stroke="{c["line"]}" stroke-width="2"/>')
    p.append(f'<line x1="{xs[FIRST_AI]}" y1="{y}" x2="{w - 40}" y2="{y}" stroke="{c["accent"]}" '
             f'stroke-width="2"/>')
    for i, (x, (year, title, sub, stat)) in enumerate(zip(xs, NODES)):
        hot = i >= FIRST_AI
        p.append(text(x, y - 28, year, 14, c["accent"] if hot else c["muted"], MONO, "600"))
        p += node(x, y, i, c)
        p.append(text(x, y + 40, title, 15, c["text"], weight="600"))
        p.append(text(x, y + 62, sub, 12.5, c["muted"]))
        if stat:
            p.append(text(x, y + 84, stat, 11.5, c["muted"], MONO))
    return "\n".join(p + ["</svg>"]) + "\n"


def mobile(c):
    step, top, x = 92, 44, 44
    w, h = 420, top + step * (len(NODES) - 1) + 60
    ys = [top + i * step for i in range(len(NODES))]
    p = frame(w, h, c)
    p.append(f'<line x1="{x}" y1="{ys[0]}" x2="{x}" y2="{ys[-1]}" stroke="{c["line"]}" stroke-width="2"/>')
    p.append(f'<line x1="{x}" y1="{ys[FIRST_AI]}" x2="{x}" y2="{ys[-1]}" stroke="{c["accent"]}" '
             f'stroke-width="2"/>')
    for i, (yy, (year, title, sub, stat)) in enumerate(zip(ys, NODES)):
        hot = i >= FIRST_AI
        p += node(x, yy, i, c)
        p.append(text(76, yy - 8, year, 14, c["accent"] if hot else c["muted"], MONO, "600", "start"))
        p.append(text(76, yy + 14, title, 17, c["text"], weight="600", anchor="start"))
        line = sub + (f"  ·  {stat}" if stat else "")
        p.append(text(76, yy + 36, line, 13.5, c["muted"], anchor="start"))
    return "\n".join(p + ["</svg>"]) + "\n"


if __name__ == "__main__":
    for name, c in THEMES.items():
        (ASSETS / f"timeline-{name}.svg").write_text(desktop(c), encoding="utf-8")
        (ASSETS / f"timeline-mobile-{name}.svg").write_text(mobile(c), encoding="utf-8")
    print("ok")
