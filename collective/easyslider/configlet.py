from z3c.form import button
import zope.i18n
from zope.i18nmessageid import MessageFactory
from plone.app.z3cform.layout import wrap_form
from collective.easyslider.settings import EasySliderSettingsForm

_ = MessageFactory('collective.easyslider')


class EasySliderControlPanelForm(EasySliderSettingsForm):
    label = _(u"EasySlider Default Settings")
    description = _(u'Default settings to use for all Easy Sliders on site.')

    @button.buttonAndHandler(_('Apply'), name='apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        msg = changes and self.successMessage or self.noChangesMessage
        self.status = zope.i18n.translate(msg)

EasySliderControlPanelView = wrap_form(EasySliderControlPanelForm)
