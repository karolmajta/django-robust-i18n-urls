Rationale
=========

`django-robust-i18n-urls: <http://django-robust-i18n-urls.readthedocs.org/>`_
is a Django application providing sane defaul behavior for internationalized
urls.

The problem
-----------

For the case of this discussion let's assume your ``urlpatterns`` variable
contains a pattern like:

.. code:: python

    url(_(r'^hello/'), my_view, name='my_view')

If the pattern ``^hello/`` gets translated into Spanish ``^ola/`` the expected
behavior would be for the controller to be accessible using both urls.
Unfortunately this is not the case with Django. Urls get resolved in a
context of a single locale. This way, if a user with ``Accept-Language`` header
set to *en* tries to access **/ola/**, he will be shown an error 404 page.

The solution
------------

`django-robust-i18n-urls <http://django-robust-i18n-urls.readthedocs.org/>`_
provides a middleware that, facing a response with ``status_code`` set to *404*
will try to resolve the url again in context of all currently installed
languages. In case of a first successful match, it will be returned instead
of the error, and a matched language will be set as default for current user's
session.

Some other minor issues can arise when dealing with i18n urls, an this
library deals with some of them. The default workings of these helpers
is detailed in :ref:`Details` section.

