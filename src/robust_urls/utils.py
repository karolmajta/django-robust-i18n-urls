'''
Created on 13 lut 2014

@author: karol
'''

from contextlib import contextmanager

from django.core.urlresolvers import Resolver404
from django.utils import translation

@contextmanager
def locale_context(locale):
    """
    Calls given block of code between calls to `transaction,activate(locale)` and
    `transaction.deactivate()`.
    """
    translation.activate(locale)
    yield
    translation.deactivate()


def try_url_for_language(path, language, resolver):
    """
    Tries to resolve given path forcing `transaction.get_language()` to be 
    given language. If url resoution succeeds returns a ResolverMatch, if
    not returns None.
    """
    with locale_context(language):
        try:
            return resolver.resolve(path)
        except Resolver404:
            return None