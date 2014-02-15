from unittest import TestCase

import mock

from robust_urls.utils import locale_context, try_url_for_language

from django.core.urlresolvers import Resolver404


class LocaleContextTestCase(TestCase):

    @mock.patch('robust_urls.utils.translation')    
    def testWillCallTranslationActivateBeforeCallingBlock(self, translation): 
        with locale_context('pl_PL'):
            translation.activate.assert_called_once_with('pl_PL')
        translation.activate.assert_called_once_with('pl_PL')
    
    @mock.patch('robust_urls.utils.translation')    
    def testWillCallTranslationDeactivateAfterCallingBlock(self, translation):
        with locale_context('pl_PL'):
            translation.deactivate.assert_not_called()
        translation.deactivate.assert_called_once()
    
    @mock.patch('robust_urls.utils.translation')
    def testWillCallWhateverIsInTheBlock(self, translation):
        fun = mock.Mock()
        with locale_context('anything'):
            fun()
        fun.assert_called_once()


class TryUrlForLanguageTestCase(TestCase):
    
    @mock.patch('robust_urls.utils.locale_context')
    def testWillCallResolverInsideLocaleContext(self, locale_context):
        resolver = mock.Mock()
        try_url_for_language('/some/path/', 'pl_PL', resolver)
        resolver.resolve.assert_called_once_with('/some/path/')
        locale_context.assert_called_with('pl_PL')
    
    @mock.patch('robust_urls.utils.locale_context')
    def testWillReturnWhateverResolverReturns(self, locale_context):
        resolver = mock.Mock()
        resolver.resolve.return_value = 'hello'
        result = try_url_for_language('/some/path', 'pl_PL', resolver)
        self.assertEquals('hello', result)
    
    @mock.patch('robust_urls.utils.locale_context')
    def testWillReturnNoneIfResolverRaises(self, locale_context):
        resolver = mock.Mock()
        resolver.resolve.side_effect = Resolver404
        result = try_url_for_language('/any/', 'pl_PL', resolver)
        self.assertIsNone(result)