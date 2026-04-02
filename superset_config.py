import os

# Menangkap variabel environment dari docker-compose.yml
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SUPERSET_SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

# Konfigurasi Cache agar dashboard tidak lemot
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_URL': 'redis://redis:6379/0'
}

# Fitur-fitur tambahan
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_CROSS_FILTERS": True,
}

PERMANENT_SESSION_LIFETIME = 86400