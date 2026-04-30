---
layout: post
title: "Temel Ruijie Switch Komutları"
date: 2026-04-30
categories: network
---

Ruijie ağ cihazları, endüstri standardı olan Cisco benzeri bir CLI yapısı kullanmaktadır. Bu yazımızda, Ruijie switchlerin temel yapılandırması için en çok kullanılan komutları kategorize edilmiş bir şekilde bulabilirsiniz.

## 1. Modlar Arası Geçiş ve Temel Ayarlar

Cihazın yönetim seviyeleri arasında geçiş yapmak ve temel tanımlamaları yapmak için kullanılır:

*   **Ayrıcalıklı Moda Geçiş:** `enable`
*   **Yapılandırma Moduna Giriş:** `configure terminal`
*   **Cihaz Adı Verme:** `hostname <Yeni_Cihaz_Adi>`
*   **Komut Tamamlama:** `Tab` tuşu kullanılır (Örn: `sh run<Tab>`)
*   **Konfigürasyon Görüntüleme:** `show running-config`

## 2. VLAN Yapılandırması

VLAN oluşturma, isimlendirme ve IP adresi atama işlemleri:
```bash
# VLAN Oluşturma ve İsimlendirme
SW1(config)# vlan 50
SW1(config-vlan)# name Camera
SW1(config-vlan)# exit

# VLAN'a Yönetim IP'si Atama
SW1(config)# interface vlan 1
SW1(config-if-VLAN 1)# ip address 172.16.16.2 255.255.255.0
SW1(config-if-VLAN 1)# exit
```

### VLAN Port Atama (Access Port)
Birden fazla portu aynı anda bir VLAN'a dahil etmek için `range` komutu kullanılır:
```bash
SW1(config)# interface range gigabitEthernet 0/1-10
SW1(config-if-range)# switchport mode access
SW1(config-if-range)# switchport access vlan 50
SW1(config-if-range)# exit
```

## 3. Uzaktan Yönetim ve Servisler

Cihaza Web arayüzü veya Telnet üzerinden erişim sağlamak için servislerin aktif edilmesi gerekir:

*   **Web Servisini Aktif Etme:** `enable service web-server all`
*   **Telnet Servisini Aktif Etme:** `enable service telnet-server`

### Konsol ve VTY Güvenliği (Şifre Koyma)
Cihaz erişimini yetkilendirmek için aşağıdaki adımlar takip edilir:
```bash
username admin secret Passw0rd
enable secret Passw0rd

line vty 0 4
 login local
```

## 4. İzleme ve Kontrol Komutları

Cihazın durumunu ve ağdaki diğer cihazları görmek için kullanılan izleme komutları:

*   **Tüm Portların Durumu:** `show interface status`
*   **MAC Adresi Tablosu:** `show mac-address-table`
*   **Belirli Bir MAC Adresini Sorgulama:** `sh mac-address-table dynamic address aaaa.bbbb.cccc.dddd`
*   **Komşu Cihazları Görme (LLDP):** `show lldp neighbors`

## 5. Gelişmiş Özellikler (GVRP ve PoE)

*   **VLAN'ları Tüm Ağa Dağıtma (GVRP):**
    ```bash
    gvrp enable
    gvrp dynamic-vlan-creation enable
    ```

*   **PoE (Power over Ethernet) Yönetimi:**
    *   PoE Aktif Etme: `poe enable`
    *   PoE Kapatma: `no poe enable`
    *   Portu Kapatma/Açma: `shutdown` / `no shutdown`

---

Bu temel komutlar, Ruijie switchlerin büyük bir bölümünde standart olarak çalışmaktadır. Yapılandırma bittikten sonra ayarların kalıcı olması için `write` veya `copy running-config startup-config` komutlarıyla kaydetmeyi unutmayın.
```
