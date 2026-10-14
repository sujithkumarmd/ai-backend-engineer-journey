"""Redraw the progress bars at the top of the root README from its concept checkboxes."""

import re
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- progress:start -->", "<!-- progress:end -->"
BAR_WIDTH = 30


def bar(done, total):
    filled = round(done / total * BAR_WIDTH) if total else 0
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def percent(done, total):
    return round(done / total * 100) if total else 0


text = README.read_text()

# Each phase/project is a <details> block; count its ticked and unticked boxes
phases = []
for block in re.findall(r"<details.*?</details>", text, flags=re.S):
    title = re.search(r"<h3>(.*?)(?:<code>|</h3>)", block).group(1).strip()
    done = len(re.findall(r"^- \[x\]", block, flags=re.M))
    todo = len(re.findall(r"^- \[ \]", block, flags=re.M))
    if done + todo:
        phases.append((title, done, done + todo))

total_done = sum(done for _, done, _ in phases)
total = sum(count for _, _, count in phases)
current = next(((t, d, c) for t, d, c in phases if d < c), phases[-1])

lines = [
    START,
    "",
    f"![Progress](https://img.shields.io/badge/progress-{total_done}%2F{total}%20items%20"
    f"({percent(total_done, total)}%25)-brightgreen?style=for-the-badge)",
    "",
    f"**Overall** &nbsp; `{bar(total_done, total)}` &nbsp; **{percent(total_done, total)}%** "
    f"· {total_done} / {total} items",
    "",
    f"**{current[0]}** &nbsp; `{bar(current[1], current[2])}` &nbsp; "
    f"**{percent(current[1], current[2])}%** · {current[1]} / {current[2]} items",
    "",
    END,
]

new_text = re.sub(re.escape(START) + ".*?" + re.escape(END), "\n".join(lines), text, flags=re.S)
README.write_text(new_text)
print(f"Overall {total_done}/{total} ({percent(total_done, total)}%) · current: {current[0]} {current[1]}/{current[2]}")
