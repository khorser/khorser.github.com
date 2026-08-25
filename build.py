#!/usr/bin/env python3
"""
Static site builder for the personal page.

Reads content.md (frontmatter + sections) and template.html (layout/CSS
with {{PLACEHOLDER}} tokens), renders everything to plain HTML, and
writes index.html. No JS is needed at runtime for content to appear —
crawlers and share-preview bots see the full page on the first request.

Usage:
    python3 build.py
    (then commit + push index.html alongside content.md)
"""

import re
import html
import sys
from pathlib import Path

ROOT = Path(__file__).parent
CONTENT_PATH = ROOT / "content.md"
TEMPLATE_PATH = ROOT / "template.html"
OUTPUT_PATH = ROOT / "index.html"

ICONS = {
    "github": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>',
    "linkedin": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M13.2 0H2.8C1.25 0 0 1.25 0 2.8v10.4C0 14.75 1.25 16 2.8 16h10.4c1.55 0 2.8-1.25 2.8-2.8V2.8C16 1.25 14.75 0 13.2 0ZM4.9 13.4H2.5V6h2.4v7.4ZM3.7 5c-.77 0-1.4-.63-1.4-1.4C2.3 2.83 2.93 2.2 3.7 2.2c.77 0 1.4.63 1.4 1.4 0 .77-.63 1.4-1.4 1.4Zm9.8 8.4h-2.4V9.8c0-.86-.02-1.97-1.2-1.97-1.2 0-1.38.94-1.38 1.9v3.67H6.1V6h2.3v1.01h.03c.32-.6 1.1-1.23 2.27-1.23 2.43 0 2.8 1.6 2.8 3.68v3.94Z"/></svg>',
    "email": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M1 4a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V4Zm1.2.2L8 8.8l5.8-4.6H2.2ZM14 5.4 8.3 9.9a.5.5 0 0 1-.6 0L2 5.4V12h12V5.4Z"/></svg>',
}

SECTION_META = {
    "expertise":  ("expertise",  "core-expertise --calypso"),
    "risk":       ("risk",       "risk --regulatory"),
    "technical":  ("technical",  "technical --depth"),
    "projects":   ("projects",   "ls ~/projects"),
    "ai-quantum": ("ai-quantum", "ai-quantum --practitioner"),
    "leadership": ("leadership", "how --i-work"),
}

CIRCUIT_PATTERNS = [
    [(90, "brass", "H"), (420, "teal", "X"), (760, "brass", "M")],
    [(220, "teal", "Z"), (600, "brass", "H")],
    [(150, "brass", "Y"), (500, "teal", "X"), (830, "brass", "M")],
    [(340, "teal", "H"), (700, "brass", "Z")],
    [(120, "brass", "X"), (460, "teal", "H"), (790, "brass", "Y")],
    [(260, "teal", "Z"), (640, "brass", "H")],
]


def circuit_svg(pattern):
    gates = "".join(
        f'<rect class="gate-{cls}" x="{x}" y="4" width="20" height="20" rx="2"></rect>'
        f'<text x="{x+10}" y="17" text-anchor="middle">{label}</text>'
        for x, cls, label in pattern
    )
    return (
        '<div class="circuit" aria-hidden="true"><svg viewBox="0 0 900 28" '
        f'preserveAspectRatio="none"><line x1="0" y1="14" x2="900" y2="14"></line>{gates}</svg></div>'
    )


def parse_frontmatter(text):
    m = re.match(r"^---\n([\s\S]*?)\n---\n?", text)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).split("\n"):
        if not line.strip():
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def parse_sections(body):
    sections = []
    current = None
    for line in body.split("\n"):
        h = re.match(r"^##\s+(.+?)\s*\{#([\w-]+)\}\s*$", line)
        if h:
            if current:
                sections.append(current)
            current = {"id": h.group(2), "title": h.group(1), "lines": []}
        elif current is not None:
            current["lines"].append(line)
    if current:
        sections.append(current)
    return {s["id"]: {"title": s["title"], "body": "\n".join(s["lines"]).strip()} for s in sections}


# ---- minimal inline/block markdown, matched to what content.md actually uses ----

