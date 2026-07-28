<div align="center">

# 🖥️ CYBER-OS TELEBOT SUITE v9.5 PRO

[![License: MIT](https://img.shields.io/badge/License-MIT-00f3ff.svg?style=for-the-badge)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-ff0055.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform: Cross--Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-9d00ff.svg?style=for-the-badge)](#)
[![Security: Auth--Protected](https://img.shields.io/badge/Security-Multi--Admin%20Protected-00ff41.svg?style=for-the-badge)](#)

<p align="center">
  <b>Python ve Telegram Bot API ile Uzaktan Sistem Yönetimi, Ağ Analizi & Güvenlik Kontrol Paneli</b>
</p>

[⚡ Özellikler](#-özellikler) • [📦 Adım Adım Kurulum Rehberi](#-adım-adım-kurulum-rehberi) • [🚀 Çalıştırma](#-çalıştırma) • [📖 Komut Referansı](#-komut-referansı) • [🛡️ Güvenlik](#️-güvenlik) • [⚠️ Yasal Uyarı](#️-yasal-uyarı--sorumluluk-reddi) • [🤝 Katkıda Bulunma](#-katkıda-bulunma) • [📝 Lisans](#-lisans)

---

</div>

## 📌 Proje Hakkında

**TeleBot Suite v9.5 Pro**, bilgisayarınızı Telegram üzerinden uzaktan güvenli ve interaktif bir şekilde yönetmenizi sağlayan gelişmiş bir Python otomasyon aracıdır.

Sadece yetkilendirilmiş Telegram kullanıcılarının erişebildiği bu sistem; anlık sistem performans raporlaması, süreç yöneticisi, ekran ve webcam görüntüsü yakalama, pano (clipboard) kontrolü ve uzaktan terminal komut çalıştırma gibi kritik işlevleri tek bir arayüzde sunar.

---

## ⚡ Özellikler

### 📊 1. Sistem İzleme & Kaynak Analizi
- **Canlı Performans Raporu:** CPU yükü, RAM kullanımı, Disk alanı, Açılış zamanı (Boot Time) ve Sistem metrikleri.
- **Süreç Yöneticisi (Process Manager):** En çok bellek (RAM) tüketen süreçleri listeleme ve istenen süreci PID ile sonlandırma (`/kill`).
- **Ağ Bilgisi:** Yerel IP ve Public IP, İSS (ISP) ve coğrafi konum bilgisi sorgulama.

### 📸 2. Multimedya & Yakalama Araçları
- **RAM İçi Ekran Görüntüsü (`/ss`):** Disk üzerinde geçici dosya oluşturmadan doğrudan bellekten Telegram'a anlık ekran görüntüsü aktarımı.
- **Webcam Fotoğrafı (`/cam`):** Bağlı web kamerasından anlık fotoğraf yakalama.

### 📋 3. Pano & Dosya İşlemleri
- **Pano (Clipboard) Yönetimi:** Masaüstü panosundaki metni okuma ve uzaktan panoya metin atama.
- **Uzaktan Dosya İndirme:** Bilgisayardaki istenen herhangi bir dosyayı Telegram sohbetine döküman olarak aktarma.
- **Terminal Komut Çalıştırıcı (`/cmd`):** Uzaktan Shell/Command Prompt komutları çalıştırma ve çıktısını canlı alma.

### ⚡ 4. Güç & Sistem Durumu
- Ekran Kilitleme (Lock WorkStation).
- Uyku Moduna Geçirme (Sleep Mode).
- Çift Aşamalı Onay Mekanizmalı Kapatma (Shutdown) ve Yeniden Başlatma (Restart).

---

## 📦 Adım Adım Kurulum Rehberi

### 1️⃣ Ön Gereksinimler
- Bilgisayarınızda **Python 3.10** veya üzeri bir sürümün yüklü olduğundan emin olun.
- Bir Telegram hesabına sahip olun.

---

### 2️⃣ Repoyu Klonlayın veya İndirin
Projeyi bilgisayarınıza indirin ve dizine gidin:

```bash
git clone https://github.com/ilahici-tg/Telebot_Suite
cd s-main
```

---

### 3️⃣ Gerekli Python Kütüphanelerini Yükleyin
Projenin ihtiyaç duyduğu bağımlılıkları `pip` paket yöneticisi ile kurun:

```bash
pip install pyTelegramBotAPI psutil Pillow
```

*(Opsiyonel)* Webcam fotoğrafı çekme ve masaüstü panosunu yönetmek istiyorsanız aşağıdaki kütüphaneleri de ekleyin:
```bash
pip install opencv-python pyperclip
```

---

### 4️⃣ Telegram Bot Token ve Kullanıcı ID'nizi Alın

1. Telegram'da **[@BotFather](https://t.me/BotFather)** ile iletişim başlatın.
2. `/newbot` komutunu gönderin ve botunuza bir isim ve kullanıcı adı belirleyin.
3. BotFather'ın size verdiği **HTTP API Token** değerini kopyalayın (Örn: `7896541230:AAEk...`).
4. Kendi Telegram Kullanıcı ID'nizi öğrenmek için **[@userinfobot](https://t.me/userinfobot)** botuna mesaj atın (Örn: `123456789`).

---

### 5️⃣ Çevre Değişkenlerini (Environment Variables) Tanımlayın

Güvenlik amacıyla Bot Token ve Admin ID bilgilerinizi ortam değişkeni olarak ekleyin:

#### 🔹 Windows (CMD):
```cmd
set TELEGRAM_BOT_TOKEN="SENIN_TELEGRAM_BOT_TOKENIN"
set TELEGRAM_ADMIN_ID="SENIN_TELEGRAM_USER_IDN"
```

#### 🔹 Windows (PowerShell):
```powershell
$env:TELEGRAM_BOT_TOKEN="SENIN_TELEGRAM_BOT_TOKENIN"
$env:TELEGRAM_ADMIN_ID="SENIN_TELEGRAM_USER_IDN"
```

#### 🔹 Linux / macOS:
```bash
export TELEGRAM_BOT_TOKEN="SENIN_TELEGRAM_BOT_TOKENIN"
export TELEGRAM_ADMIN_ID="SENIN_TELEGRAM_USER_IDN"
```

*(Alternatif olarak `TeleBot_Suite.py` içerisindeki `BOT_TOKEN` ve `ADMIN_ID_RAW` satırlarına doğrudan bilgilerinizi yazabilirsiniz.)*

---

## 🚀 Çalıştırma

Kurulum adımlarını tamamladıktan sonra betiği çalıştırın:

```bash
python TeleBot_Suite.py
```

Bot çalıştığında Telegram sohbetinizde `/start` yazarak kontrol panelini başlatabilirsiniz.

---

## 📖 Komut Referansı

| Komut | Açıklama |
|---|---|
| `/start` | Ana interaktif inline kontrol panelini açar |
| `/sysinfo` | Detaylı sistem performans ve kaynak raporu sunar |
| `/ss` | Anlık ekran görüntüsü alır ve gönderir |
| `/cam` | Web kamerasından anlık fotoğraf çeker |
| `/ps` | En çok RAM tüketen süreçleri listeler |
| `/kill <PID>` | Belirtilen süreç ID'sini (PID) sonlandırır |
| `/ip` | Dış IP (Public IP) ve konum bilgilerini getirir |
| `/clip` | Masaüstü panosundaki metni okur |
| `/setclip <metin>` | Belirtilen metni masaüstü panosuna kopyalar |
| `/download <yol>` | Belirtilen yoldaki dosyayı Telegram'a indirir |
| `/cmd <komut>` | Terminal komut satırını çalıştırır |
| `/help` | Tüm kullanılabilir komut listesini gösterir |

---

## 🛡️ Güvenlik

- **Yetkisiz Erişim Koruması:** Bot sadece tanımlanan `TELEGRAM_ADMIN_ID` kullanıcılarına yanıt verir. Yetkisiz bir kullanıcı mesaj attığında erişim engellenir ve konsola güvenlik alarmı kaydedilir.
- **Bellek İçi İşlem:** Ekran görüntüleri diske yazılmadan bellek (RAM) üzerinde işlenip temizlenir.

---

## ⚠️ Yasal Uyarı & Sorumluluk Reddi

> **ÖNEMLİ:** Bu araç yalnızca kişisel sistem yönetimi, meşru otomasyon ve eğitim amaçlarıyla geliştirilmiştir. İzinsiz sistemlerde veya yetkisiz erişim amacıyla kullanılması yasadışıdır. Kullanıcı, uygulamanın kullanımından doğabilecek tüm hukuki ve cezai sorumlulukları kendisi üstlenir.

---

## 🤝 Katkıda Bulunma

Projeye katkıda bulunmak isterseniz adımları takip edebilirsiniz:

1. Bu depoyu çatallayın (Fork edin).
2. Yeni bir özellik dalı oluşturun (`git checkout -b feature/YeniOzellik`).
3. Değişikliklerinizi işleyin (`git commit -m 'feat: Yeni özellik eklendi'`).
4. Dalınıza itin (`git push origin feature/YeniOzellik`).
5. Bir Çekme İsteği (Pull Request) başlatın.

---

## 📝 Lisans

Bu proje **[MIT Lisansı](LICENSE)** ile lisanslanmıştır. Detaylar için `LICENSE` dosyasına göz atabilirsiniz.

---

<div align="center">

<b>Developed with 💻 & ⚡ by <a href="https://github.com/ilahici-tg">Yusuf Balcı</a></b>

</div>
