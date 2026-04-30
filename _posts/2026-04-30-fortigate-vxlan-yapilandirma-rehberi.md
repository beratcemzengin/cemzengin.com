---
layout: post
title: "FortiGate VXLAN Yapılandırması: Adım Adım Rehber"
date: 2026-04-30
categories: firewall
---

FortiGate firewall cihazlarında yapılandıracağımız bazı konfigürasyonların web arayüzünde (GUI) karşılığı bulunmamaktadır[cite: 1]. Bu nedenle işlemlerimizi ilk olarak CLI konsolu kullanarak gerçekleştireceğiz[cite: 1]. CLI konsolumuzu açıyoruz ve yapılandırmaya başlıyoruz[cite: 1].

## 1. Adım: CLI ile VXLAN Arayüzü Oluşturma

Yapılandırmanın ilk adımında sanal tünel arayüzünü tanımlıyoruz[cite: 1]:
```bash
MERKEZ-40F # config system vxlan
MERKEZ-40F (vxlan) # edit vxlan35
# new entry 'vxlan35' added
MERKEZ-40F (vxlan35) # set vni 35
MERKEZ-40F (vxlan35) # set interface wan
MERKEZ-40F (vxlan35) # set remote-ip x.x.x.x  # Uzak cihazın Public IP adresi
MERKEZ-40F (vxlan35) # end
```

Wan portunu kontrol ettiğimizde **VXLAN35** arayüzünün oluştuğunu teyit ediyoruz[cite: 1].

## 2. Adım: VLAN Interface ve Sanallaştırma

Oluşturduğumuz VXLAN altında 35 ID nolu bir VLAN interface oluşturuyoruz[cite: 1]. Bu sayede 35 nolu VLAN'ımızı sanallaştırıp uzak bölgeye taşıyacağız[cite: 1]. Arayüzün başarıyla oluşturulduğunu kontrol ediyoruz[cite: 1].

Sonraki adımda lokal network altında ilgili VLAN'ı oluşturuyoruz[cite: 1]. Bu aşamada herhangi bir network IP bilgisi girmiyoruz[cite: 1].

## 3. Adım: Software Switch Yapılandırması

Tekrar bir interface oluşturuyoruz ve tip (type) olarak **Software Switch** seçiyoruz[cite: 1]. Bir önceki adımlarda hazırladığımız VLAN ve VXLAN arayüzlerini seçerek bu switch'e üye (member) yapıyoruz[cite: 1]. Son olarak DHCP sunucusunu aktif ederek işlemimizi tamamlıyoruz[cite: 1].

Yapılandırma sonunda Software Switch'in başarıyla oluşturulduğunu görüyoruz[cite: 1].

## 4. Adım: Şube Lokasyon Yapılandırması

Aynı işlemleri şubedeki farklı lokasyonda bulunan ikinci firewall cihazımızda da gerçekleştiriyoruz[cite: 1]. Şube tarafında da VXLAN arayüzünün oluştuğunu teyit ediyoruz[cite: 1].

Şube tarafındaki tek fark; Software Switch oluşturma kısmında IP ve network bilgisini lokasyona uygun şekilde güncelliyoruz[cite: 1].

## 5. Adım: Bağlantı Testi ve MAC Doğrulama

Bağlantıyı test etmek için merkez cihazından ping atıyoruz[cite: 1]. Ping cevabı alındıktan sonra aşağıdaki komutla durumu teyit ediyoruz[cite: 1]:
```bash
diagnose sys vxlan fdb list vxlan35
```

Bu komut ile VNI, port, remote IP ve MAC adreslerini görüyoruz[cite: 1].

### Kritik Kontrol ve Teyit
İleri seviye teyit işlemi için listedeki MAC adreslerini kontrol ediyoruz[cite: 1]. Örneğin; listedeki `aa:a4:63:cf:4a:2a` veya `12:a7:22:98:91:5c` gibi MAC adreslerinin, cihazlardaki firewall VXLAN interface'lerine ait olduğunu görerek trafiğin doğru tünel üzerinden geçtiğini doğruluyoruz[cite: 1].
```
