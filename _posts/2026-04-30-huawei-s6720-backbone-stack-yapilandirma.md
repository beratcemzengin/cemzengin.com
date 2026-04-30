---
layout: post
title: "Huawei S6720 Switch Backbone Olarak Ayarlanması ve Stacking"
date: 2026-04-30
categories: network
---

Bu rehberde, iki adet Huawei S6720 switch'in backbone (omurga) olarak yapılandırılmasını, yedeklilik için stack yapısının kurulmasını ve VLAN/Trunk konfigürasyonlarını adım adım inceleyeceğiz.

## 1. Stack Yapısını Oluşturma

**Önemli Not:** Stack kurulumu her türlü konfigürasyondan önce yapılmalıdır. Çünkü stack moduna geçildiğinde switch üzerindeki mevcut tüm konfigürasyon silinir.



Bağlantı için her iki switch üzerindeki 40G'lik 1 ve 2 nolu portları kullanacağız. Kablolama mantığı şöyledir:
*   **Master Port 1** -> **Slave Port 2**
*   **Slave Port 1** -> **Master Port 2**

### Master Switch Yapılandırması:
```bash
system-view
interface stack-port 0/1
 port interface 40GE 0/0/1 enable
 y
interface stack-port 0/2
 port interface 40GE 0/0/2 enable
 y
```

### Slave Switch Yapılandırması:
Slave switch üzerinde slot numarasını değiştirmemiz gerekir:
```bash
system-view
stack slot 0 renumber 1
 y
interface stack-port 1/1
 port interface 40GE 1/0/1 enable
 y
interface stack-port 1/2
 port interface 40GE 1/0/2 enable
 y
```
Bu komutlardan sonra switchler yeniden başlayacaktır. Master switch **Slot 0**, Slave switch ise **Slot 1** olarak belirlenmiş olur.

### Stack Yapısını Kontrol Etme
Stack yapısının sağlıklı kurulduğunu aşağıdaki komutlarla teyit edebiliriz:
```bash
display stack current-configuration
display stack channel all
```
Bu komutla Master (0/0/x) ve Slave (1/0/x) portlarının birbirine nasıl eşleştiğini görebilirsiniz. Artık iki switch tek bir cihaz gibi yönetilecektir.

## 2. Temel Yapılandırma

Cihaz stack modunda açıldıktan sonra temel ayarları yapıyoruz:
*   **System Name:** BACKBONE
*   **Management IP:** 192.168.100.1
*   **Ek Ayarlar:** SSH Server, Time Zone ve Admin şifresi.

## 3. Backbone Üzerinde VLAN Tanımlama

Ağdaki trafiği ayırmak için gerekli VLAN'ları oluşturuyoruz:
```bash
[BACKBONE] vlan 1
[BACKBONE-vlan1] description MANAGEMENT_VLAN
[BACKBONE-vlan1] q

[BACKBONE] vlan 101
[BACKBONE-vlan101] description IDARE_101
[BACKBONE-vlan101] q

[BACKBONE] vlan 102
[BACKBONE-vlan102] description MUHASEBE_102
[BACKBONE-vlan102] q
```

## 4. Kenar Switchler İçin Trunk Yapılandırması

Kat switchlerinden gelen uplink bağlantıları için **Eth-Trunk** (Link Aggregation) oluşturuyoruz. Bu sayede hem Master hem de Slave switch üzerinden birer port kullanarak yedeklilik sağlıyoruz.



### 1. Kat Uplink Yapılandırması:
```bash
interface Eth-Trunk1
 description **** 1.KAT UPLINK ****
 port trunk allow-pass vlan 101 to 102
 q

# Fiziksel portları Trunk'a üye yapma
interface XGigabitEthernet0/0/1
 eth-trunk 1
 description **** 1.KAT UPLINK ****
 q
interface XGigabitEthernet1/0/1
 eth-trunk 1
 description **** 1.KAT UPLINK ****
 q
```

### 2. Kat Uplink Yapılandırması:
```bash
interface Eth-Trunk2
 description **** 2.KAT UPLINK ****
 port trunk allow-pass vlan 101 to 102
 q

interface XGigabitEthernet0/0/2
 eth-trunk 2
 description **** 2.KAT UPLINK ****
 q
interface XGigabitEthernet1/0/2
 eth-trunk 2
 description **** 2.KAT UPLINK ****
 q
```

## 5. Firewall Trunk Yapılandırması

Firewall yedekli yapısı (HA) için iki ayrı Eth-Trunk oluşturuyoruz:
```bash
# Master Firewall Bağlantısı
interface Eth-Trunk50
 description **** MASTER FIREWALL UPLINK ****
 port trunk allow-pass vlan 2 to 4094
 q

interface XGigabitEthernet0/0/23
 eth-trunk 50
 q
interface XGigabitEthernet1/0/23
 eth-trunk 50
 q

# Slave Firewall Bağlantısı
interface Eth-Trunk51
 description **** SLAVE FIREWALL UPLINK ****
 port trunk allow-pass vlan 2 to 4094
 q

interface XGigabitEthernet0/0/24
 eth-trunk 51
 q
interface XGigabitEthernet1/0/24
 eth-trunk 51
 q
```

## 6. Yönlendirme ve Kayıt

Tüm trafiğin Firewall üzerinden internete çıkması için gateway adresine bir static route giriyoruz:
```bash
[BACKBONE] ip route-static 0.0.0.0 0.0.0.0 192.168.100.254
```

Son olarak yaptığımız tüm işlemleri kaydediyoruz:
```bash
<BACKBONE> save all
```

**Sonuç:** Bu konfigürasyon ile yedekli bir backbone yapısı oluşturulmuştur. Firewall üzerinde ilgili VLAN interface'lerini ve kurallarını tanımladığınızda, ağ bölümleri arasındaki trafik güvenli bir şekilde akmaya başlayacaktır.
```</BACKBONE>
