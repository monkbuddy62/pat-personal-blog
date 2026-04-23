#!/usr/bin/env python3
"""
Add a new post:
  1. Create a .md file in posts/<section>/<slug>.md with this header:

       ---
       title: Your Post Title
       date: April 2026
       ---

       Your content here...

  2. Run: python build.py

  It generates the HTML post page, updates the section index,
  the archive, and the home page.
"""

import os
import re
from datetime import datetime

try:
    import markdown
except ImportError:
    print("Run: pip install markdown")
    raise

SECTIONS   = ['projects', 'music', 'thoughts']
POSTS_DIR  = 'posts'
NAV        = """\
  <a href="/">home</a> /
  <a href="/projects/">projects</a> /
  <a href="/music/">music</a> /
  <a href="/thoughts/">thoughts</a> /
  <a href="/archive/">archive</a> /
  <a href="/about/">about</a> /
  <a href="/blogroll/">blogroll</a>"""

SECTION_INTROS = {
    'projects': 'Hardware, software, things I\'ve built or am building.',
    'music':    'Things I\'m listening to, playing, or thinking about.',
    'thoughts': 'Musings. Opinions. Things I\'m thinking about.',
}


def parse_post(path):
    with open(path, encoding='utf-8') as f:
        raw = f.read()

    if not raw.startswith('---'):
        raise ValueError(f"Missing frontmatter in {path}")

    _, front, body = raw.split('---', 2)
    meta = {}
    for line in front.strip().splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip()

    return meta, body.strip()


def render_page(title, inner, back_href, back_label):
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — Pat McCaffrey</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>

<p class="site-title"><a href="/">Pat McCaffrey</a></p>
<nav>
{NAV}
</nav>

<hr>

{inner}

<hr>

<footer>
  <a href="{back_href}">← {back_label}</a>
</footer>

</body>
</html>
"""


def build_post(md_path, section, slug):
    meta, body = parse_post(md_path)
    title = meta.get('title', slug.replace('-', ' ').title())
    date  = meta.get('date', '')

    html_body = markdown.markdown(body, extensions=['fenced_code'])

    inner = f"""<h2>{title}</h2>
<p class="post-meta">{date} &mdash; <a href="/{section}/">{section}</a></p>

{html_body}"""

    out_dir = os.path.join(section, slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'index.html')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(render_page(title, inner, f'/{section}/', section))

    print(f"  wrote {out_path}")
    return {'title': title, 'date': date, 'section': section, 'slug': slug}


def collect_all_posts():
    """Scan posts/ directory and build all posts. Returns list of post dicts."""
    all_posts = []
    for section in SECTIONS:
        section_dir = os.path.join(POSTS_DIR, section)
        if not os.path.isdir(section_dir):
            continue
        for fname in sorted(os.listdir(section_dir)):
            if not fname.endswith('.md'):
                continue
            slug = fname[:-3]
            md_path = os.path.join(section_dir, fname)
            print(f"Building: {section}/{slug}")
            post = build_post(md_path, section, slug)
            all_posts.append(post)
    return all_posts


def write_section_index(section, posts):
    intro = SECTION_INTROS.get(section, '')
    items = '\n'.join(
        f'  <li><span class="post-date">{p["date"]}</span> &mdash; '
        f'<a href="/{section}/{p["slug"]}/">{p["title"]}</a></li>'
        for p in reversed(posts)
    )
    inner = f"""<h2>{section.title()}</h2>

<p>{intro}</p>

<ul class="post-list">
{items}
</ul>"""
    page = render_page(section.title(), inner, '/', 'home')
    path = os.path.join(section, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(page)
    print(f"  updated {path}")


def write_archive(all_posts):
    by_year = {}
    for p in all_posts:
        year = p['date'].split()[-1] if p['date'] else 'Unknown'
        by_year.setdefault(year, []).append(p)

    blocks = []
    for year in sorted(by_year.keys(), reverse=True):
        items = '\n'.join(
            f'  <li><span class="post-date">{p["date"]}</span> &mdash; '
            f'<a href="/{p["section"]}/{p["slug"]}/">{p["title"]}</a> '
            f'<small>({p["section"]})</small></li>'
            for p in reversed(by_year[year])
        )
        blocks.append(f'<h3>{year}</h3>\n\n<ul class="post-list">\n{items}\n</ul>')

    inner = '<h2>Archive</h2>\n\n' + '\n\n'.join(blocks)
    page  = render_page('Archive', inner, '/', 'home')
    with open('archive/index.html', 'w', encoding='utf-8') as f:
        f.write(page)
    print("  updated archive/index.html")


def write_home(all_posts):
    recent = list(reversed(all_posts))[:10]
    items  = '\n'.join(
        f'  <li><span class="post-date">{p["date"]}</span> &mdash; '
        f'<a href="/{p["section"]}/{p["slug"]}/">{p["title"]}</a> '
        f'<small>({p["section"]})</small></li>'
        for p in recent
    )

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pat McCaffrey</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>

<p class="site-title"><a href="/">Pat McCaffrey</a></p>
<nav>
{NAV}
</nav>

<hr>

<p>I live in Seattle. I work in ag-tech. I build things, play music, and think too much about stuff. This is where I write about it.</p>

<h3>Recent</h3>

<ul class="post-list">
{items}
</ul>

<hr>

<footer>
  <a href="/about/">about</a> &nbsp;&middot;&nbsp;
  <a href="/blogroll/">blogroll</a> &nbsp;&middot;&nbsp;
  <a href="/archive/">archive</a>
</footer>

</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  updated index.html")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    all_posts = collect_all_posts()

    print("\nUpdating indexes...")
    for section in SECTIONS:
        section_posts = [p for p in all_posts if p['section'] == section]
        if section_posts:
            write_section_index(section, section_posts)

    write_archive(all_posts)
    write_home(all_posts)

    print(f"\nDone. {len(all_posts)} posts built.")
