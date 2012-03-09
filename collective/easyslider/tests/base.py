import unittest
import sys
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
from Products.CMFCore.utils import getToolByName

from zope.configuration import xmlconfig

import collective.easyslider

@onsetup
def setUp():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', collective.easyslider)
    fiveconfigure.debug_mode = False
    ztc.installPackage('collective.easyslider')

setUp()

ptc.setupPloneSite(products=('collective.easyslider', ))

class ESTestCase(ptc.PloneTestCase):
    """
    """
    def afterSetUp(self):
        self.setRoles(('Manager',))
        
    def uninstall(self):
        setup_tool = getToolByName(self.portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-collective.easyslider:uninstall')
        
    def create_object(self, id, type_name, parent=None):
        if parent:
            return parent[parent.invokeFactory(type_name=type_name, id=id)]
        else:
            return self.portal[self.portal.invokeFactory(type_name=type_name, id=id)]