# from zope.formlib import form
from collective.easyslider import _ as _
from collective.easyslider.interfaces import IPageSliderSettings
from collective.easyslider.interfaces import ISlide
from collective.easyslider.interfaces import ISliderPage
from collective.easyslider.interfaces import IViewSliderSettings
from collective.easyslider.settings import PageSliderSettings
from collective.easyslider.widgets import HiddenWidget
from collective.easyslider.widgets import SlidesWidget
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from plone.app.form import base as ploneformbase
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements

import zope.lifecycleevent


class AddSlideAdapter(SchemaAdapterBase):
    """
    This is getting a little ugly....  Store index
    in the request.
    """

    adapts(ISliderPage)
    implements(ISlide)

    def __init__(self, context):
        super(AddSlideAdapter, self).__init__(context)

        self.settings = PageSliderSettings(context)
        self.request = context.REQUEST

    def get_slide(self):
        if self.index == -1:  # creating new
            return ""
        else:
            val = self.settings.slides[self.index]
            if isinstance(val, str):
                return val
            elif isinstance(val, dict) and "html" in val:
                return val["html"]
        return ""

    def set_slide(self, value):
        """
        saved in the form handler since there is no real store
        for the index
        """
        pass

    slide = property(get_slide, set_slide)

    def get_overlay(self):
        if self.index == -1:  # creating new
            return ""
        else:
            val = self.settings.slides[self.index]
            if isinstance(val, dict) and "overlay" in val:
                return val["overlay"]
        return ""

    def set_overlay(self, value):
        """
        saved in the form handler since there is no real store
        for the index
        """
        pass

    overlay = property(get_overlay, set_overlay)

    def get_on_hover(self):
        if self.index == -1:  # creating new
            return False
        else:
            val = self.settings.slides[self.index]
            if isinstance(val, dict) and "on_hover" in val:
                return val["on_hover"]
        return False

    def set_on_hover(self, value):
        """
        saved in the form handler since there is no real store
        for the index
        """
        pass

    on_hover = property(get_on_hover, set_on_hover)

    def get_index(self):
        return int(self.request.get("index", "-1"))

    def set_index(self, value):
        pass

    index = property(get_index, set_index)


class AddSlideForm(ploneformbase.EditForm):
    """
    The add/edit form for a slide
    """

    form_fields = form.FormFields(ISlide)
    form_fields["slide"].custom_widget = WYSIWYGWidget
    form_fields["overlay"].custom_widget = WYSIWYGWidget
    form_fields["index"].custom_widget = HiddenWidget

    label = _("heading_add_slide_form", default="")
    description = _("description_add_slide_form", default="")
    form_name = _("title_add_slide_form", default="Add/Update Slide")

    @form.action(
        _("label_save", default="Save"), condition=form.haveInputWidgets, name="save"
    )
    def handle_save_action(self, action, data):
        if form.applyChanges(self.context, self.form_fields, data, self.adapters):
            zope.event.notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
            zope.event.notify(ploneformbase.EditSavedEvent(self.context))
            self.status = "Changes saved"
        else:
            zope.event.notify(ploneformbase.EditCancelledEvent(self.context))
            self.status = "No changes"

        settings = PageSliderSettings(self.context)
        slides = settings.slides
        index = data.get("index", -1)
        value = {
            "html": data["slide"],
            "overlay": data["overlay"],
            "on_hover": data["on_hover"],
        }

        if index == -1:
            slides.append(value)
            index = len(slides) - 1
        else:
            slides[index] = value

        settings.slides = slides

        url = (
            getMultiAdapter((self.context, self.request), name="absolute_url")()
            + "/@@slider-settings"
        )
        self.request.response.redirect(url)


class SliderPageSettingsForm(ploneformbase.EditForm):
    """
    The page that holds all the slider settings
    """

    form_fields = form.FormFields(IPageSliderSettings)
    # our revised SlidesWidget that only displays slides really
    form_fields["slides"].custom_widget = SlidesWidget

    label = _("heading_slider_settings_form", default="Slider Settings")
    description = _(
        "description_slider_settings_form",
        default="Configure the parameters for this slider.",
    )
    form_name = _("title_slider_settings_form", default="Slider settings")


class SliderViewSettingsForm(ploneformbase.EditForm):
    """
    The page that holds all the slider settings
    """

    form_fields = form.FormFields(IViewSliderSettings)
    # our revised SlidesWidget that only displays slides really
    form_fields["allowed_types"].custom_widget = MultiCheckBoxVocabularyWidget

    label = _("heading_slider_settings_form", default="Slider Settings")
    description = _(
        "description_slider_settings_form",
        default="Configure the parameters for this slider.",
    )
    form_name = _("title_slider_settings_form", default="Slider settings")
