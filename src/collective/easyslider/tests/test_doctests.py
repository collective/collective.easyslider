from collective.easyslider.tests import BaseFunctionalTest
from Testing import ZopeTestCase as ztc

import unittest2 as unittest


def test_suite():
    return unittest.TestSuite(
        [
            ztc.FunctionalDocFileSuite(
                "browser.txt",
                package="collective.easyslider",
                test_class=BaseFunctionalTest,
            )
        ]
    )


if __name__ == "__main__":
    unittest.main(defaultTest="test_suite")
