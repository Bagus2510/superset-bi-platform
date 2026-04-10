# =========================================================================================
# FILE KONFIGURASI UTAMA APACHE SUPERSET
# =========================================================================================

# Modul 'os' adalah bawaan Python. 
# Perannya: Berkomunikasi dengan sistem operasi tempat Docker berjalan untuk mengambil 
# nilai-nilai rahasia (seperti password) dari file .env atau GitLab CI/CD Variables.
import os


# Peran: Mengubah string environment variable menjadi nilai boolean.
# Contoh yang dianggap True: 1, true, yes, on.
def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# Peran: Mengubah daftar domain berbasis CSV menjadi list Python.
# Contoh input: "https://a.com,https://b.com".
def _csv_to_list(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


# Peran: Mengubah string environment variable menjadi integer dengan fallback aman.
# Kegunaan: Menjaga aplikasi tetap jalan saat nilai env kosong atau tidak valid.
def _to_int(value: str, default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default

# -----------------------------------------------------------------------------------------
# 1. KONFIGURASI KEAMANAN & DATABASE UTAMA
# -----------------------------------------------------------------------------------------

# Peran: Memberitahu Superset di mana letak database utama (PostgreSQL) untuk menyimpan 
# metadata (seperti daftar user, pengaturan chart, dan hak akses).
# Mengapa pakai os.getenv? Agar password tidak tertulis langsung di file ini.
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

# Peran: Kunci rahasia untuk mengenkripsi sesi login user dan password database eksternal.
# Syarat: Harus string acak yang sangat panjang.
SUPERSET_SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

# Peran: Membuat Superset memahami header dari reverse proxy (Nginx/Traefik/Ingress).
# Penjelasan: Wajib untuk deployment production agar URL, skema HTTPS, dan cookie
# tidak salah terbaca saat TLS terminasi terjadi di proxy.
ENABLE_PROXY_FIX = _to_bool(os.getenv("ENABLE_PROXY_FIX"), default=True)
PROXY_FIX_CONFIG = {
    "x_for": 1,
    "x_proto": 1,
    "x_host": 1,
    "x_port": 1,
    "x_prefix": 1,
}


# -----------------------------------------------------------------------------------------
# 2. KONFIGURASI EMBEDDING (MENANAMKAN DASHBOARD KE WEBSITE LAIN)
# -----------------------------------------------------------------------------------------

# Peran: Kunci rahasia khusus untuk membuat "Guest Token". 
# Penjelasan: Saat website kita ingin menampilkan dashboard, website kita akan meminta 
# izin (token) ke Superset menggunakan kunci rahasia ini, sehingga pengunjung website 
# tidak perlu repot-repot login manual ke Superset.
GUEST_TOKEN_JWT_SECRET = os.getenv("GUEST_TOKEN_JWT_SECRET")
if not GUEST_TOKEN_JWT_SECRET:
    raise RuntimeError("GUEST_TOKEN_JWT_SECRET is required for deployment")

# Peran: Mengatur sifat Cookie di browser (seperti Chrome/Safari).
# Penjelasan: Browser modern sangat ketat. Agar Superset bisa berjalan di dalam "Iframe" 
# pada website domain lain, Cookie harus diset 'None' (lintas domain) dan 'Secure' (wajib HTTPS).
SESSION_COOKIE_SAMESITE = 'None'

# Peran: Menentukan nama cookie sesi agar konsisten lintas deployment.
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "superset_session")

# Peran: Membatasi domain cookie jika Superset berjalan pada subdomain tertentu.
# Catatan: Biarkan kosong jika tidak butuh domain cookie custom.
SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN") or None

# Peran: Mencegah cookie sesi diakses oleh JavaScript (mitigasi XSS).
SESSION_COOKIE_HTTPONLY = True

# Peran: Memastikan cookie hanya dikirim lewat HTTPS bila diaktifkan.
SESSION_COOKIE_SECURE = _to_bool(os.getenv("SESSION_COOKIE_SECURE"), default=True)

# Peran: Menentukan tujuan redirect setelah proses logout.
LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", "/login/")

# Peran: Mematikan sistem keamanan bawaan Superset (Talisman) yang sifatnya memblokir Iframe.
# Penjelasan: Secara default, aplikasi web menolak dimasukkan ke Iframe untuk mencegah 
# serangan peretasan (Clickjacking). Karena kita memang sengaja ingin meng-embed, 
# kita harus mengizinkannya secara eksplisit (ALLOWALL).
HTTP_HEADERS = {'X-Frame-Options': 'ALLOWALL'}
TALISMAN_ENABLED = False 

# Peran: Cross-Origin Resource Sharing (CORS).
# Penjelasan: Mengizinkan server website utama kita (misal: React/Next.js) untuk saling 
# bertukar data atau API dengan server Superset ini meskipun alamat IP/Domain-nya berbeda.
# Catatan: CORS hanya diaktifkan jika daftar origin tidak kosong.
ALLOWED_CORS_ORIGINS = _csv_to_list(os.getenv("ALLOWED_CORS_ORIGINS"))
ENABLE_CORS = bool(ALLOWED_CORS_ORIGINS)
CORS_OPTIONS = {
    'supports_credentials': True, # Mengizinkan pengiriman cookie/token
    'allow_headers': ['*'],       # Mengizinkan semua jenis header API
    'resources': ['*'],           # Mengizinkan akses ke semua rute API Superset
    'origins': ALLOWED_CORS_ORIGINS
}


# -----------------------------------------------------------------------------------------
# 3. KONFIGURASI PERFORMA (CACHING)
# -----------------------------------------------------------------------------------------

# Peran: Mengatur sistem memori sementara (Cache) menggunakan Redis.
# Penjelasan: Jika sebuah chart membutuhkan waktu 10 detik untuk menarik data dari database, 
# Redis akan menyimpan hasilnya. Jika ada user lain membuka chart yang sama, Superset tidak 
# perlu mengambil dari database lagi, tapi langsung mengambil dari Redis (hanya 0.1 detik).
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',            # Menggunakan Redis sebagai mesin cache
    'CACHE_DEFAULT_TIMEOUT': 86400,        # Data cache disimpan selama 24 jam (dalam detik)
    'CACHE_KEY_PREFIX': 'superset_',       # Penamaan file cache agar tidak tertukar
    'CACHE_REDIS_URL': 'redis://redis:6379/0' # Alamat container Redis di dalam Docker kita
}


# -----------------------------------------------------------------------------------------
# 4. KONFIGURASI FITUR TAMBAHAN (FEATURE FLAGS)
# -----------------------------------------------------------------------------------------

# Peran: Saklar (On/Off) untuk menyalakan fitur-fitur beta atau fitur khusus di Superset.
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True, # Mengizinkan penggunaan variabel logika (Jinja) di SQL Lab
    "DASHBOARD_CROSS_FILTERS": True,    # Mengizinkan user mengklik chart A, lalu chart B ikut terfilter
    "EMBEDDED_SUPERSET": True,          # WAJIB ON: Memunculkan tombol "Embed Dashboard" di UI Superset
}

# Peran: Mengatur batas waktu (umur) sesi login user.
# Penjelasan: Diatur ke 86400 detik (24 jam) agar user/developer tidak ter-logout secara 
# otomatis setiap beberapa jam saat sedang sibuk membuat dashboard.
# Catatan: Nilai bisa dioverride dari environment variable.
PERMANENT_SESSION_LIFETIME = _to_int(os.getenv("PERMANENT_SESSION_LIFETIME"), 86400)