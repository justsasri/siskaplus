# Cache time to live is an hour.
import os

CACHE_TTL = 60 * 0

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_CACHE_URL', 'redis://localhost:6379/2'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": os.getenv('SITE_NAME', 'instrasite')
    },
    'select2': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_CACHE_URL', 'redis://localhost:6379/2'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "select2_cache"
    }
}

# Set the cache backend to select2
SELECT2_CACHE_BACKEND = 'select2'