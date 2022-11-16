from collective.easyslider.tests import BaseTest
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from plone.portlets.interfaces import IPortletType
from Products.CMFCore.utils import getToolByName
from zope.component import getUtilitiesFor
from zope.component import queryUtility

import unittest2 as unittest


class TestSetup(BaseTest):
    """ """

    def test_portlet_installed_correctly(self):
        portlets = [u[0] for u in getUtilitiesFor(IPortletType)]
        self.assertTrue("collective.easyslider.portlet.slider" in portlets)

    def test_portlet_uninstalls_correctly(self):
        self.uninstall()
        portlets = [u[0] for u in getUtilitiesFor(IPortletType)]
        self.assertTrue("collective.easyslider.portlet.slider" not in portlets)

    def test_css_registry(self):
        pcss = self.portal.portal_css
        self.assertTrue(
            "++resource++easySlider.css" in [css.getId() for css in pcss.getResources()]
        )
        self.assertTrue(
            "++resource++slider-settings.css"
            in [css.getId() for css in pcss.getResources()]
        )
        self.assertTrue(
            "++resource++easyslider-portlet.css"
            in [css.getId() for css in pcss.getResources()]
        )

    def test_css_registry_uninstalls(self):
        self.uninstall()
        pcss = self.portal.portal_css
        self.assertTrue(
            "++resource++easySlider.css"
            not in [css.getId() for css in pcss.getResources()]
        )
        self.assertTrue(
            "++resource++slider-settings.css"
            not in [css.getId() for css in pcss.getResources()]
        )
        self.assertTrue(
            "++resource++easyslider-portlet.css"
            not in [css.getId() for css in pcss.getResources()]
        )

    def test_js_added(self):
        pjavascripts = getToolByName(self.portal, "portal_javascripts")
        self.assertTrue(
            "++resource++easySlider.js"
            in [js.getId() for js in pjavascripts.getResources()]
        )
        self.assertTrue(
            "++resource++slider-settings.js"
            in [js.getId() for js in pjavascripts.getResources()]
        )
        self.assertTrue(
            "++resource++easyslider-portlet.js"
            in [js.getId() for js in pjavascripts.getResources()]
        )

    def test_js_uninstalls(self):
        self.uninstall()
        pjavascripts = getToolByName(self.portal, "portal_javascripts")
        self.assertTrue(
            "++resource++easySlider.js"
            not in [js.getId() for js in pjavascripts.getResources()]
        )
        self.assertTrue(
            "++resource++slider-settings.js"
            not in [js.getId() for js in pjavascripts.getResources()]
        )
        self.assertTrue(
            "++resource++easyslider-portlet.js"
            not in [js.getId() for js in pjavascripts.getResources()]
        )

    def test_actions_install(self):
        actionTool = self.portal.portal_actions

        # these would throw an exception if they weren't there..
        actionTool.getActionInfo(["object_buttons/enable_slider"])
        actionTool.getActionInfo(["object_buttons/disable_slider"])
        actionTool.getActionInfo(["object/slider_settings"])
        actionTool.getActionInfo(["object/view_slider_settings"])

    def test_actions_uninstall(self):
        self.uninstall()
        actionTool = self.portal.portal_actions

        ob = actionTool["object_buttons"]
        os = actionTool["object"]
        # these would throw an exception if they weren't there..
        self.assertTrue("enable_slider" not in ob.objectIds())
        self.assertTrue("disable_slider" not in ob.objectIds())
        self.assertTrue("slider_settings" not in os.objectIds())
        self.assertTrue("view_slider_settings" not in os.objectIds())

    def test_viewlet_installs(self):
        storage = queryUtility(IViewletSettingsStorage)
        self.assertTrue(
            "collective.easyslider" in storage.getOrder("plone.belowcontenttitle", None)
        )
        self.assertTrue(
            "collective.easyslider.head"
            in storage.getOrder("plone.htmlhead.links", None)
        )
        self.assertTrue(
            "collective.easyslider" in storage.getOrder("plone.belowcontent", None)
        )

    def test_viewlet_uninstalls(self):
        self.uninstall()
        storage = queryUtility(IViewletSettingsStorage)
        self.assertTrue(
            "collective.easyslider"
            not in storage.getOrder("plone.belowcontenttitle", None)
        )
        self.assertTrue(
            "collective.easyslider.head"
            not in storage.getOrder("plone.htmlhead.links", None)
        )
        self.assertTrue(
            "collective.easyslider" not in storage.getOrder("plone.belowcontent", None)
        )

    def test_permissions(self):
        """Ensure Site Administrators can manage sliders on Plone 4.1+."""
        mtool = getToolByName(self.portal, "portal_membership", None)
        perm = "collective.easyslider: Manage slider settings"
        roles = self.portal.rolesOfPermission
        if mtool and "Site Administrator" in mtool.getPortalRoles():
            roles = [r["name"] for r in roles(perm) if r["selected"]]
            self.assertEqual(roles, ["Site Administrator"])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
