import sys, os
import unittest

from setuptools import setup

import distutils.core
import distutils.errors


class FailedTestsError(distutils.errors.DistutilsError):
    """One or more tests failed"""


class RunUnittests(distutils.core.Command):
    """Custom test command"""
    description = "run unit tests"

    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):
        # make sure robust_urls is on sys.path. If it is present do nothing,
        # we shall run tests on the present instance. If it's not present
        # add `src` to python path (this means we are testing a source checkout)
        try:
            import robust_urls
        except ImportError:
            project_root = os.path.dirname(os.path.abspath(__file__))
            sys.path.append(os.path.join(project_root, 'src'))
        
        loader = unittest.TestLoader()
        tests = loader.discover('src/tests')
        testRunner = unittest.runner.TextTestRunner()
        result = testRunner.run(tests)
        if len(result.errors) > 0 or len(result.failures) > 0:
            tpl = "Test runner reported {0} failures and {1} errors."
            msg = tpl.format(len(result.failures), len(result.errors))
            raise FailedTestsError(msg)
        
        
setup(
    name = "django-robust-i18n-urls",
    version = "1.0.0",
    package_dir = {
        '': 'src',
    },
    packages = [
        'robust_urls',
    ],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [
        'Django>=1.5.0',
    ],

    author = "Karol Majta",
    author_email = "karolmajta@gmail.com",
    description = "Robust internationalized urls implementation for Django.",
    license = "MIT",
    url = "http://karolmajta.com/django-robust-i18n-urls/",
    
    cmdclass = {
        'test': RunUnittests,
    },
)