def inline_md(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text


def block_md(body):
    """Paragraphs and '- ' dash lists, in source order."""
    out = []
    para = []
    list_items = []

    def flush_para():
        if para:
            out.append(f"<p>{inline_md(' '.join(para))}</p>")
            para.clear()

    def flush_list():
        if list_items:
            items = "".join(f"<li>{inline_md(i)}</li>" for i in list_items)
            out.append(f'<ul class="dash">{items}</ul>')
            list_items.clear()

    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped:
            flush_para()
            flush_list()
        elif stripped.startswith("- "):
            flush_para()
            list_items.append(stripped[2:])
        else:
            flush_list()
            para.append(stripped)
    flush_para()
    flush_list()
    return "".join(out)


def parse_technical(body):
    idx = re.search(r"^###\s+", body, re.M)
    if not idx:
        return body.strip(), []
    intro = body[: idx.start()].strip()
    rest = body[idx.start():]
    parts = re.split(r"^###\s+(.+)$", rest, flags=re.M)
    groups = []
    for i in range(1, len(parts), 2):
        groups.append({"title": parts[i].strip(), "items": parts[i + 1].strip()})
    return intro, groups


def render_technical(body):
    intro, groups = parse_technical(body)
    cols = []
    for g in groups:
        items_html = "<br>".join(html.escape(x.strip()) for x in g["items"].split("|"))
        cols.append(
            f'<div><h3>{html.escape(g["title"])}</h3><div class="items">{items_html}</div></div>'
        )
    intro_html = f'<p class="dim" style="margin-bottom:1.8rem">{inline_md(intro)}</p>' if intro else ""
    return f'{intro_html}<div class="toolgrid">{"".join(cols)}</div>'


def parse_projects(body):
    cards = []
    for m in re.finditer(r"```project\n([\s\S]*?)\n```\n?([\s\S]*?)(?=```project|\Z)", body):
        meta = {}
        for line in m.group(1).split("\n"):
            if not line.strip() or ":" not in line:
                continue
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
        cards.append({"meta": meta, "desc": m.group(2).strip()})
    return cards


def render_projects(body):
    cards_html = []
    for card in parse_projects(body):
        meta, desc = card["meta"], card["desc"]
        tag_class = "" if meta.get("tag", "").lower() == "public" else " private"
        tags_html = "".join(
            f"<span>{html.escape(t.strip())}</span>" for t in meta.get("tags", "").split(",") if t.strip()
        )
        link_html = ""
        if meta.get("link"):
            linktext = html.escape(meta.get("linktext", meta["link"]))
            link_html = (
                f'<a class="card-link" href="{html.escape(meta["link"])}" '
                f'target="_blank" rel="noopener">{linktext} →</a>'
            )
        cards_html.append(
            f'<div class="card"><div class="card-head">'
            f'<h3>{html.escape(meta.get("name", ""))}</h3>'
            f'<span class="card-tag{tag_class}">{html.escape(meta.get("tag", ""))}</span>'
            f'</div>{block_md(desc)}<div class="tags">{tags_html}</div>{link_html}</div>'
        )
    return f'<div class="projects">{"".join(cards_html)}</div>'


def render_generic(body):
    return f'<div class="block">{block_md(body)}</div>'


def main():
    if not CONTENT_PATH.exists():
        sys.exit(f"missing {CONTENT_PATH}")
    if not TEMPLATE_PATH.exists():
        sys.exit(f"missing {TEMPLATE_PATH}")

    text = CONTENT_PATH.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    sections = parse_sections(body)

    nav_ids = [sid for sid in SECTION_META if sid in sections]

    nav_html = "".join(f'<li><a href="#{sid}">{SECTION_META[sid][0]}</a></li>' for sid in nav_ids)
    nav_html += '<li><a href="#contact">contact</a></li>'

    sections_html = [circuit_svg(CIRCUIT_PATTERNS[0])]
    for i, sid in enumerate(nav_ids):
        title = sections[sid]["title"]
        sbody = sections[sid]["body"]
        cmd = SECTION_META[sid][1]
        if sid == "technical":
            inner = render_technical(sbody)
        elif sid == "projects":
            inner = render_projects(sbody)
        else:
            inner = render_generic(sbody)
        sections_html.append(
            f'<section id="{sid}"><p class="eyebrow">{html.escape(cmd)}</p>'
            f'<h2>{html.escape(title)}</h2>{inner}</section>'
        )
        if i < len(nav_ids) - 1:
            sections_html.append(circuit_svg(CIRCUIT_PATTERNS[(i + 1) % len(CIRCUIT_PATTERNS)]))

    hero_links = []
    footer_links = []
    if fm.get("github"):
        label = re.sub(r"^https?://", "", fm["github"])
        hero_links.append(f'<a href="{fm["github"]}" target="_blank" rel="noopener">{ICONS["github"]}{label}</a>')
        footer_links.append(f'<a href="{fm["github"]}" target="_blank" rel="noopener">{ICONS["github"]}{label}</a>')
    if fm.get("linkedin"):
        footer_links.append(f'<a href="{fm["linkedin"]}" target="_blank" rel="noopener">{ICONS["linkedin"]}linkedin</a>')
    if fm.get("email"):
        mail = f'<a href="mailto:{fm["email"]}">{ICONS["email"]}email</a>'
        hero_links.append(mail)
        footer_links.append(mail)

    badges_html = "".join(f'<span class="badge">{html.escape(b.strip())}</span>' for b in fm.get("badges", "").split("|") if b.strip())
    location_html = fm.get("location", "").replace(" · ", "<br>")
    contact_body = block_md(sections.get("contact", {}).get("body", ""))

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    out = (
        template
        .replace("{{NAME}}", html.escape(fm.get("name", "")))
        .replace("{{SLUG}}", html.escape(fm.get("name", "site")).lower())
        .replace("{{ROLE}}", inline_md(fm.get("role", "")))
        .replace("{{TERM_USER}}", html.escape(fm.get("term_user", "sergei@markets")))
        .replace("{{WHOAMI}}", html.escape(fm.get("whoami", "")))
        .replace("{{BADGES}}", badges_html)
        .replace("{{HERO_LINKS}}", "".join(hero_links))
        .replace("{{NAV}}", nav_html)
        .replace("{{LOCATION_HTML}}", location_html)
        .replace("{{LOCATION}}", html.escape(fm.get("location", "")))
        .replace("{{SECTIONS}}", "".join(sections_html))
        .replace("{{CONTACT_BODY}}", contact_body)
        .replace("{{FOOTER_LINKS}}", "".join(footer_links))
    )

    OUTPUT_PATH.write_text(out, encoding="utf-8")
    print(f"wrote {OUTPUT_PATH} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
