# -*- coding: utf-8 -*-
from collective.easyslider.testing import COLLECTIVE_EASYSLIDER_FUNCTIONAL_TESTING
from collective.easyslider.testing import COLLECTIVE_EASYSLIDER_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_EASYSLIDER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_view_slider_settings_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST),
            name="view-slider-settings",
        )
        self.assertTrue(view.__name__ == "view-slider-settings")

    def test_view_slider_settings_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST),
                name="view-slider-settings",
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_EASYSLIDER_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
