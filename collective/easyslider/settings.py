from Acquisition import aq_inner
from collective.easyslider.interfaces import IPageSliderSettings
from collective.easyslider.interfaces import IViewSliderSettings
from collective.easyslider.interfaces import ISliderSettings
from persistent.dict import PersistentDict
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements


class SliderSettings(object):
    """
    Pretty much copied how it is done in Slideshow Folder
    hopefully no one is foolish enough to want a custom slider
    and a view slider.  If they are then the settings will
    overlap.
    """
    implements(IPageSliderSettings)

    interfaces = []

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)

        self._metadata = annotations.get('collective.easyslider', None)
        if self._metadata is None:
            self._metadata = PersistentDict()
            annotations['collective.easyslider'] = self._metadata

        ctx = aq_inner(context)
        rootctx = getToolByName(ctx, 'portal_url').getPortalObject()
        rootannotations = IAnnotations(rootctx)
        self._rootmetadata = rootannotations.get('collective.easyslider', None)
        if self._rootmetadata is None:
            self._rootmetadata = PersistentDict()
            rootannotations['collective.easyslider'] = self._rootmetadata

    @property
    def __parent__(self):
        return self.context

    @property
    def __roles__(self):
        return self.context.__roles__

    def __setattr__(self, name, value):
        if name[0] == '_' or name in ['context', 'interfaces']:
            self.__dict__[name] = value
        else:
            self._metadata[name] = value

    def __getattr__(self, name):
        value = self._metadata.get(name)
        if value is None:
            # first check to see if there are global settings
            if name in self._rootmetadata:
                return self._rootmetadata[name]
            else:
                # no global settings, check to see if there are defaults
                for interface in self.interfaces:
                    v = interface.get(name)
                    if v:
                        return v.default
        return value


class PageSliderSettings(SliderSettings):
    interfaces = [ISliderSettings, IPageSliderSettings]

    def __getattr__(self, name):
        if name == 'slides':
            # somehow this default value gets manually set. This prevents this
            # form happening on the slides...
            return self._metadata.get(name, [])
        return super(PageSliderSettings, self).__getattr__(name)


class ViewSliderSettings(SliderSettings):
    interfaces = [ISliderSettings, IViewSliderSettings]
