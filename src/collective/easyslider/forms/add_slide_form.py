from collective.easyslider import _
from collective.easyslider.interfaces import ISlide
from collective.easyslider.settings import PageSliderSettings
from plone.app.textfield.value import RichTextValue
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button
from z3c.form import form
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter

import operator


class AddSlideAdapter:
    """
    This is getting a little ugly....  Store index
    in the request.
    """

    def __init__(self, context):
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


class IAddSlideForm(ISlide):
    """Schema Interface for IAddSlideForm"""


class AddSlideForm(AutoExtensibleForm, form.EditForm):
    schema = IAddSlideForm
    ignoreContext = False

    label = _("heading_add_slide_form", default="")
    description = _("description_add_slide_form", default="")

    def updateWidgets(self, prefix=None):
        super().updateWidgets(prefix)
        index = self.request.get("eindex", -1)
        if int(index) < 0:
            return
        self.widgets["index"].value = index
        settings = PageSliderSettings(self.context)
        slides = settings.slides
        self.widgets["slide"].value = RichTextValue(
            slides[int(index)]["html"], "text/plain", "text/html"
        )
        self.widgets["overlay"].value = RichTextValue(
            slides[int(index)]["overlay"], "text/plain", "text/html"
        )
        self.widgets["on_hover"].value = (
            operator.truth(slides[int(index)]["on_hover"])
            and ["selected"]
            or ["unselected"]
        )

    def getContent(self):
        annotations = IAnnotations(self.context)
        return annotations["collective.easyslider"]

    @button.buttonAndHandler("Ok")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        settings = PageSliderSettings(self.context)
        slides = settings.slides
        index = data.get("index", -1)
        slide = data["slide"]
        overlay = data["overlay"]
        value = {
            "html": slide and slide.raw,
            "overlay": overlay and overlay.raw,
            "on_hover": data["on_hover"],
        }

        if index == -1 or index is None:
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

    @button.buttonAndHandler("Cancel")
    def handleCancel(self, action):
        """User canceled. Redirect back to the front page."""
