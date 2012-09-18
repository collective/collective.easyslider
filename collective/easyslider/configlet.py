from z3c.form import field
from z3c.form import form
from plone.app.z3cform.layout import wrap_form
from collective.easyslider.interfaces import ISliderSettings
from collective.easyslider import easyslider_message_factory as _


class EasySliderSettingsForm(form.EditForm):
    """
    The page that holds all the slider settings
    """

    fields = field.Fields(ISliderSettings)


EasySliderSettingsView = wrap_form(EasySliderSettingsForm)


class EasySliderControlPanelForm(EasySliderSettingsForm):
    label = _(u"EasySlider Default Settings")
    description = _(u'Default settings to use for all Easy Sliders on site.')

EasySliderControlPanelView = wrap_form(EasySliderControlPanelForm)
