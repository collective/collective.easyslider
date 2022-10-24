from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from zope.configuration import xmlconfig
from plone.testing import z2


class EasySlider(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import collective.easyslider
        xmlconfig.file('configure.zcml', collective.easyslider,
                       context=configurationContext)
        z2.installProduct(app, 'collective.easyslider')

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'collective.easyslider:default')
        setRoles(portal, TEST_USER_ID, ('Member', 'Manager'))
        workflowTool = getToolByName(portal, 'portal_workflow')
        workflowTool.setDefaultChain('plone_workflow')


EasySlider_FIXTURE = EasySlider()
EasySlider_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EasySlider_FIXTURE,), name="EasySlider:Integration")
EasySlider_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EasySlider_FIXTURE,), name="EasySlider:Functional")


def browserLogin(portal, browser, username=None, password=None):
    handleErrors = browser.handleErrors
    try:
        browser.handleErrors = False
        browser.open(portal.absolute_url() + '/login_form')
        if username is None:
            username = TEST_USER_NAME
        if password is None:
            password = TEST_USER_PASSWORD
        browser.getControl(name='__ac_name').value = username
        browser.getControl(name='__ac_password').value = password
        browser.getControl(name='submit').click()
    finally:
        browser.handleErrors = handleErrors


def createObject(context, _type, id, delete_first=True,
                 check_for_first=False, **kwargs):
    if delete_first and id in context.objectIds():
        context.manage_delObjects([id])
    if not check_for_first or id not in context.objectIds():
        return context[context.invokeFactory(_type, id, **kwargs)]

    return context[id]
