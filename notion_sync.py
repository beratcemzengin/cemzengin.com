import os
import re
import json
import urllib.request

# Ayarlar
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

def slugify(text):
    text = text.lower()
    tr_map = str.maketrans("ığüşöç", "igusoç")
    text = text.translate(tr_map)
    text = re.sub(r'\s+', '-', text)
    return re.sub(r'[^\w\-]', '', text)

# Notion API'ye doğrudan istek atıyoruz
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Sadece "Published" olanları filtrele
data = json.dumps({
    "filter": {
        "property": "Status",
        "select": {
            "equals": "Published"
        }
    }
}).encode('utf-8')

try:
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode())
        pages = res_data.get("results", [])

    if not pages:
        print("Yayınlanacak yazı bulunamadı (Status=Published olanları kontrol et).")

    for page in pages:
        props = page["properties"]
        
        # Başlık Al (Name sütunu)
        title = props["Name"]["title"][0]["plain_text"]
        
        # Tarih Al (Date sütunu)
        date_prop = props.get("Date", {}).get("date")
        date_val = date_prop["start"] if date_prop else "2026-03-27"
        
        filename = f"_posts/{date_val}-{slugify(title)}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"layout: post\n")
            f.write(f"title: \"{title}\"\n")
            f.write(f"date: {date_val}\n")
            f.write("---\n\n")
            f.write("Notion'dan API ile doğrudan çekildi. İçerik yakında eklenecek.")
            
        print(f"BAŞARILI: {filename} dosyası oluşturuldu.")

    print("İşlem başarıyla tamamlandı.")

except Exception as e:
    print(f"Hata Detayı: {str(e)}")
