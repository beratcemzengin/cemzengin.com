---
layout: post
title: "Huawei Switch-Router Temel Komutlar"
date: 2026-04-30
categories: network
---

Huawei switch ve router’larında bulunan işletim sistemi **VRP (Versatile Routing Platform)** olarak adlandırılır. Cihaz yönetiminde temelden başlamak ve işletim sisteminin mantığını kavramak, konfigürasyon sürecini çok daha verimli hale getirir.

## Huawei Cihazlarda Çalışma Modları

Huawei cihazlarda komutlar temel olarak iki farklı modda çalışır:

1.  **User-View Mode (`<Huawei>`):** Genellikle temel izleme, görüntüleme ve sınırlı ayarların yapıldığı moddur. Cihaza ilk bağlandığınızda bu modda başlarsınız.
2.  **System-View Mode (`[Huawei]`):** Cihazın genel yapılandırmasının, interface ayarlarının ve protokol tanımlamalarının yapıldığı kapsamlı moddur.

## Temel Navigasyon ve Yardımcı Komutlar

*   **`?` :** Kullanılabilir komutları listeler.
*   **`Tab` :** Komut tamamlamak için kullanılır.
*   **`Return` :** Direkt olarak User-view moduna geçiş yapar (Kısayol: `CTRL+Z`).
*   **`Quit` :** Bir önceki çalışma alanına döner.
*   **`Undo` :** Bir işlevi devre dışı bırakmak veya silmek için kullanılır (Cisco'daki `no` komutu ile aynıdır).
*   **`Sysname` :** Cihaza isim vermek için kullanılır.
*   **`Display` :** Görüntüleme komutudur. Parametre ile birlikte kullanılır (Örn: `display clock`).
*   **`Display This` :** Bulunduğunuz arayüz veya alandaki güncel yapılandırmayı gösterir.
*   **`Save` :** Çalışan konfigürasyonu başlangıç yapılandırmasına kaydeder.
*   **`Reset saved-configuration` :** Başlangıç yapılandırmasını sıfırlar.
*   **`Reboot` :** Cihazı yeniden başlatır.
*   **`Description` :** Interface veya VLAN’a açıklama eklemek için kullanılır.

---

## Huawei - Cisco Komut Karşılaştırma Tablosu

Cisco altyapısından gelenler için Huawei (VRP) karşılıklarını içeren hızlı referans tablosu:

| Cisco Komutu | Huawei (VRP) Karşılığı |
| :--- | :--- |
| `show interfaces` | `display interface` |
| `show ip route` | `display routing-table` |
| `show version` | `display version` |
| `show running-config` | `display current-configuration` |
| `show startup-config` | `display saved-configuration` |
| `configure terminal` | `system-view` |
| `exit` | `quit` |
| `end` | `return` |
| `write memory` | `save` |
| `write erase` | `reset saved-configuration` |
| `no [command]` | `undo [command]` |
| `hostname` | `sysname` |
| `show clock` | `display clock` |
| `show logging` | `display logbuffer` |
| `show users` | `display users` |
| `telnet` | `telnet` |
| `reload` | `reboot` |
| `shutdown` | `shutdown` |

---

Bu temel komutlar ve modlar arasındaki geçiş mantığı, Huawei ağ cihazlarını profesyonel bir şekilde yönetmenizin ilk adımıdır. İlerleyen yazılarda VLAN, Routing ve Güvenlik ayarlarının detaylarına değineceğiz.
```
