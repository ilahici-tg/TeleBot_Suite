"""
====================================================================
 🖥️ CYBER-OS TELEBOT SUITE v9.5 PRO
 Uzaktan Sistem Yönetimi, Ağ Analizi & Güvenlik Kontrol Paneli
====================================================================
"""

import os
import sys
import time
import platform
import subprocess
import ctypes
import json
import logging
import socket
import urllib.request
from io import BytesIO
from datetime import datetime

# Bağımlılık Tespiti ve Esnek Importlar
try:
    import psutil
except ImportError:
    psutil = None

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

try:
    import telebot
    from telebot import types
except ImportError:
    print("❌ HATA: 'pyTelegramBotAPI' kütüphanesi eksik! Yüklemek için: pip install pyTelegramBotAPI")
    sys.exit(1)

# Opsiyonel: OpenCV (Webcam) & Pyperclip (Pano)
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

# ==========================================
# 1. LOGGING VE KONFİGÜRASYON
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Token ve Admin ID yapılandırması (Çevre değişkenleri veya varsayılanlar)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "6036147688:AAFzq43Urq3ySRlHgSnYThrP3RPbcAY_hQ8")
ADMIN_ID_RAW = os.getenv("TELEGRAM_ADMIN_ID", "2094053613")

try:
    ADMIN_IDS = [int(i.strip()) for i in ADMIN_ID_RAW.split(",") if i.strip().isdigit()]
except Exception:
    ADMIN_IDS = [123456789]

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

def is_admin(user_id: int) -> bool:
    """Yalnızca yetkili Admin ID'lerine erişim izni verir."""
    return user_id in ADMIN_IDS

def log_security_alert(user):
    """Yetkisiz erişim denemelerini loglar ve uyarır."""
    logging.warning(f"⚠️ YETKİSİZ ERİŞİM DENEMESİ! User ID: {user.id}, Username: @{user.username}, Name: {user.first_name}")

# ==========================================
# 2. İNTERAKTİF MENÜ YÖNETİMİ (KEYBOARDS)
# ==========================================
def get_main_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_ss = types.InlineKeyboardButton("📸 Ekran Görüntüsü", callback_data="btn_ss")
    btn_sys = types.InlineKeyboardButton("📊 Sistem Durumu", callback_data="btn_sys")
    btn_cam = types.InlineKeyboardButton("📷 Kamera Görüntüsü", callback_data="btn_webcam")
    btn_proc = types.InlineKeyboardButton("⚙️ Çalışan Süreçler", callback_data="btn_processes")
    btn_net = types.InlineKeyboardButton("🌐 Ağ & Public IP", callback_data="btn_network")
    btn_clip = types.InlineKeyboardButton("📋 Pano (Clipboard)", callback_data="btn_clipboard")
    btn_power = types.InlineKeyboardButton("⚡ Güç Menüsü", callback_data="btn_power_menu")
    btn_cmd_help = types.InlineKeyboardButton("❓ Komut Listesi", callback_data="btn_cmd_help")

    markup.add(btn_ss, btn_sys)
    markup.add(btn_cam, btn_proc)
    markup.add(btn_net, btn_clip)
    markup.add(btn_power, btn_cmd_help)
    return markup

def get_power_keyboard() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_lock = types.InlineKeyboardButton("🔒 Ekranı Kilitle", callback_data="do_lock")
    btn_sleep = types.InlineKeyboardButton("🌙 Uyku Modu", callback_data="do_sleep")
    btn_restart = types.InlineKeyboardButton("🔄 Yeniden Başlat", callback_data="btn_restart_confirm")
    btn_shutdown = types.InlineKeyboardButton("🛑 Kapat", callback_data="btn_shutdown_confirm")
    btn_back = types.InlineKeyboardButton("◀️ Ana Menü", callback_data="btn_main")

    markup.add(btn_lock, btn_sleep)
    markup.add(btn_restart, btn_shutdown)
    markup.add(btn_back)
    return markup

def get_confirm_keyboard(action: str) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_yes = types.InlineKeyboardButton("✅ Evet, Uygula", callback_data=f"do_{action}")
    btn_no = types.InlineKeyboardButton("❌ İptal", callback_data="btn_power_menu")
    markup.add(btn_yes, btn_no)
    return markup

