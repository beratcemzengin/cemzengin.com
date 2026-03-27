import urllib.error

try:
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode())
        pages = res_data.get("results", [])

except urllib.error.HTTPError as e:
    print("HTTP STATUS:", e.code)
    print("HTTP BODY:", e.read().decode("utf-8", errors="replace"))
except Exception as e:
    print(f"Hata Detayı: {str(e)}")
