---
layout: post
title: "FortiGate Admin Password Sıfırlama"
date: 2024-01-30
categories: firewall
---

FortiGate cihazımızın şifresini unuttuk veya sıfırlamamız gerekiyor. Bunun için aşağıdaki işlemleri sırasıyla gerçekleştirmemiz gerekiyor.

## Maintainer Modu Nedir?

Cihazımızın şifresini sıfırlayabilmemiz için **maintainer** modunda oturum açmamız gerekiyor. Bunun için kullanıcı adı olarak `maintainer` kullanırken, şifrede ise **seri numarasını** kullanacağız.

## Adım 1: Console Bağlantısı

Öncelikle cihazımıza bir **console kablosu** bağlıyoruz ve power-off durumundaki cihazımızı power-on durumuna getiriyoruz.

Cihazımız ilk açılmaya başladığında kendisiyle ilgili bilgileri ekrana basacaktır. Ekranda cihazın **seri numarasını** göreceğiz. Bu seri numarasını kenara not alıyoruz.

Örnek seri numarası:

FGT60D4234324234

## Adım 2: Şifreyi Hazırla

Seri numarasının başına bcpb ekliyoruz:

bcpbFGT60D4234324234

## Adım 3: Giriş Yap

Maintainer kullanıcı adını kullanarak giriş yapıyoruz:

Kullanıcı adı : maintainer
Şifre         : bcpbFGT60D4234324234

## ⚠️ Önemli Uyarılar

**1. Büyük/Küçük Harf:** Şifrede yazmış olduğumuz seri numarasında **küçük harf bulunmaması** gerekiyor, yoksa şifreyi kabul etmez.

**2. 14 Saniye Kuralı:** Cihaz açıldığından itibaren **14 saniye** gibi bir sürede giriş yapmanız gerekmektedir. Sonrasında şifreyi kabul etmeyecektir. Bunun için kullanıcı adı ve şifresini bir **not defterinde hazır** bulundurmanız iyi olacaktır. Direkt olarak kopyala yapıştır yaparak giriş sağlayabilirsiniz.

## Adım 4: Şifreyi Sıfırla

Giriş yaptıktan sonra admin şifresini sıfırlamak için aşağıdaki komutları giriyoruz:

config system admin
edit admin
set password YeniSifreniz123
end

Sonrasında **admin** kullanıcısıyla oluşturmuş olduğunuz yeni şifre ile giriş yapabilirsiniz.

## Özet

| Adım | İşlem |
|------|-------|
| 1 | Console kablosu bağla, cihazı aç |
| 2 | Seri numarasını not al |
| 3 | Seri numarasının başına bcpb ekle |
| 4 | 14 saniye içinde maintainer ile giriş yap |
| 5 | config system admin ile şifreyi değiştir |

> **İpucu:** Bu işlem fiziksel erişim gerektirir. Uzaktan yapılamaz. Bu yüzden FortiGate şifrenizi güvenli bir yerde saklayın.