# ==========================================
# 3. SİSTEM & MEYDANA GELEN İŞLEMLER
# ==========================================
def take_screenshot() -> BytesIO:
    """Ekran görüntüsü alır (RAM içi PNG)."""
    if ImageGrab is None:
        return None
    screenshot = ImageGrab.grab()
    bio = BytesIO()
    bio.name = 'screenshot.png'
    screenshot.save(bio, 'PNG')
    bio.seek(0)
    return bio

def take_webcam_photo() -> BytesIO:
    """Kameradan anlık fotoğraf çeker."""
    if not HAS_CV2:
        return None
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    
    # BGR to RGB / Encoding
    _, buffer = cv2.imencode('.jpg', frame)
    bio = BytesIO(buffer.tobytes())
    bio.name = 'webcam.jpg'
    bio.seek(0)
    return bio

def get_detailed_system_info() -> str:
    """Sistem performans verilerini detaylı HTML döküm yapar."""
    uname = platform.uname()
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S") if psutil else "N/A"
    
    if psutil:
        cpu_pct = psutil.cpu_percent(interval=0.5)
        cpu_count = psutil.cpu_count(logical=True)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        ram_total_gb = round(ram.total / (1024**3), 2)
        ram_used_gb = round(ram.used / (1024**3), 2)
        disk_total_gb = round(disk.total / (1024**3), 2)
        disk_used_gb = round(disk.used / (1024**3), 2)
    else:
        cpu_pct = ram_total_gb = ram_used_gb = disk_total_gb = disk_used_gb = "N/A"
        ram = disk = type('obj', (object,), {'percent': 0})
        cpu_count = 1

    status_icon = "🟢" if (cpu_pct < 75 if isinstance(cpu_pct, (int, float)) else True) else "🔴"

    info = (
        f"{status_icon} <b>CYBER-OS SİSTEM RAPORU</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💻 <b>İşletim Sistemi:</b> {uname.system} {uname.release} ({uname.machine})\n"
        f"🏷️ <b>Cihaz Adı:</b> {uname.node}\n"
        f"⏰ <b>Açılış Zamanı:</b> {boot_time}\n\n"
        f"⚙️ <b>CPU Kullanımı:</b> %{cpu_pct} ({cpu_count} Çekirdek)\n"
        f"🧠 <b>RAM Kullanımı:</b> %{ram.percent} ({ram_used_gb} GB / {ram_total_gb} GB)\n"
        f"💾 <b>Ana Disk:</b> %{disk.percent} ({disk_used_gb} GB / {disk_total_gb} GB)\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📡 <b>Yerel IP:</b> {get_local_ip()}"
    )
    return info

def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_public_ip_info() -> str:
    """Public IP ve Coğrafi konum tespiti."""
    try:
        req = urllib.request.urlopen("http://ip-api.com/json/", timeout=5)
        data = json.loads(req.read().decode())
        if data.get("status") == "success":
            return (
                f"🌐 <b>PUBLIC IP BİLGİLERİ</b>\n\n"
                f"• <b>IP Adresi:</b> <code>{data.get('query')}</code>\n"
                f"• <b>Ülke / Şehir:</b> {data.get('country')} / {data.get('city')}\n"
                f"• <b>ISP / Servis Sağlayıcı:</b> {data.get('isp')}\n"
                f"• <b>Posta Kodu / Bölge:</b> {data.get('zip')} ({data.get('regionName')})"
            )
    except Exception as e:
        return f"⚠️ Public IP bilgisi alınamadı: {str(e)}"
    return "⚠️ Bilgi alınamadı."

def get_top_processes(limit: int = 8) -> str:
    """En çok RAM/CPU tüketen süreçlerin listesi."""
    if not psutil:
        return "psutil kütüphanesi eksik."
    
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    procs.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
    top_list = procs[:limit]

    output = "⚙️ <b>EN ÇOK KAYNAK TÜKETEN SÜREÇLER (RAM Top 8)</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
    for p in top_list:
        mem = round(p['memory_percent'] or 0, 1)
        name = p['name'][:20]
        output += f"• <code>PID {p['pid']:<6}</code> | <b>{name:<20}</b> | RAM: %{mem}\n"
    return output

