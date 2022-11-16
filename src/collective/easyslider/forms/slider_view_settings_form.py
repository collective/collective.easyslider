from collective.easyslider import _
from collective.easyslider.interfaces import IViewSliderSettings
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


class ISliderViewSettingsForm(IViewSliderSettings):
    """Schema Interface for ISliderViewSettingsForm"""

    directives.widget("slides", SlidesFieldWidget)

    # model.fieldset(
    #     "default",
    #     label="Default",
    #     fields=[
    #         "slides",
    #     ],
    # )

    model.fieldset(
        "settings",
        label="Settings",
        fields=[
            "width",
            "height",
            "border_width",
            "padding",
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
            "allowed_types",
            "limit",
            "image_scale",
            "hidetext",
        ],
    )


class SliderViewSettingsForm(AutoExtensibleForm, form.EditForm):
    schema = ISliderViewSettingsForm
    ignoreContext = False

    label = _("heading_slider_settings_form", default="Slider Settings")
    description = _(
        "description_slider_settings_form",
        default="Configure the parameters for this slider.",
    )

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
        changes = self.applyChanges(data)
        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        if changes:
            self.status = "Settings saved"

    @button.buttonAndHandler("Cancel")
    def handleCancel(self, action):
        """User canceled. Redirect back to the front page."""
