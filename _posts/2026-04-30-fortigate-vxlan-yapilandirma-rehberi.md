---
layout: post
title: "FortiGate VXLAN Konfigürasyonu"
date: 2024-01-30
categories: firewall
---

FortiGate firewall de yapılandıracağım konfigürasyonun web üzerinde karşılığı olmadığı izin işlemlerimi ilk olarak CLI konsol kullanarak yapılandıracağım. CLI konsolumu açıyorum ve yapılandırmama başlıyorum.

```bash
MERKEZ-40F # config system vxlan
MERKEZ-40F (vxlan) # edit vxlan35
new entry 'vxlan35' added
MERKEZ-40F (vxlan35) # set vni 35
MERKEZ-40F (vxlan35) # set interface wan
MERKEZ-40F (vxlan35) # set remote-ip x.x.x.x
MERKEZ-40F (vxlan35) # end

Wan portumu kontrol ettiğimde VXLAN35 arayüzümün oluştuğunu teyit ediyorum.

Sonraki adımda oluşturmuş olduğum VXLAN altında bir 35 id nolu vlan interface oluşturuyorum. 35 nolu vlan mını sanallaştırıp uzağa bölgeye taşıyacağım. Görüldüğü üzere interface oluşturuldu.

Sonraki adımda local network altında ilgili vlan ı oluşturuyorum. Bu adımalar da network ip bilgisi girmiyorum.

Sonraki adımda tekrar bir interface oluşturuyorum ve type olarak software switch seçiyorum. Bir önceki adımlarda oluşturmuş olduğum vlan ve vxlan interface seçip member ediyorum. Son olarak dhcp sunucumu açıp ok diyerek işlememi tamamlıyorum. Görüldüğü üzere software sw oluşturuldu.

Aynı işlemleri şubedeki farklı lokasyon 2. Firewall cihazımda da gerçekşetiriyorum. Görüldüğü üzere VXlan arayüz oluşturuldu.

Sonraki adımda yukarıdaki adımların aynısı gerçekleştiriyorum. Sadece virtual sw oluşturma kısmında ip ver network bilgisini değişiyorum.

Bağlantımı test ediyorum. Merkez cihazımdan Ping cevabım alındı. “diagnose sys vxlan fdb list vxlan35” komutu ile vni, port, remote ip ve mac aderslerimi görüyorum.

Hata ileri şekilde teyit etmek istediğimde listedeki mac adresinin merkez cihazımdaki firewall vxlan interface e ait olduğunu görüyorum.
mac=aa:a4:63:cf:4a:2a

Aynısını şube cihazımı ping lerek gerçekleştiriyorum. Ping e cevam aldım.

Hata ileri şekilde teyit etmek istediğimde listedeki mac adresinin merkez cihazımdaki firewall vxlan interface e ait olduğunu görüyorum.
mac=12:a7:22:98:91:5c
