---
layout: post
title: "Huawei S7706 Wi-Fi 7 (802.11be) AP Kurulum Rehberi"
date: 2026-04-30
categories: network
---

Huawei AP Controller özellikli switchlerde, firmware güncellemesi yapılsa dahi bazen web arayüzünde Wi-Fi 7 (802.11be) protokolü seçenekler arasında görünmeyebilir. Bu gibi durumlarda, yeni nesil AirEngine serisi AP'leri tam performansıyla çalıştırmak için CLI üzerinden müdahale etmek gerekir.

## 1. Hazırlık ve Kontrol

Yeni cihazı bağlamadan önce altyapının yazılımsal gereksinimleri karşıladığından emin olun:

*   **Versiyon:** En az **V200R024** ana sürümü ve **SPH180** (veya üstü) yaması yüklü olmalıdır.
*   **Lisans:** Mevcut AP kapasitenizi `display license` komutuyla kontrol edin.

## 2. Wi-Fi 7 Radyo Profili Oluşturma

Web arayüzünde "Radio Type" kısmında Wi-Fi 7 seçeneği çıkmadığı durumlarda bu işlemi bir kez CLI'dan yapmanız yeterlidir:
```bash
system-view
wlan
# Wi-Fi 7 destekli 5GHz profili oluşturma
radio-5g-profile name wifi7-test
 radio-type dot11be
 quit
