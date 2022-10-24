from Products.CMFCore.utils import getToolByName
from collective.easyslider.interfaces import ISliderPage
from zope.interface import noLongerProvides
try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite
import logging
logger = logging.getLogger('collective.easyslider')

from zope.annotation.interfaces import IAnnotations


def install(context):
    types = getToolByName(getSite(), 'portal_types')
    if 'Collection' in types.objectIds():
        collection = types['Collection']
        view_methods = set(collection.view_methods)
        view_methods.add('sliderview')
        collection.view_methods = tuple(view_methods)


def remove_annotations(items_to_check):
    for item in items_to_check:
        item = item.getObject()
        logger.info("Removing slider data for %s" % (
            '/'.join(item.getPhysicalPath())))
        noLongerProvides(item, ISliderPage)
        item.reindexObject(idxs=['object_provides'])

        annotations = IAnnotations(item)
        metadata = annotations.get('collective.easyslider', None)
        if metadata is not None:
            del annotations['collective.easyslider']


def remove_layout(portal, items):
    for item in items:
        utils = portal.plone_utils
        obj = item.getObject()
        layout = utils.browserDefault(obj)

        if layout[1][0] == "sliderview":
            logger.info("removing sliderview layout on %s" % (
                '/'.join(obj.getPhysicalPath())))
            layout[0].setLayout(layout[0].getDefaultLayout())


def uninstall(context):

    if context.readDataFile('collective.easyslider-uninstall.txt') is None:
        return

    portal = context.getSite()

    catalog = portal.portal_catalog
    remove_annotations(catalog.searchResults(
        object_provides=ISliderPage.__identifier__))
    items = catalog.searchResults(
        portal_type=('Folder', 'Topic', 'Large Plone Folder'))
    remove_annotations(items)
    remove_layout(portal, items)

    portal_actions = getToolByName(portal, 'portal_actions')
    object_buttons = portal_actions.object_buttons
    object_tabs = portal_actions.object

    actions_to_remove = ('enable_slider', 'disable_slider',
                         'slider_settings', 'view_slider_settings')
    for action in actions_to_remove:
        if action in object_buttons.objectIds():
            object_buttons.manage_delObjects([action])
        if action in object_tabs.objectIds():
            object_tabs.manage_delObjects([action])

    object_buttons._p_changed = 1
    object_tabs._p_changed = 1
