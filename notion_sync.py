import os
from notion_client import Client

# GitHub Secrets'tan verileri alıyoruz
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE_ID"]

try:
    results = notion.databases.query(
        database_id=database_id,
        filter={
            "property": "Status",
            "select": {
                "equals": "Published"
            }
        }
    ).get("results")

    for page in results:
        # Notion'daki sütun isimlerinin "Name", "Date" ve "Status" olduğundan emin ol
        title = page["properties"]["Name"]["title"][0]["plain_text"]
        date = page["properties"]["Date"]["date"]["start"]
        
        filename = f"_posts/{date}-{title.lower().replace(' ', '-')}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"layout: post\n")
            f.write(f"title: \"{title}\"\n")
            f.write(f"date: {date}\n")
            f.write("---\n\n")
            f.write("Notion'dan otomatik olarak senkronize edildi.")
    print("Senkronizasyon basariyla tamamlandi.")
except Exception as e:
    print(f"Hata olustu: {e}")
