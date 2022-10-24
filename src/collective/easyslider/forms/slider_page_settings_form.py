# from collective.easyslider import _
from plone import schema
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button
from z3c.form import form
from zope.interface import Interface


class ISliderPageSettingsForm(Interface):
    """ Schema Interface for ISliderPageSettingsForm
        Define your form fields here.
    """
    name = schema.TextLine(
        title=u"Your name",
    )


class SliderPageSettingsForm(AutoExtensibleForm, form.EditForm):
    schema = ISliderPageSettingsForm
    ignoreContext = True

    label = u"What's your name?"
    description = u"Simple, sample form"

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here

        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        self.status = "Thank you very much {}!".format(data.get('name', ''))

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User canceled. Redirect back to the front page.
        """
