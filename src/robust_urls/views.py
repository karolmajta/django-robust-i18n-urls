'''
Created on 13 lut 2014

@author: karol
'''
import urlparse
import urllib

from django.conf import settings
from django.core.urlresolvers import get_resolver, reverse
from django.utils.http import is_safe_url
from django.utils.translation import get_language, check_for_language
from django import http

from .utils import try_url_for_language, locale_context

def set_language(request):
    """
    Redirect to a given url, reversed while setting the chosen language in the
    session or cookie. The url and the language code need to be
    specified in the request parameters.

    Since this view changes how the user will see the rest of the site, it must
    only be accessed as a POST request.
    """
    
    if request.method == 'POST':
        # get necessary values from request
        language = request.POST.get('language', None)
        next_path = request.REQUEST.get('next', '')
        # django safety checks... 
        if not is_safe_url(url=next_path, host=request.get_host()):
            referer = request.META.get('HTTP_REFERER', '')
            next_path = urlparse.urlparse(referer).path
            if not is_safe_url(url=next_path, host=request.get_host):
                next_path = '/'
        
        next_path = urllib.unquote(next_path).decode('utf8')

        # check if given url is found using current locale
        resolver = get_resolver(None)
        resolve_result = try_url_for_language(next_path, get_language(), resolver)
        if resolve_result is None:
            # we didn't succeed at resolving the url with current locale, so
            # we may as well redirect to given url, and it will just be a 404
            redirect_to = next_path
        else:
            # we did succeed, this means the route exists and we can get view's
            # name, expected args and kwargs
            url_name = resolve_result.url_name
            view_args = resolve_result[1]
            view_kwargs = resolve_result[2]
            with locale_context(language):
                redirect_to = reverse(url_name, args=view_args, kwargs=view_kwargs)
            
        # this is standard django stuff again...
        response = http.HttpResponseRedirect(redirect_to)
        if language and check_for_language(language):
            if hasattr(request, 'session'):
                request.session['django_language'] = language
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
    else:
        return http.HttpResponseNotAllowed(['POST',])