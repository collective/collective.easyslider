from Acquisition import aq_inner, aq_parent
from persistent.mapping import PersistentMapping
from persistent.dict import PersistentDict
from collective.easyslider import _
from collective.easyslider.interfaces import ISliderSettings, IPageSliderSettings

from collective.easyslider.controlpanels.easy_slider_settings.controlpanel import IEasySliderSettings
from plone import schema
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button
from z3c.form import form
from zope.interface import Interface
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
import transaction


class ISliderPageSettingsForm(IPageSliderSettings):
    """ Schema Interface for ISliderPageSettingsForm
    """


class SliderPageSettingsForm(AutoExtensibleForm, form.EditForm):
    schema = ISliderPageSettingsForm
    ignoreContext = False

    label = _(u"heading_slider_settings_form", default=u"Slider Settings")
    description = _(
        u"description_slider_settings_form",
        default=u"Configure the parameters for this slider.",
    )
    # form_name = _(u"title_slider_settings_form", default=u"Slider settings")

    # return annotation dict as form content
    def getContent(self):
        annotations = IAnnotations(self.context)
        if "collective.easyslider" not in annotations:
            registry = getUtility(IRegistry)
            defaults = PersistentMapping()
            field_names = self.fields.keys()
            for k in field_names:
                defaults[k] = registry.get(
                    "collective.easyslider.easy_slider_settings.{}".format(k)
                )
            annotations["collective.easyslider"] = defaults
        return annotations["collective.easyslider"]

    # def updateWidgets(self, prefix=None):
    #     super().updateWidgets(prefix)
    #     annotations = IAnnotations(self.context)
    #     for widget in self.widgets.values():
    #         name = widget.name.split(".")[-1]
    #         value = annotations["collective.easyslider"][name]
    #         if name == 'slides' and value is None:
    #             value = []
    #         # if name == 'show':
    #         #     import pdb; pdb.set_trace()  # NOQA: E702
    #         widget.field.default = value

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        if changes:
            self.status = "Settings saved"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User canceled. Redirect back to the front page."""
