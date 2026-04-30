---
layout: post
title: "Huawei Switch ve AC'lerde Wi-Fi 7 (802.11be) AP Yapılandırma Rehberi"
date: 2026-04-30
categories: network
---

Huawei AP controller olan switchlerde switch güncellemesini yapsanız bile arayüzünden Wi-Fi 7 olan AP yayınını göremeyebiliyorsunuz. Bu gibi durumlarda komut satırı (CLI) üzerinden switch üzerine müdahale etmeniz gereken anlar oluyor. İşte adım adım kurulum rehberi:

## 1. Hazırlık ve Kontrol
Yeni cihazı bağlamadan önce altyapının hazır olduğundan emin olun:
* **Versiyon:** En az V200R024 ana sürümü ve SPH180 (veya üstü) yaması aktif olmalıdır.
* **Lisans:** `display license` komutu ile mevcut AP kapasitenizi kontrol edin.

## 2. Wi-Fi 7 Radyo Profili Oluşturma
Web arayüzünde Wi-Fi 7 seçeneği çıkmadığı için bu işlemi bir kez CLI'dan yapmanız yeterlidir:
```bash
system-view
wlan

# Wi-Fi 7 destekli 5GHz profili oluşturma
radio-5g-profile name wifi7-test
 radio-type dot11be
 quit
```

## 3. Yeni AP'yi Tanımlama
Yeni AP'yi switch'e bağlayın ve ID numarasını öğrenin:
```bash
display ap all
```
*(Örnek: Yeni cihazın ID'si 42 olsun.)*

## 4. Profili Yeni AP'ye Atama
Bu profil sadece Wi-Fi 7 destekli cihazlara (AirEngine 5776-26 gibi) atanmalıdır:
```bash
wlan
 ap-id 42
  # 5GHz Radyosu (Genellikle Radio 1)
  radio 1
   radio-5g-profile wifi7-test
   # (Gelen uyarıya 'y' ile onay verin)
  quit

  # Varsa 6GHz Radyosu (Genellikle Radio 2)
  radio 2
   radio-5g-profile wifi7-test
   quit
```

## 5. Sistem ve Protokol Denetleme (Kritik Adım)
Tüm AP'lerin hangi protokolde (ax mi be mi) çalıştığını tek bir tabloda görmek için şu komutu kullanın:

```bash
display wlan radio all
```

**Kontrol:** Bu tabloda, yeni eklediğiniz AP'nin karşısında **11be** yazdığını görmelisiniz. Diğer eski AP'lerinizin **11ax** olarak kalmaya devam ettiğini de buradan teyit edebilirsiniz.

## 6. Kayıt
Yaptığınız ayarların kalıcı olması için:
```bash
save
```

> **Not:** Web arayüzünde "Radio Type" kısmının boş görünmesi tamamen görsel bir durumdur; `display wlan radio all` çıktısında **11be** yazıyorsa Wi-Fi 7 hızından faydalanıyorsunuz demektir.
```
