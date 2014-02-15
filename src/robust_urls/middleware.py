'''
Created on 13 lut 2014

@author: karol
'''
from django.conf import settings
from django.core.urlresolvers import get_resolver
from django.utils import translation

from .utils import try_url_for_language

class RobustI18nLocaleMiddleware(object):
    """
    If `response.status_code == 404` this middleware makes sure to
    check request.path resolution in contex of all languages present
    in `settings.Languages`. If resolution succeeds a proper page will
    be returned instead. If resolution fails nothing happens.
    """
    
    def process_response(self, request, response):
        """
        If request status code is other than 404, just return provided response.
        If request status code is 404:
          - if request.path can be resolved in context of a language from
            `settings.Languages`, call `handle_successful_match` and return it's
            result
          - if request.path cannot be resolved in context of a language from
            `settings.Languages` return provided response.
        """
        if response.status_code == 404:
            all_languages =  [i[0] for i in settings.LANGUAGES]
            resolver = get_resolver(None)
            for language in all_languages:
                match = try_url_for_language(request.path, language, resolver)
                if match is not None:
                    return self.handle_successful_match(
                        request,
                        response,
                        match[0],
                        match[1],
                        match[2],
                        language
                    )
            return response
        else:
            return response
    
    def handle_successful_match(self, request, response,  view, args, kwargs, language):
        """
        In order make sure to:
          - store the matched language in users session or cookie
          - render response from matched view (in context of matched language) and
            return it.
        """
        # this is copypasted from django's i18n.py view
        if hasattr(request, 'session'):
            request.session['django_language'] = language
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        # we shall activate translation during response rendering
        # i am not sure if this is a necessity, but it's surely not stupid
        # to do so
        translation.activate(language)
        resp = view(request, *args, **kwargs)
        resp.render()
        translation.deactivate()
        return resp