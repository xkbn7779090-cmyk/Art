from pathlib import Path
import json, re, urllib.parse

# === Настройки ===
USER = "xkbn7779090-cmyk"
REPO = "Art"
BRANCH = "main"
CREATED_IN = "Limburg, Netherlands"
YEAR = 2025
REGION = "LN"

# цены по размеру (правь при желании)
PRICE = {
    "20x20": 110, "25x25": 130, "29x29": 140, "30x24": 150, "24x30": 150, "24x18": 120,
    "40x40": 180, "50x40": 220, "50x50": 250, "60x50": 280, "70x50": 320, "70x100": 380,
    "100x70": 420, "120x40": 450
}

root = Path("images")
base_url = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/images"

# шаблон имени: #203_detail_30x24_CB.jpg  или  #203_main_20x20_C.jpg
pat = re.compile(r"#?(\d+)_(main|detail)_(\d+x\d+)_(C|CB)$", re.IGNORECASE)

def url_for(p: Path) -> str:
    return f"{base_url}/{urllib.parse.quote(p.name)}"

# === группировка ===
groups = {}  # key -> dict

for p in sorted(root.glob("*.jpg")):
    m = pat.match(p.stem)
    if not m:
        # игнорируем несоответствия
        # print("skip:", p.name)
        continue

    num, kind, size, mat = m.groups()
    size = size.lower()
    mat = mat.upper()
    kind = kind.lower()

    # спец-случай: 120x40_C #227 + #228 — одна картина с 4 фото
    if size == "120x40" and mat == "C" and num in {"227", "228"}:
        group_key = ("120x40", "C", "227-228")  # общий ключ
        primary_num = "227"
    else:
        group_key = (size, mat, num)
        primary_num = num

    g = groups.setdefault(group_key, {
        "num": primary_num,
        "size": size,
        "mat": mat,
        "images": {"main": [], "detail": []}
    })
    g["images"][kind].append(url_for(p))

# === сбор карточек ===
items = []
for (size, mat, _), g in groups.items():
    num = g["num"]
    size_cm = size.replace("x", "×") + " cm"
    mat_full = "Oil on canvas, stretched on stretcher frame" if mat == "C" else "Oil on canvas board"

    # заголовок и SKU (пока Untitled — можно позже подставить название)
    title = f"#{num} Untitled {size} {'canvas' if mat=='C' else 'board'}"
    sku = f"{REGION}-{YEAR}-{size}-{num}_Untitled_{size}_{mat}"
    price = f"€{PRICE.get(size, 200)}"

    # порядок картинок: сначала main, потом detail
    images = g["images"]["main"] + g["images"]["detail"]

    item = {
        "Title": title,
        "SKU": sku,
        "Size": size_cm,
        "Material": mat_full,
        "Created in": CREATED_IN,
        "Price": price,
        "Images": images,             # << все ссылки здесь
        "Description (EN)": "",
        "Description (RU)": ""
    }
    items.append(item)

# сортировка по номеру
def art_key(it):
    # вытаскиваем номер из "Title": "#110 ..."
    m = re.search(r"#(\d+)", it["Title"])
    return int(m.group(1)) if m else 0

items.sort(key=art_key)

Path("index_grouped.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OK: записей {len(items)} → index_grouped.json")
