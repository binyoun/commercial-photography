# Commercial Photography: Course Studio

Course companion site for Commercial Photography (VART3672), RMIT University Vietnam.

Live: https://binyoun.github.io/commercial-photography/

## What this is

A single self-contained page with hash routing. Twelve sessions, each pairing a lecture
with studio time. Two session companions are fully built; the rest are placeholders that
render from the `SESSIONS` data in `studio.html`.

- **Landing** — semester map, weekly session anatomy, assessment thread (A1, A2, A3)
- **S03 Product: From Brand to Image** — commercial pipeline, four-layer brand
  deconstruction, seven case pairs, persona sentence, moodboard rules, a craft-first
  five-step AI ladder, 2026 trends, lighting recipes, prep, treatment template
- **S08 Trend and Brand Analysis** — seven-part pre-class brand dossier, image ecosystem,
  brand kit reading, platform grammar, trend fit test, storytelling structures,
  reverse-brief method, brand kit build, three-surface campaign board

Deliberately free of dates and week numbers so it can be reused across semesters.

**Design:** a light contact-sheet theme. Warm paper ground, white frames, sprocket
rails fixed down both edges, dark slate blocks for part dividers and prompts, and the
signal red carried over from the class deck.

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Course hub: sessions, assessments, handouts, references. Redirects old `#/...` links to the studio. |
| `studio.html` | The session companion site (hash-routed). Edit this for session content. |
| `embed_handouts.py` | Re-embeds `handouts/*.pdf` into `studio.html` as data URIs |
| `restyle.py` | Holds the Contact Sheet stylesheet; re-run to reapply the theme |
| `handouts/dossier-worksheet.html` | Print source for the team worksheet |
| `handouts/make_docx.py` | Builds the editable DOCX version |
| `handouts/paste-into-google-doc.html` | Copy-paste source for a shared Google Doc |

## Updating the worksheet

```bash
# 1. edit handouts/dossier-worksheet.html, then re-render the PDF
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=handouts/Brand-Dossier-Team-Worksheet.pdf \
  handouts/dossier-worksheet.html

# 2. re-embed it into the page
python3 embed_handouts.py
```

## Adding a session companion

1. Add a `<div class="view" id="view-sNN">` block, copying the S03 structure.
2. Add the key to the `BUILT` map in the script at the bottom.
3. Set `live: true` on that session in `SESSIONS` so its card lights up.
