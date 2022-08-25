from storages.backends.s3boto3 import S3Boto3Storage
# Fro aws


class MediaStorage(S3Boto3Storage):
    location = 'offer-1/media'
    file_overwrite = True
