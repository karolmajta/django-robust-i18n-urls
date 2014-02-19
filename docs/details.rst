Details
=======

While *django-robust-i18n-urls* does not expose any particular APIs to end
users (it's designed as a plug&play app) it won't hurt to know what is
going on under the hood.


robust_urls.urls
----------------

This module contains `urlpatterns` variable that can be used as a drop-in
replacement for `urplatterns` contained in `django.conf.urls.i18n`.


robust_urls.views
-----------------

This module contains a single view that is used to change locale of current
user, and can be used as a drop-in replacement for `set_language` view
from `django.views.i18n.set_language`


set_language
~~~~~~~~~~~~

`set_language` view works in a fasion similar to Django's original one.
The key differences are:

* It does not allow GET requests, they will result in a 405 response.
  Only POST method is allowed.
* If a URL path specified in `request.REQUEST['next']` can be matched
  against a specific view, instead of issuing an immediate redirect,
  the `set_language` will first reverse the match to obtain a request
  path in language of user's choosing.
* If a URL path specified in `request.REQUEST['next']` cannot be matched
  to any view, a redirection will be issued to it anyway.


robust_urls.middleware
----------------------

This module containse the `RobustI18nLocaleMiddleware` that, next to
`robust_urls.view.set_language` is the app's main component.


RobustI18nLocaleMiddleware
~~~~~~~~~~~~~~~~~~~~~~~~~~

This middleware's `process_response` method will touch only responses
with `status_code` 404. It will try to match the URL using languages
in order specified in `LANGUAGES` setting. If a match is not found,
the response is returned unchanged. If a match is found, the result
of rendering the view's response is returned instead. This method also
takes care to set proper (matched) locale in user's session or language
cookie.


robust_urls.utils
-----------------


locale_context
~~~~~~~~~~~~~~

This context manager will execute given block making sure that language
provided as argument is active during execution. On exit will call
`translation.deactivate`.

.. code:: python

    with locale_context('pl_PL'):
        print _('Good Morning')  # will print 'Dzień Dobry'

**Warning! `locale_context` calls `transaction.deactivate` so it is
ill suited for use inside views. In future versions it will probably hold
to a locale used before the manager was endered, and activate it on exit
instead of calling `transaction.deactivate`. This api will change!**


try_uri_for_language
~~~~~~~~~~~~~~~~~~~~

A simple helper that takes *path*, *language* and *resolver* arguments.
Will try to resolve path using resolver, in context of given language.
If no match is found will return `None` instead of raising an exception.
If match is found will return whatever resolver returns (`ResolverMatch`
instance).
