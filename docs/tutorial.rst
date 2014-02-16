Tutorial
========

Installing
----------

You can install the most recent version directly from pypi:

.. code::

    pip install django-robust-i18n-urls


For development
~~~~~~~~~~~~~~~

If you want to develop the application yourself (or just like living on the
bleeding edge) just checkout the code:

.. code::

    git checkout https://github.com/karolmajta/django-robust-i18n-urls.git

Install it as a code drop:

.. code::

    pip install -e .

Install development requirements (this will fetch Sphinx and Mock):

.. code::

    pip install -r requirements.txt


To run tests issue:

.. code::

    python setup.py test


Configuring
-----------

To make sure your users won't get 404 responses when using urls for locales
other than reported by their browser just modify your ``MIDDLEWARE_CLASSES``
setting, by adding ``robust_urls.middleware.RobustI18nLocaleMiddleware``.

If you plan on providing users with an url for changing their current language
just inlcude in your ``urls.py``:

.. code:: python

    import robust_urls.urls

    # ...

    urlpatterns += patterns(url(r'/i18n/', include(robust_urls.urls)))
