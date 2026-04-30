---
layout: post
title: "Cisco Switch ve Router Üzerinde SSH Yapılandırması"
date: 2026-04-30
categories: network
---

## Genel Bakış

Bir ağ yöneticisi, normalde masasında oturarak uzaktaki ağ cihazlarına SSH ile bağlanarak çalışır[cite: 1]. Bunun mümkün olmadığı bazı durumlarda da cihazın yanına giderek console ile bağlanıp işlem yapmak durumunda kalır[cite: 1]. Bu yazımızda Cisco router ve switch üzerinde SSH yapılandırmasının nasıl yapılacağı anlatılacaktır[cite: 1].

### Başlarken

Yapılandırmaya başlamadan önce şu iki şartın sağlandığını varsayalım:
*   Router veya switch üzerinde IP adresi yapılandırmasını yaptınız[cite: 1].
*   Cihaza doğrudan konsol (console) erişiminiz bulunuyor[cite: 1].

---

## SSH Uzaktan Yönetim Yapılandırması

### 1. Kullanıcı ve Enable Parolası Oluşturma
Cisco cihazımıza giriş yapıp bir kullanıcı oluşturarak ve yetki seviyesini belirleyerek başlıyoruz[cite: 1]:
```bash
conf t
username netadmin privilege 15 secret 1111
enable secret 2222
```

Parolaların konfigürasyon dosyasında açık metin olarak görünmemesi için şifrelemeyi aktif hale getiriyoruz[cite: 1]:
```bash
service password-encryption
```

### 2. Domain Name ve RSA Anahtarı Oluşturma
SSH'in çalışabilmesi için bir alan adı tanımlanması ve ardından kriptografik anahtarların oluşturulması gerekir[cite: 1]. Güvenlik için 2048 bitlik anahtar seçiyoruz[cite: 1]:
```bash
ip domain-name cemzengin.com.tr
crypto key generate rsa
```
*(Key modulus boyutu sorulduğunda **2048** giriniz.)*

### 3. VTY Hatlarını Düzenleme
Sanal terminalleri (VTY) sadece SSH bağlantısına izin verecek şekilde yapılandırıp Telnet'i devre dışı bırakıyoruz[cite: 1]:
```bash
line vty 0 4
 login local
 transport input ssh
 exit
```

### 4. SSH Versiyon ve Güvenlik Ayarları
SSH versiyonunun güncel ve güvenli olan 2.0 sürümü olduğundan emin oluyoruz[cite: 1]:
```bash
ip ssh version 2
```

Güvenlik seviyesini artırmak için erişim yapabilecek IP adreslerini bir Access List (ACL) ile sınırlıyoruz ve boşta kalma süresini (timeout) belirliyoruz[cite: 1]:
```bash
ip access-list standard ACL-SSH
 permit 192.168.95.0 0.0.0.255
 exit

line vty 0 4
 access-class ACL-SSH in
 exec-timeout 5
 exit
```

### 5. AAA Servisini Etkinleştirme
Cihaza her girişte kimlik doğrulama süreçlerini yönetmek için AAA hizmetini aktif ediyoruz[cite: 1]:
```bash
aaa new-model
```

---

## SSH Bağlantısını Test Etme

Yapılandırma tamamlandıktan sonra Putty (veya benzeri bir SSH istemcisi) kullanarak cihazın IP adresine bağlanmayı deneyebilirsiniz[cite: 1].

Bağlantının detaylarını kontrol etmek için şu komutu kullanabilirsiniz:
```bash
show ip ssh
```
Bu komut sonucunda **"SSH Enabled – version 2.0"** ifadesini görmeniz, yapılandırmanın başarıyla tamamlandığını gösterir[cite: 1].
```
