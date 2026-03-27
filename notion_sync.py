import os
import re
import json
import urllib.request

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

def slugify(text):
    text = text.lower()
    tr_map = str.maketrans("ığüşöç", "igusoc")
    text = text.translate(tr_map)
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"[^\w\-]", "", text)

def notion_request(url, payload):
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def get_plain_text_from_rich_text(rich_text_list):
    if not rich_text_list:
        return ""
    return "".join(item.get("plain_text", "") for item in rich_text_list)

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

payload = {
    "filter": {
        "property": "Status",
        "status": {
            "equals": "Published"
        }
    }
}

os.makedirs("_posts", exist_ok=True)

try:
    all_pages = []
    has_more = True
    next_cursor = None

    while has_more:
        if next_cursor:
            payload["start_cursor"] = next_cursor

        res_data = notion_request(url, payload)
        all_pages.extend(res_data.get("results", []))
        has_more = res_data.get("has_more", False)
        next_cursor = res_data.get("next_cursor")

    if not all_pages:
        print("Yayınlanacak yazı bulunamadı.")

    for page in all_pages:
        props = page.get("properties", {})

        title_items = props.get("Name", {}).get("title", [])
        title = get_plain_text_from_rich_text(title_items).strip() or "baslik-yok"

        date_prop = props.get("Date", {}).get("date")
        date_val = date_prop["start"] if date_prop else "2026-03-27"

        summary = get_plain_text_from_rich_text(
            props.get("Summary", {}).get("rich_text", [])
        )

        filename = f"_posts/{date_val}-{slugify(title)}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write("layout: post\n")
            f.write(f'title: "{title}"\n')
            f.write(f"date: {date_val}\n")
            f.write("---\n\n")
            f.write(summary or "İçerik bulunamadı.")

        print(f"BAŞARILI: {filename} oluşturuldu.")

    print("İşlem başarıyla tamamlandı.")

except Exception as e:
    print(f"Hata Detayı: {str(e)}")