# ==========================================
# 4. BOT KOMUT HANDLER'LARI
# ==========================================
@bot.message_handler(commands=['start', 'menu'])
def cmd_start(message):
    if not is_admin(message.from_user.id):
        log_security_alert(message.from_user)
        bot.reply_to(message, "⛔ <b>Erişim Engellendi:</b> Yetkisiz kullanıcı tespiti kaydedildi.")
        return

    welcome_msg = (
        f"🛡️ <b>CYBER-OS SYSTEM CONTROL SUITE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Hoş geldiniz, <b>{message.from_user.first_name}</b>!\n"
        f"Sistem hazır ve bağlantı aktif.\n\n"
        f"Hızlı işlemler için aşağıdaki menüyü kullanabilir veya <code>/help</code> yazabilirsiniz."
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=get_main_keyboard())

@bot.message_handler(commands=['help'])
def cmd_help(message):
    if not is_admin(message.from_user.id): return
    help_text = (
        f"📖 <b>KULLANILABİLİR KOMUT LİSTESİ</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"• <code>/start</code> - Ana kontrol menüsünü açar\n"
        f"• <code>/sysinfo</code> - Detaylı sistem performans dökümü\n"
        f"• <code>/ss</code> - Anlık ekran görüntüsü gönderir\n"
        f"• <code>/cam</code> - Kameradan fotoğraf çeker\n"
        f"• <code>/cmd <komut></code> - Uzaktan Shell/Terminal komutu çalıştırır\n"
        f"• <code>/ps</code> - Çalışan en yüksek RAM yüküne sahip süreçler\n"
        f"• <code>/kill <PID></code> - Belirtilen süreci sonlandırır\n"
        f"• <code>/ip</code> - Public IP ve ISP bilgilerini sorgular\n"
        f"• <code>/clip</code> - Pano (Clipboard) metnini okur\n"
        f"• <code>/setclip <metin></code> - Panoya metin yazar\n"
        f"• <code>/lock</code> - Ekranı kilitler\n"
        f"• <code>/download <dosya_yolu></code> - PC'den dosya indirir\n"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['sysinfo'])
def handle_sysinfo(message):
    if not is_admin(message.from_user.id): return
    bot.send_message(message.chat.id, get_detailed_system_info())

@bot.message_handler(commands=['ss'])
def handle_ss(message):
    if not is_admin(message.from_user.id): return
    msg = bot.send_message(message.chat.id, "📸 Ekran görüntüsü yakalanıyor...")
    photo = take_screenshot()
    if photo:
        bot.send_photo(message.chat.id, photo, caption="📸 Anlık Ekran Görüntüsü")
    else:
        bot.send_message(message.chat.id, "❌ Ekran görüntüsü alınamadı (Pillow kütüphanesi eksik).")
    bot.delete_message(message.chat.id, msg.message_id)

@bot.message_handler(commands=['cam'])
def handle_cam(message):
    if not is_admin(message.from_user.id): return
    msg = bot.send_message(message.chat.id, "📷 Kamera erişimi sağlanıyor...")
    photo = take_webcam_photo()
    if photo:
        bot.send_photo(message.chat.id, photo, caption="📷 Anlık Kamera Fotoğrafı")
    else:
        bot.send_message(message.chat.id, "❌ Kamera görüntüsü alınamadı (OpenCV yok veya kamera bağlı değil).")
    bot.delete_message(message.chat.id, msg.message_id)

@bot.message_handler(commands=['ps'])
def handle_ps(message):
    if not is_admin(message.from_user.id): return
    bot.send_message(message.chat.id, get_top_processes())

