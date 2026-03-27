import os
import re
from notion_client import Client

# GitHub Secrets'tan verileri çekiyoruz
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE_ID"]

def slugify(text):
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    # Türkçe karakterleri ve özel işaretleri temizle
    text = text.replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
    return re.sub(r'[^\w\-]', '', text)

try:
    # Doğu yazım şekli budur:
    response = notion.databases.query(database_id=database_id)
    results = response.get("results")

    if not results:
        print("Veritabaninda hic yazi bulunamadi.")

    for page in results:
        props = page["properties"]
        
        # Sadece "Status" sütununda "Published" seçili olanları filtrele
        # Not: Status veya Select isimlerini kontrol et!
        status_obj = props.get("Status", {}).get("select")
        
        if status_obj and status_obj.get("name") == "Published":
            title = props["Name"]["title"][0]["plain_text"]
            
            # Tarih kontrolü
            if props["Date"]["date"]:
                date_val = props["Date"]["date"]["start"]
            else:
                from datetime import date as dt
                date_val = dt.today().isoformat()
            
            filename = f"_posts/{date_val}-{slugify(title)}.md"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"layout: post\n")
                f.write(f"title: \"{title}\"\n")
                f.write(f"date: {date_val}\n")
                f.write("---\n\n")
                f.write("Notion'dan otomatik olarak senkronize edildi.\n")
                print(f"Yazi olusturuldu: {filename}")
            
    print("Islem basariyla tamamlandi.")

except Exception as e:
    print(f"Hata detayi: {str(e)}")
