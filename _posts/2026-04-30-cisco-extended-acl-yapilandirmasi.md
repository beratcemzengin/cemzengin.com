---
layout: post
title: "Cisco Extended ACL Yapılandırması"
date: 2026-04-30
categories: network
---

Merhaba arkadaşlar, bu yazımızda standart ACL yapılandırmasının bir üst seviyesi olan **Extended (Genişletilmiş) ACL** yapılandırmasını inceleyeceğiz. Konuyu daha iyi kavrayabilmek için pratik bir senaryo üzerinden ilerleyeceğiz.

## Extended ACL Nedir?

Extended ACL, standart ACL yapılandırmasından farklı olarak sadece kaynak IP adresine değil, **hem kaynak hem de hedef IP adresine** bakar. Ayrıca protokol bazlı (TCP, UDP, ICMP vb.) kısıtlamalar yapmamıza olanak sağlar.

*   **Numara Aralığı:** 100-199 arasıdır.
*   **Esneklik:** Port numaraları (80, 443, 21 vb.) üzerinden detaylı filtreleme yapılabilir.



## Uygulama Senaryosu

Senaryomuzda şu kısıtlamaları gerçekleştireceğiz:
1.  `192.168.1.2` IP adresine sahip cihaz server'a **FTP** yapabilsin.
2.  Diğer tüm cihazlar server'a FTP yapamasın ancak **Ping** atabilsin.

Extended ACL kuralları, standart ACL'in aksine hedefe değil **kaynağa en yakın router** üzerinde yazılır. Bu yüzden Router0 üzerinde işlem yapacağız.

### 1. Adım: FTP İzni ve Kısıtlamaları

Öncelikle özel olarak izin vereceğimiz host için kuralımızı yazıyoruz. FTP için port numarası olan `21`'i de kullanabiliriz:
```bash
Router0> enable
Router0# configure terminal
# Özel host için FTP izni
Router0(config)# access-list 110 permit tcp host 192.168.1.2 host 192.168.10.2 eq ftp
```

Şimdi diğer networklerin FTP erişimini kapatıyoruz:

```bash
# 1.0 ve 2.0 networkleri için FTP yasaklama
Router0(config)# access-list 110 deny tcp 192.168.1.0 0.0.0.255 host 192.168.10.2 eq ftp
Router0(config)# access-list 110 deny tcp 192.168.2.0 0.0.0.255 host 192.168.10.2 eq ftp
```

### 2. Adım: Ping (ICMP) İzni

Diğer tüm cihazların server'a ping atabilmesi için ICMP protokolüne izin veriyoruz. Burada kullandığımız `any any` ifadesi "herhangi bir kaynaktan herhangi bir hedefe" anlamına gelir:
```bash
Router0(config)# access-list 110 permit icmp any any
```

### 3. Adım: ACL'i Arayüze Uygulama

Yazdığımız listelerin aktif olması için ilgili portlara tanımlamamız gerekir. Trafiğin router'a girdiği yönü baz alarak `in` yönüne uyguluyoruz:
```bash
Router0(config)# interface fastEthernet 0/0
Router0(config-if)# ip access-group 110 in

Router0(config)# interface fastEthernet 0/1
Router0(config-if)# ip access-group 110 in
```

## Kontrol ve Doğrulama

Yapılandırmayı tamamladıktan sonra cihazlar üzerinden testlerinizi yapabilirsiniz. Sadece `192.168.1.2` adresli cihaz FTP yapabilecek, ancak tüm cihazlar birbirine ping atabilecektir.

Yazdığınız Access-List kurallarını ve eşleşme (match) durumlarını görmek için şu komutu kullanabilirsiniz:
```bash
Router0# show access-lists
```

Bu rehberle birlikte Extended ACL kullanarak ağ trafiği üzerinde nasıl daha hassas bir denetim kurabileceğinizi görmüş olduk. Bir sonraki yazımızda görüşmek üzere!
```
