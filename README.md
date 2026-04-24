# pat-personal-blog

Static blog hosted on GitHub Pages at `monkbuddy62.github.io/pat-personal-blog`.

---

## Writing a new post

1. Create a `.md` file in `posts/<section>/<slug>.md`

   Sections: `projects`, `music`, `thoughts`

   ```
   posts/thoughts/my-new-post.md
   ```

2. Add frontmatter at the top:

   ```markdown
   ---
   title: My Post Title
   date: April 2026
   ---

   Post content goes here. Standard Markdown.
   ```

3. Run the build and publish:

   ```bash
   ./publish.sh
   ```

   Or with a custom commit message:

   ```bash
   ./publish.sh "add post: my new post"
   ```

That's it. `publish.sh` runs `build.py`, stages everything, commits, and pushes.

---

## What `build.py` does

- Converts each `posts/<section>/*.md` file into an HTML post page
- Regenerates each section index (`projects/`, `music/`, `thoughts/`)
- Regenerates the archive and home page

You never edit the generated HTML directly — always edit the `.md` source and re-run `build.py`.

---

## Changing the style

Theme values (colors, fonts, spacing) live as CSS custom properties at the top of `style.css`. A full theme swap is just editing that variables block.

For experiments, use a branch so reverting is just `git checkout main`:

```bash
git checkout -b theme-experiment
# edit style.css
git checkout main   # revert, no undo needed
```

---

## Dependencies

```bash
pip install -r requirements.txt   # just: markdown
```

---

## Site structure

```
posts/<section>/<slug>.md   ← write here
build.py                    ← run to rebuild
publish.sh                  ← build + commit + push
style.css                   ← all styles; CSS vars at top for theming
index.html                  ← home page (generated)
archive/                    ← full post list (generated)
projects/ music/ thoughts/  ← section indexes (generated)
about/ blogroll/            ← static pages, edit HTML directly
```
