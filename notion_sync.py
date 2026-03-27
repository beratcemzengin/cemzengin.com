import os
import re
from notion_client import Client

# GitHub Secrets'tan verileri çekiyoruz
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE_ID"]

def slugify(text):
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    return re.sub(r'[^\w\-]', '', text)

try:
    # Kritik Düzeltme: .query() yerine .databases.query() kullanıyoruz
    response = notion.databases.query(
        database_id=database_id,
        filter={
            "property": "Status",
            "select": {
                "equals": "Published"
            }
        }
    )
    results = response.get("results")

    if not results:
        print("Yayinlanacak 'Published' durumunda yazi bulunamadi.")

    for page in results:
        # Notion sütun isimlerini kontrol et: Name, Date, Status
        properties = page["properties"]
        title = properties["Name"]["title"][0]["plain_text"]
        
        # Tarih yoksa bugünü al
        if properties["Date"]["date"]:
            date_val = properties["Date"]["date"]["start"]
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
            
    print("Islem basariyla tamamlandi.")

except Exception as e:
    print(f"Hata olustu: {e}")
