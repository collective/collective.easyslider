from collective.easyslider.portlets import slider as sliderportlet
from collective.easyslider.tests import BaseTest
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from zope.component import getMultiAdapter
from zope.component import getUtility


class TestPortlet(BaseTest):
    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name="collective.easyslider.portlet.slider")
        self.assertEquals(portlet.addview, "collective.easyslider.portlet.slider")

    def testInterfaces(self):
        portlet = sliderportlet.Assignment(over="blah", under="blah")
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name="collective.easyslider.portlet.slider")
        mapping = self.portal.restrictedTraverse("++contextportlets++plone.leftcolumn")
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse("+/" + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], sliderportlet.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()

        mapping["foo"] = sliderportlet.Assignment(over="blah", under="blah")
        editview = getMultiAdapter((mapping["foo"], self.request), name="edit")
        self.failUnless(isinstance(editview, sliderportlet.EditForm))

    def testRenderer(self):
        context = self.portal
        view = self.portal.restrictedTraverse("@@plone")
        manager = getUtility(
            IPortletManager, name="plone.leftcolumn", context=self.portal
        )
        assignment = sliderportlet.Assignment(over="blah", under="blah")

        renderer = getMultiAdapter(
            (context, self.request, view, manager, assignment), IPortletRenderer
        )
        self.failUnless(isinstance(renderer, sliderportlet.Renderer))


class TestRenderer(BaseTest):
    def renderer(
        self, context=None, request=None, view=None, manager=None, assignment=None
    ):
        context = self.portal
        view = view or self.portal.restrictedTraverse("@@plone")
        manager = manager or getUtility(
            IPortletManager, name="plone.leftcolumn", context=self.portal
        )
        assignment = assignment or sliderportlet.Assignment(
            template="portlet_recent", macro="portlet"
        )

        return getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer
        )


def test_suite():
    from unittest import makeSuite
    from unittest import TestSuite

    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
