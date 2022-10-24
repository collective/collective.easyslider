import unittest2 as unittest
from Testing import ZopeTestCase as ztc
from collective.easyslider.tests import BaseFunctionalTest


def test_suite():
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
            'browser.txt', package='collective.easyslider',
            test_class=BaseFunctionalTest)])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