@bot.message_handler(commands=['kill'])
def handle_kill(message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ Kullanım: <code>/kill <PID></code> (Örn: <code>/kill 1234</code>)")
        return
    
    pid = int(args[1])
    try:
        p = psutil.Process(pid)
        name = p.name()
        p.terminate()
        bot.reply_to(message, f"✅ Süreç başarıyla sonlandırıldı: <b>{name}</b> (PID: {pid})")
    except Exception as e:
        bot.reply_to(message, f"❌ Süreç kapatılırken hata oluştu: <code>{str(e)}</code>")

@bot.message_handler(commands=['ip'])
def handle_ip(message):
    if not is_admin(message.from_user.id): return
    bot.send_message(message.chat.id, get_public_ip_info())

@bot.message_handler(commands=['clip'])
def handle_clip(message):
    if not is_admin(message.from_user.id): return
    if not HAS_PYPERCLIP:
        bot.reply_to(message, "⚠️ <code>pyperclip</code> kütüphanesi eksik.")
        return
    text = pyperclip.paste()
    if text:
        bot.send_message(message.chat.id, f"📋 <b>PANO İÇERİĞİ:</b>\n<code>{text[:3500]}</code>")
    else:
        bot.send_message(message.chat.id, "📋 Pano boş.")

@bot.message_handler(commands=['setclip'])
def handle_setclip(message):
    if not is_admin(message.from_user.id): return
    if not HAS_PYPERCLIP:
        bot.reply_to(message, "⚠️ <code>pyperclip</code> kütüphanesi eksik.")
        return
    text = message.text.replace("/setclip", "").strip()
    if not text:
        bot.reply_to(message, "⚠️ Kullanım: <code>/setclip Metin...</code>")
        return
    pyperclip.copy(text)
    bot.reply_to(message, "✅ Metin panoya yazıldı.")

@bot.message_handler(commands=['download'])
def handle_download(message):
    if not is_admin(message.from_user.id): return
    filepath = message.text.replace("/download", "").strip()
    if not filepath or not os.path.exists(filepath):
        bot.reply_to(message, "⚠️ Geçersiz veya bulunamayan dosya yolu!\nKullanım: <code>/download C:\\dosya.pdf</code>")
        return
    
    try:
        with open(filepath, 'rb') as f:
            bot.send_document(message.chat.id, f)
    except Exception as e:
        bot.reply_to(message, f"❌ Dosya gönderilemedi: <code>{str(e)}</code>")

@bot.message_handler(commands=['cmd'])
def handle_cmd(message):
    """Uzaktan Terminal / Command Prompt Komutu Çalıştırma"""
    if not is_admin(message.from_user.id): return
    
    command = message.text.replace("/cmd", "").strip()
    if not command:
        bot.reply_to(message, "⚠️ Lütfen çalıştırılacak komutu girin.\nÖrnek: <code>/cmd dir</code> veya <code>/cmd ipconfig</code>")
        return

    status_msg = bot.send_message(message.chat.id, "⚙️ Komut çalıştırılıyor...")
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=15)
        decoded = output.decode("utf-8", errors="ignore")
        if not decoded.strip():
            decoded = "(Komut başarıyla çalıştı, çıktı üretilmedi.)"
        if len(decoded) > 3800:
            decoded = decoded[:3800] + "\n... [Çıktı kırpıldı]"
        bot.edit_message_text(f"<b>⚙️ Komut:</b> <code>{command}</code>\n\n<b>Çıktı:</b>\n<code>{decoded}</code>", message.chat.id, status_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ <b>Hata Oluştu:</b>\n<code>{str(e)}</code>", message.chat.id, status_msg.message_id)

# ==========================================
# 5. INLINE CALLBACK YÖNETİMİ
# ==========================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⛔ Yetkisiz erişim!", show_alert=True)
        return

    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data

    if data == "btn_main":
        bot.edit_message_text("🖥️ <b>CYBER-OS SİSTEM KONTROL PANENLİ</b>", chat_id, msg_id, reply_markup=get_main_keyboard())

    elif data == "btn_ss":
        bot.answer_callback_query(call.id, "Ekran görüntüsü alınıyor...")
        photo = take_screenshot()
        if photo:
            bot.send_photo(chat_id, photo, caption="📸 Ekran Görüntüsü")
        else:
            bot.send_message(chat_id, "❌ Ekran görüntüsü alınamadı.")

    elif data == "btn_webcam":
        bot.answer_callback_query(call.id, "Kamera yakalanıyor...")
        photo = take_webcam_photo()
        if photo:
            bot.send_photo(chat_id, photo, caption="📷 Kamera Görüntüsü")
        else:
            bot.send_message(chat_id, "❌ Kamera görüntüsü alınamadı (kamera kapalı veya cv2 kütüphanesi yok).")

    elif data == "btn_sys":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, get_detailed_system_info())

    elif data == "btn_processes":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, get_top_processes())

    elif data == "btn_network":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, get_public_ip_info())

    elif data == "btn_clipboard":
        bot.answer_callback_query(call.id)
        if HAS_PYPERCLIP:
            txt = pyperclip.paste()
            bot.send_message(chat_id, f"📋 <b>Pano İçeriği:</b>\n<code>{txt[:3000]}</code>" if txt else "📋 Pano boş.")
        else:
            bot.send_message(chat_id, "⚠️ `pyperclip` yüklü değil.")

    elif data == "btn_power_menu":
        bot.edit_message_text("⚡ <b>Güç & Sistem Yönetimi</b>", chat_id, msg_id, reply_markup=get_power_keyboard())

    elif data == "btn_cmd_help":
        bot.answer_callback_query(call.id)
        cmd_help(call.message)

    elif data == "do_lock":
        bot.answer_callback_query(call.id, "Ekran kilitleniyor...", show_alert=True)
        if platform.system() == "Windows":
            ctypes.windll.user32.LockWorkStation()
        elif platform.system() == "Darwin":
            subprocess.run(["pmset", "displaysleepnow"])
        else:
            subprocess.run(["xdg-screensaver", "lock"])

    elif data == "do_sleep":
        bot.answer_callback_query(call.id, "Sistem uyku moduna geçiyor...", show_alert=True)
        if platform.system() == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif data == "btn_shutdown_confirm":
        bot.edit_message_text("⚠️ <b>Bilgisayar kapatılacak! Emin misiniz?</b>", chat_id, msg_id, reply_markup=get_confirm_keyboard("shutdown"))

    elif data == "btn_restart_confirm":
        bot.edit_message_text("⚠️ <b>Bilgisayar yeniden başlatılacak! Emin misiniz?</b>", chat_id, msg_id, reply_markup=get_confirm_keyboard("restart"))

    elif data == "do_shutdown":
        bot.answer_callback_query(call.id, "Kapatma başlatıldı...", show_alert=True)
        if platform.system() == "Windows":
            os.system("shutdown /s /t 10")
        else:
            os.system("shutdown -h now")

    elif data == "do_restart":
        bot.answer_callback_query(call.id, "Yeniden başlatma başlatıldı...", show_alert=True)
        if platform.system() == "Windows":
            os.system("shutdown /r /t 10")
        else:
            os.system("reboot")

