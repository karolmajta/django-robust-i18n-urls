# django-robust-i18n-urls

This application solves a few problems related with using internaitonalized
urls inside Django. If you want a full rationale please check out:

http://blog.karolmajta.com/robust-internationalized-urls-for-django.html

for an article explaining issues that arise when dealing with default
Django setup for internationalized urls.

## Usage

To use the app:

    pip install django-robust-i18n-urls

In your `urls.py`, add to your `urlpatterns`:

    url(r'^i18n/', include('robust_urls.urls')),

In your `settings.py`:

    MIDDLEWARE_CLASSES = (
        # ...
        'robust_urls.middleware.RobustI18nLocaleMiddleware',
        # ...
    )

This should get you going with the default setup. Django's documentation
on translation and selecting language can help you.

For full documentation please see
http://django-robust-i18n-urls.readthedocs.org/

## Development

Clone this repo, then:

    pip install -e .
    pip install -r requirements.txt
    python setup.py test

## TODO/Roadmap

Currently I don't need any more features beyond what is already provided,
but if you have ones that suit your use cases, feel free to issue a pull
request. Any additional tests are welcome too.
