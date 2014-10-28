import os
from memcacheify import memcacheify
from postgresify import postgresify
from envs.common import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'django_ses.SESBackend'
BROKER_URL = os.environ["REDISTOGO_URL"]

MEDIA_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
ADMIN_MEDIA_PREFIX = '%sadmin/' % STATIC_URL
COMPRESS_URL = STATIC_URL
FAVICON_URL = "%sfavicon.ico" % STATIC_URL

CACHES = memcacheify()
DATABASES = None
DATABASES = postgresify()
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = "backends.CachedS3BotoStorage"
COMPRESS_STORAGE = STATICFILES_STORAGE

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
GOOGLE_ANALYTICS_PROPERTY_ID = "UA-47030017-1"