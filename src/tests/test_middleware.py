import unittest

import mock

from robust_urls.middleware import RobustI18nLocaleMiddleware


class RobustI18nLocaleMiddlewareTestCase(unittest.TestCase):
    
    settings = mock.Mock()
    settings.LANGUAGES = (
        ('en', 'English'),
        ('pl', 'Polish'),
        ('de', 'German'),
        ('fr', 'French'),
    )
    
    def setUp(self):
        self.middleware = RobustI18nLocaleMiddleware()
    
    def testProcessResponseWillJustReturnResponsesOtherThan404(self):
        response = mock.Mock()
        response.status_code = 200
        self.assertEquals(
            response,
            self.middleware.process_response(None, response)
        )
    
    @mock.patch('robust_urls.middleware.settings', settings)
    @mock.patch('robust_urls.middleware.get_resolver')
    def testProcessResponseWillTryToResolveWithAllLanguages(self, resolver):
        request = mock.Mock()
        request.path = '/hello/'
        response = mock.Mock()
        response.status_code = 404
        with mock.patch('robust_urls.middleware.try_url_for_language') as m:
            m.return_value = None
            result = self.middleware.process_response(request, response)
            expected_langs = ['en', 'pl', 'de', 'fr']
            actual_langs = [c[1][1] for c in m.mock_calls]
            self.assertListEqual(expected_langs, actual_langs)
            self.assertEqual(response, result)
    
    @mock.patch('robust_urls.middleware.settings', settings)
    @mock.patch('robust_urls.middleware.get_resolver', mock.Mock())
    @mock.patch('robust_urls.middleware.translation', mock.Mock())
    def testProcessResponseWillTryUnlessMatchAndReturnResultOfHandle(self):
        request = mock.MagicMock()
        request.path = '/hello/'
        response = mock.Mock()
        response.status_code = 404
        with mock.patch('robust_urls.middleware.try_url_for_language',
                        mock.Mock(side_effect=self.matchGerman)) as m:
            retval = mock.Mock()
            with mock.patch.object(self.middleware,  # @UndefinedVariable
                                   'handle_successful_match',
                                   mock.Mock(return_value=retval)):  
                result = self.middleware.process_response(request, response)
                expected_langs = ['en', 'pl', 'de']
                actual_langs = [c[1][1] for c in m.mock_calls]
                self.assertListEqual(expected_langs, actual_langs)
                self.assertEqual(retval, result)
    
    def matchGerman(self, path, lang, resolver):
        if lang == 'de':
            return (lambda x: mock.Mock(), (), {})
        else:
            return None    