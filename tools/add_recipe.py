#!/usr/bin/env python3
"""Add one or more recipes to the Kitchen Recipes app.

Usage:  python3 tools/add_recipe.py recipe.json [more.json ...]

Each JSON file holds one recipe (or a list of them) using the keys below.
Only "title", "ingredients" and "steps" are required; the rest default sensibly.

{
  "title": "Amalfi Lemon Cake",
  "serves": "10",
  "time": "1 hr 15 min",
  "time_detail": "15 min prep + 1 hr bake",
  "cal": "", "fat": "", "protein": "", "netcarbs": "", "fibre": "",
  "ingredients": ["250g butter", "..."],          # or {"h": "For the syrup"} for a heading
  "steps": ["Preheat oven to 180C.", "..."],      # or {"h": "Syrup"} for a heading
  "tips": [{"h": "Note", "t": "Keeps for 3 days."}],
  "sources": ["delicious. via Herald Sun"],
  "cats": ["Snacks & sweets"],                    # Breakfast, Mains, Soups & starters, Sides & salads, Snacks & sweets, Drinks
  "tags": ["Vegetarian", "Family & friends"]
}

The script rewrites index.html (data block only) and bumps the version in sw.js
so installed copies pick up the change.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX, SW = ROOT / 'index.html', ROOT / 'sw.js'
STOP = {'and', 'with', 'the', 'a', 'of', 'in', 'on', 'for', 'to'}

def make_id(title, taken):
    words = re.sub(r"[^a-z0-9 ]", " ", title.lower().replace("’", " ").replace("'", " ")).split()
    base = " ".join(w for w in words if w not in STOP) or " ".join(words)
    rid, n = base, 2
    while rid in taken:
        rid, n = f"{base} {n}", n + 1
    return rid

def norm_items(items):
    out = []
    for it in items:
        if isinstance(it, str):
            out.append({"t": it})
        elif "h" in it:
            out.append({"h": it["h"]})
        else:
            out.append({"t": it["t"]})
    return out

def main(paths):
    html = INDEX.read_text(encoding='utf-8')
    m = re.search(r'(<script id="data" type="application/json">)(.*?)(</script>)', html, re.S)
    data = json.loads(m.group(2))
    taken = {r['id'] for r in data['recipes']}
    added = []
    for p in paths:
        raw = json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
        for src in (raw if isinstance(raw, list) else [raw]):
            r = {
                "title": src["title"].strip(),
                "serves": str(src.get("serves", "")),
                "time": src.get("time", ""),
                "time_detail": src.get("time_detail", ""),
                "cal": str(src.get("cal", "")), "fat": str(src.get("fat", "")),
                "protein": str(src.get("protein", "")), "netcarbs": str(src.get("netcarbs", "")),
                "fibre": str(src.get("fibre", "")),
                "ingredients": norm_items(src["ingredients"]),
                "steps": norm_items(src["steps"]),
                "tips": src.get("tips", []),
                "sources": src.get("sources", ["Family & friends"]),
                "kind": src.get("kind", "family"),
                "pesc_plan": False,
                "slots": [],
                "id": src.get("id") or make_id(src["title"], taken),
                "cats": src.get("cats", ["Mains"]),
                "tags": src.get("tags", ["Family & friends"]),
            }
            taken.add(r["id"]); data['recipes'].append(r); added.append(r)
    new_json = json.dumps(data, ensure_ascii=False, separators=(', ', ': '))
    html = html[:m.start(2)] + new_json + html[m.end(2):]
    INDEX.write_text(html, encoding='utf-8')
    sw = SW.read_text(encoding='utf-8')
    sw, n = re.subn(r"(const VERSION = 'kitchen-recipes-v)(\d+)(';)", lambda mm: f"{mm.group(1)}{int(mm.group(2)) + 1}{mm.group(3)}", sw)
    SW.write_text(sw, encoding='utf-8')
    ver = re.search(r"kitchen-recipes-v\d+", sw).group(0)
    for r in added:
        print(f"added: {r['title']}  (id: {r['id']})")
    print(f"recipes now: {len(data['recipes'])}; service worker {ver}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
