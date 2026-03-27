import os
import re
from notion_client import Client

# Anahtarlar
notion = Client(auth=os.environ["NOTION_TOKEN"])
db_id = os.environ["NOTION_DATABASE_ID"]

def slugify(text):
    text = text.lower()
    # Türkçe karakter fix
    tr_map = str.maketrans("ığüşöç", "igusoç")
    text = text.translate(tr_map)
    text = re.sub(r'\s+', '-', text)
    return re.sub(r'[^\w\-]', '', text)

try:
    # Sorgu metodunu garantili hale getirdik
    response = notion.databases.query(database_id=db_id)
    pages = response.get("results", [])

    if not pages:
        print("Notion'da veri bulunamadi.")

    for page in pages:
        props = page["properties"]
        
        # STATUS KONTROLÜ
        # Notion'daki sütun isminin "Status" ve seçeneğin "Published" olduğundan emin ol
        status_data = props.get("Status", {}).get("select")
        if status_data and status_data.get("name") == "Published":
            
            title = props["Name"]["title"][0]["plain_text"]
            
            # Tarih varsa al, yoksa bugünü yaz
            date_prop = props.get("Date", {}).get("date")
            date_val = date_prop["start"] if date_prop else "2026-03-27"
            
            filename = f"_posts/{date_val}-{slugify(title)}.md"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"layout: post\n")
                f.write(f"title: \"{title}\"\n")
                f.write(f"date: {date_val}\n")
                f.write("---\n\n")
                f.write("Notion'dan otomatik çekildi. İçerik yakında eklenecek.")
                
            print(f"Başarılı: {filename} oluşturuldu.")

    print("İşlem bitti.")

except Exception as e:
    print(f"Hata Detayi: {str(e)}")
