from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class MediaYandexCloudStorage(S3Boto3Storage):
    bucket_name = settings.YANDEX_OBJECT_STORAGE_BUCKET_NAME
    location = 'media'
    file_overwrite = False


class StaticYandexCloudStorage(S3Boto3Storage):
    bucket_name = settings.YANDEX_OBJECT_STORAGE_BUCKET_NAME
    location = 'static'
    file_overwrite = False
