from collective.easyslider.interfaces import ICollectiveEasysliderLayer
from collective.easyslider.testing import COLLECTIVE_EASYSLIDER_FUNCTIONAL_TESTING
from collective.easyslider.testing import COLLECTIVE_EASYSLIDER_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from zope.interface import alsoProvides

import unittest


class BaseTest(unittest.TestCase):

    layer = COLLECTIVE_EASYSLIDER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.app = self.layer["app"]
        alsoProvides(self.request, ICollectiveEasysliderLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def tearDown(self):
        pass

    def uninstall(self):
        setup_tool = getToolByName(self.portal, "portal_setup")
        setup_tool.runAllImportStepsFromProfile(
            "profile-collective.easyslider:uninstall"
        )

    def create_object(self, id, type_name, parent=None):
        if parent:
            return parent[parent.invokeFactory(type_name=type_name, id=id)]
        else:
            return self.portal[self.portal.invokeFactory(type_name=type_name, id=id)]


class BaseFunctionalTest(BaseTest):
    layer = COLLECTIVE_EASYSLIDER_FUNCTIONAL_TESTING
