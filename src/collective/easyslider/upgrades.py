from Products.CMFCore.utils import getToolByName
from collective.easyslider.importexport import install

default_profile = 'profile-collective.easyslider:default'


def upgrade_from_0_3rc1__to__0_3rc2(context):
    context.runImportStepFromProfile(default_profile, 'viewlets')
    context.runImportStepFromProfile(default_profile, 'portlets')
    context.runImportStepFromProfile(default_profile, 'jsregistry')
    context.runImportStepFromProfile(default_profile, 'cssregistry')


def upgrade_to_0_3rc2(context):
    #just run all since you don't know what version was previously used
    context.runAllImportStepsFromProfile(default_profile)


def upgrade_to_0_3rc4(context):
    pass


def upgrade_to_0_3(context):
    """
    just reload portal_javascripts for the js changes to take effect
    """
    portal_javascripts = getToolByName(context, 'portal_javascripts')
    portal_javascripts.cookResources()


def upgrade_to_0_4_0(context):
    """
    Just have to re-cook css and js since those files changed
    """
    js = getToolByName(context, 'portal_javascripts')
    js.cookResources()
    css = getToolByName(context, 'portal_css')
    css.cookResources()


def upgrade_to_0_4_1(context):
    pass


def upgrade_to_0_5_4(context):
    js = getToolByName(context, 'portal_javascripts')
    js.cookResources()


def upgrade_rolemap(context):
    context.runImportStepFromProfile(default_profile, 'rolemap')


def upgrade_controlpanel(context):
    context.runImportStepFromProfile(default_profile, 'controlpanel')


def upgrade_collection(context):
    install(context)
