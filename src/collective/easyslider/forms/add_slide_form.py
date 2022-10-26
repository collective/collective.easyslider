from collective.easyslider import _
from collective.easyslider.settings import PageSliderSettings
# from plone import schema
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button
from z3c.form import form
# from zope.interface import Interface
from collective.easyslider.interfaces import ISlide
from zope.component import getMultiAdapter


class IAddSlideForm(ISlide):
    """Schema Interface for IAddSlideForm
    """


class AddSlideForm(AutoExtensibleForm, form.EditForm):
    schema = IAddSlideForm
    ignoreContext = True

    label = _(u'heading_add_slide_form', default=u"")
    description = _(u'description_add_slide_form', default=u"")

    #def handle_save_action(self, action, data):
    #    if form.applyChanges(self.context, self.form_fields, data, self.adapters):
    #        zope.event.notify(zope.lifecycleevent.ObjectModifiedEvent(self.context))
    #        zope.event.notify(ploneformbase.EditSavedEvent(self.context))
    #        self.status = "Changes saved"
    #    else:
    #        zope.event.notify(ploneformbase.EditCancelledEvent(self.context))
    #        self.status = "No changes"


    @button.buttonAndHandler("Ok")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        settings = PageSliderSettings(self.context)
        import pdb; pdb.set_trace()  # NOQA: E702
        slides = settings.slides
        index = self.request.get("index", -1)
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
        # if changes:
        #     self.status = "Settings saved"
        self.request.response.redirect(url)

    @button.buttonAndHandler("Cancel")
    def handleCancel(self, action):
        """User canceled. Redirect back to the front page."""
