from collective.easyslider import _
from collective.easyslider.interfaces import IPageSliderSettings
from collective.easyslider.widgets.slides import SlidesFieldWidget
from persistent.mapping import PersistentMapping
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from z3c.form import button
from z3c.form import form
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility


class ISliderPageSettingsForm(IPageSliderSettings):
    """Schema Interface for ISliderPageSettingsForm"""

    directives.widget("slides", SlidesFieldWidget)

    model.fieldset(
        "default",
        label="Default",
        fields=[
            "slides",
        ],
    )

    model.fieldset(
        "settings",
        label="Settings",
        fields=[
            "width",
            "height",
            "show",
            "effect",
            "vertical",
            "speed",
            "odd_speed",
            "auto",
            "pause",
            "odd_pause",
            "continuous",
            "centered",
            "navigation_type",
            "navigation_buttons_rendering_type",
            "fade_navigation",
            "hover_pause",
            "resume_play",
            "randomize",
            "sliderposition",
        ],
    )


class SliderPageSettingsForm(AutoExtensibleForm, form.EditForm):
    schema = ISliderPageSettingsForm
    ignoreContext = False

    label = _("heading_slider_settings_form", default="Slider Settings")
    description = _(
        "description_slider_settings_form",
        default="Configure the parameters for this slider.",
    )
    # form_name = _(u"title_slider_settings_form", default=u"Slider settings")

    # return annotation dict as form content
    def getContent(self):
        annotations = IAnnotations(self.context)
        if "collective.easyslider" not in annotations:
            registry = getUtility(IRegistry)
            defaults = PersistentMapping()
            field_names = list(self.fields.keys())
            for k in field_names:
                defaults[k] = registry.get(
                    "collective.easyslider.easy_slider_settings.{}".format(k)
                )
            annotations["collective.easyslider"] = defaults
        return annotations["collective.easyslider"]

    @button.buttonAndHandler("Ok")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        del data["slides"]
        changes = self.applyChanges(data)
        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        if changes:
            self.status = "Settings saved"

    @button.buttonAndHandler("Cancel")
    def handleCancel(self, action):
        """User canceled. Redirect back to the front page."""
