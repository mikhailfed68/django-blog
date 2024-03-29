# “Incognito” Blog
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Django CI](https://github.com/MichaelFed68/django-blog/actions/workflows/github_actions.yaml/badge.svg?branch=main)](https://github.com/MichaelFed68/django-blog/actions)

## Description
Hello! 👋 This app was created for educational purposes!

It is a blog where you can read and create blogs and articles.
You can also follow interesting authors or blogs in your personal feed by subscribing to them!

*All you have to do to try the full functionality of this project is to register on site!*

#### Behind the scene:
- Python (Django as the main framework)
- PostgreSQL for data
- Redis for caching, sessions and online system functionality
- Yandex Cloud Object Storage (S3 API) for media and static files
- Bootstrap 5 for a beautiful and fast-changing design

#### App on Railway:
> [Incognito blog](https://incognito-b.up.railway.app)

*The same as Heroku*

## For developers

### Requirements

* Docker
* Docker compose

If you want to install this project on your local machine manually, you need to do the following:
Clone the repository and go to it:

`git clone https://github.com/MichaelFed68/django-blog.git`

`cd django-blog`

Now, you have to create .env.dev file and setup environment variables:

`touch .env.dev`

This is the minimum set of variables to start a project:

DEBUG='true'

SECRET_KEY='your generated secret key for django project'

_For example:_

`from django.core.management.utils import get_random_secret_key`

`get_random_secret_key()`

>See [Environment variables](#environment-variables) section.

When you have configured variables, run following docker compose commands:

`docker compose build`

`docker compose up`

## Environment variables
This is a list of enviroment variables that are needed
for the application to work correctly

**ALLOWED_HOSTS**

Values are specified as a string, separated by a space

_By default set to '127.0.0.1 .localhost [::1]'_

**CSRF_TRUSTED_ORIGINS**

Values are specified as a string, separated by a space

_By default set to 'http://127.0.0.1'_

**SECRET_KEY**

**DEBUG**

_By default set to False_

**DATABASE_URL**

postgresql://[user[:password]@][host][:port][/dbname]

**REDIS_URL**

redis://host:port

---
**BASE_GROUP**

_By default set to 'base_members_of_site'_

The name of the group that will be automatically
created when the user first registers on the site.
It will contain all the listed permissions
from the PERMISSIONS_FOR_BASE_GROUP variable.

**PERMISSIONS_FOR_BASE_GROUP**

_By default set to the following list:
["add_article", "change_article", "delete_article", "view_article", "add_blog", "view_blog", "view_language", "change_profile", "delete_profile", "view_profile"]_

Contains a list of permissions that
will be granted to newly registered users.

---
***USER_ONLINE_TIMEOUT***

_By default set to 60 seconds_

Time during which the user will be considered online

**USER_LAST_SEEN_TIMEOUT**

_By default set to 86400 seconds (1 day)_

Time during which the date of the last visit of the user will be stored in Redis

---
**ENABLED_YANDEX_STORAGE**

_By default set to False_

Whether or not Yandex cloud storage will be used.
The app can use custom storage
through the S3 API provided by Yandex cloud.

_Read more in the documentation of Yandex storage
if you want to use it_

https://cloud.yandex.com/en/docs/storage/s3/

https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

_For more information, read django-storages docs also_

**YANDEX_OBJECT_STORAGE_BUCKET_NAME**

Your backet name in Object Storage

**YANDEX_S3_DOMAIN**

_f.e. '.s3.yandexcloud.net'_

**AWS_S3_ENDPOINT_URL**

_f.e. 'https://storage.yandexcloud.net'_

**AWS_S3_REGION_NAME**

_f.e. 'ru-central1-a'_

---
**ENABLED_EMAIL**

Whether or not the actual mailing will be used.

_By default set to False_

Define to send a password reset email and error reporting:

_Requires ENABLED_EMAIL='true'_

**SERVER_EMAIL**

**ADMINS**

A *tuple* of all the people who get code error notifications

**EMAIL_USE_TLS**

**EMAIL_PORT**

**EMAIL_HOST**

**EMAIL_HOST_USER**

**EMAIL_HOST_PASSWORD**

## Support
If you need help, please contact me via email:
> mikhailfedorov1939@gmail.com
