---
layout: post
title: "FortiGate VXLAN Yapılandırması: Adım Adım Rehber"
date: 2026-04-30
categories: firewall
---

FortiGate firewall cihazlarında bazı gelişmiş yapılandırmaların web arayüzünde (GUI) tam karşılığı bulunmayabilir. VXLAN (Virtual Extensible LAN) yapılandırması da bu durumlardan biridir. Bu rehberde, Layer 2 trafiği uzak bir bölgeye taşımak için CLI ve GUI kullanarak VXLAN kurulumunu gerçekleştireceğiz.

## 1. Adım: CLI ile VXLAN Arayüzü Oluşturma

Yapılandırmanın ilk adımını CLI konsolu üzerinden başlatıyoruz. Bu işlemle sanal tünel arayüzünü tanımlayacağız.
```bash
MERKEZ-40F # config system vxlan
MERKEZ-40F (vxlan) # edit vxlan35
# new entry 'vxlan35' added
MERKEZ-40F (vxlan35) # set vni 35
MERKEZ-40F (vxlan35) # set interface wan
MERKEZ-40F (vxlan35) # set remote-ip x.x.x.x  # Uzak cihazın Public IP adresi
MERKEZ-40F (vxlan35) # end
