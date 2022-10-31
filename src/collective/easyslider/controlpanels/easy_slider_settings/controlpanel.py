# -*- coding: utf-8 -*-
from collective.easyslider import _
from collective.easyslider.interfaces import ICollectiveEasysliderLayer
from collective.easyslider.interfaces import ISliderSettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope import schema
from zope.component import adapter
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class IEasySliderSettings(ISliderSettings):
    """ """


class EasySliderSettings(RegistryEditForm):
    schema = IEasySliderSettings
    schema_prefix = "collective.easyslider.easy_slider_settings"
    label = _("Easy Slider Settings")


EasySliderSettingsView = layout.wrap_form(EasySliderSettings, ControlPanelFormWrapper)


@adapter(Interface, ICollectiveEasysliderLayer)
class EasySliderSettingsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IEasySliderSettings
    configlet_id = "easy_slider_settings-controlpanel"
    configlet_category_id = "Products"
    title = _("Easy Slider Settings")
    group = ""
    schema_prefix = "collective.easyslider.easy_slider_settings"
