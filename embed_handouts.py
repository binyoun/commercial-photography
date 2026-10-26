#!/usr/bin/env python3
"""Embed the team worksheet files into studio.html as data-URI downloads.

Re-runnable: rewrites everything between the HANDOUTS markers, so regenerate
the PDF/DOCX first, then run this again.
"""

import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
PAGE = ROOT / "studio.html"
HANDOUTS = ROOT / "handouts"

FILES = [
    ("Brand-Dossier-Team-Worksheet.pdf", "application/pdf", "Download the worksheet", "One page, one team"),
]

buttons = []
for name, mime, title, sub in FILES:
    path = HANDOUTS / name
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    buttons.append(
        f'<a class="dlbtn solid mono disp" download="{name}" href="data:{mime};base64,{b64}">'
        f"{title}<span>{sub}</span></a>"
    )

block = f"""      <div class="handout">
        <div class="ht">
          <span class="he mono disp">Team worksheet</span>
          <h3 class="disp">One page, one team</h3>
          <p>Team name, members, and who led each of the seven searches, with a line per finding.
          Fill it in together, attach your slide deck, and bring both to class.</p>
        </div>
        <div class="dl">
          {buttons[0]}
        </div>
      </div>"""

html = PAGE.read_text()
new = re.sub(
    r"(<!--HANDOUTS:START-->).*?(<!--HANDOUTS:END-->)",
    lambda m: f"{m.group(1)}\n{block}\n      {m.group(2)}",
    html,
    flags=re.S,
)
if new == html:
    raise SystemExit("markers not found or nothing changed")

PAGE.write_text(new)
print(f"embedded {len(FILES)} files; studio.html is now {len(new)/1024:.0f} KB")