# ==========================================
# 6. BAŞLATMA DÖNGÜSÜ & BOT MENÜSÜ AYARI
# ==========================================
def setup_bot_commands():
    """Telegram mobil/masaüstü istemcisinde çıkan komut menüsünü ayarlar."""
    commands = [
        types.BotCommand("start", "Ana kontrol paneli menüsü"),
        types.BotCommand("sysinfo", "Detaylı sistem raporu"),
        types.BotCommand("ss", "Ekran görüntüsü al"),
        types.BotCommand("cam", "Webcam fotoğrafı çek"),
        types.BotCommand("cmd", "Terminal komutu çalıştır"),
        types.BotCommand("ps", "Çalışan süreçleri listele (RAM top)"),
        types.BotCommand("ip", "Public IP ve ağ detayları"),
        types.BotCommand("clip", "Pano metnini oku"),
        types.BotCommand("download", "Bilgisayardan dosya indir"),
        types.BotCommand("help", "Tüm komutları listele"),
    ]
    try:
        bot.set_my_commands(commands)
    except Exception as e:
        logging.warning(f"Bot komut menüsü ayarlanamadı: {e}")

if __name__ == "__main__":
    print("==========================================")
    print(" 🚀 CYBER-OS TELEBOT SUITE v9.5 PRO STARTING")
    print("==========================================")
    setup_bot_commands()
    print("🟢 Bot dinlemede... Ctrl+C ile durdurabilirsiniz.")
    
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except KeyboardInterrupt:
        print("\n🛑 Bot durduruldu.")
    except Exception as e:
        logging.error(f"Kritik çalışma hatası: {e}")