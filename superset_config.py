import os

# Fetch environment variables from docker-compose.yml
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SUPERSET_SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

# ==========================================
# --- EMBEDDING CONFIGURATION (NEW) ---
# ==========================================

# 1. Secret key for Guest Token (passwordless access for web viewers)
# Ideally, add GUEST_TOKEN_JWT_SECRET to your .env file later.
GUEST_TOKEN_JWT_SECRET = os.getenv("GUEST_TOKEN_JWT_SECRET", "super-secret-guest-token-do-not-share")

# 2. Allow Superset to be opened within modern browser Iframes
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True  # Must be True for iframes to work in modern browsers (especially if your main site uses HTTPS)

# 3. Disable built-in protections that block Iframes
HTTP_HEADERS = {'X-Frame-Options': 'ALLOWALL'}
TALISMAN_ENABLED = False 

# 4. Enable CORS so other websites can communicate with Superset
ENABLE_CORS = True
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['*'] # In production, replace '*' with your website's domain, e.g., ['https://yourwebsite.com']
}

# ==========================================

# Cache configuration to ensure fast dashboard rendering
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_URL': 'redis://redis:6379/0'
}

# Additional Feature Flags
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "EMBEDDED_SUPERSET": True, # 5. REQUIRED: Enables the "Embed" menu in the Superset UI
}

# Allow anonymous users to be automatically assigned the 'Public' role
AUTH_ROLE_PUBLIC = "Public"

# Grant the 'Public' role permissions similar to the 'Gamma' (viewer) role
PUBLIC_ROLE_LIKE = "Gamma"

PERMANENT_SESSION_LIFETIME = 86400