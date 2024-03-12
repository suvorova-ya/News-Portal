from django.apps import AppConfig
# import redis

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals


# red = redis.Redis(
#     host='redis-10989.c302.asia-northeast1-1.gce.cloud.redislabs.com',
#     port=10989,
#     password='8QVl794BSqNDSuhbGkVUEziF1KT8R6kI'
# )