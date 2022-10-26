from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.easyslider.controlpanels.easy_slider_settings.controlpanel import (
    IEasySliderSettings,
)
from collective.easyslider.interfaces import IPageSliderSettings
from collective.easyslider.interfaces import ISliderSettings
from collective.easyslider.interfaces import IViewSliderSettings
from persistent.mapping import PersistentMapping
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from z3c.form import interfaces
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implementer


@implementer(IPageSliderSettings)
class SliderSettings(object):
    """
    Pretty much copied how it is done in Slideshow Folder
    hopefully no one is foolish enough to want a custom slider
    and a view slider.  If they are then the settings will
    overlap.
    """

    interfaces = []

    def _get_field_names_from_schema(self):
        names = []
        for iface in self.interfaces:
            names.extend(iface.names())
        return names

    def __init__(self, context):
        self.context = context
        self._registry = getUtility(IRegistry)

        try:
            annotations = IAnnotations(self.context)
        except TypeError:
            # XXX for things like plone.app.event, traversers
            # are not adaptable so we need to look at the parent here
            self.context = aq_parent(context)
            annotations = IAnnotations(self.context)

        self._metadata = annotations.get("collective.easyslider", None)
        if self._metadata is None:
            defaults = PersistentMapping()
            field_names = self._get_field_names_from_schema()
            for k in field_names:
                defaults[k] = self._registry.get(
                    "collective.easyslider.easy_slider_settings.{}".format(k)
                )
            self._metadata = defaults
            annotations["collective.easyslider"] = self._metadata

    @property
    def __parent__(self):
        return self.context

    @property
    def __roles__(self):
        return self.context.__roles__

    def __setattr__(self, name, value):
        if name[0] == "_" or name in ["context", "interfaces"]:
            self.__dict__[name] = value
        else:
            self._metadata[name] = value

    def __getattr__(self, name):
        if name[0] == "_" or name in ["context", "interfaces"]:
            return self.__dict__[name]
        value = self._metadata.get(name)
        # if value is None:
        #     # print(f"using global setting: {name}")
        #     return self._get_global_setting(name)
        return value


class PageSliderSettings(SliderSettings):
    interfaces = [ISliderSettings, IPageSliderSettings]

    def __getattr__(self, name):
        if name == "slides":
            # somehow this default value gets manually set. This prevents this
            # form happening on the slides...
            return self._metadata.get(name, [])
        return super().__getattr__(name)


class ViewSliderSettings(SliderSettings):
    interfaces = [ISliderSettings, IViewSliderSettings]
