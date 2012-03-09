from zope.interface import implements
from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

from collective.easyslider import easyslider_message_factory as _


class ISliderPortlet(IPortletDataProvider):
    """A portlet which renders predefined static HTML.

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    over = schema.Text(
        title=_(u"Over"),
        description=_(u"The cover text. You might want an image here."),
        required=True)
        
    under = schema.Text(
        title=_(u"Under"),
        description=_(u"The text you'll see when a user hovers."),
        required=True)

    height = schema.Int(
        title=_(u"Height"),
        description=_(u"Required since it is difficult to know the height "
                      u"when using two different over and under elements."),
        required=True,
        default=200
    )

    hide = schema.Bool(
        title=_(u"Hide portlet"),
        description=_(u"Tick this box if you want to temporarily hide "
                      "the portlet without losing your text."),
        required=True,
        default=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ISliderPortlet)

    header = _(u"title_slider_portlet", default=u"Slider portlet")
    over = u""
    under = u""
    hide = False

    def __init__(self, over=u"", under=u"", height=200, hide=False):
        self.over = over
        self.under = under
        self.hide = hide
        self.height = height

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return u"Slider Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('slider.pt')

    @property
    def available(self):
        return not self.data.hide

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ISliderPortlet)
    form_fields['over'].custom_widget = WYSIWYGWidget
    form_fields['under'].custom_widget = WYSIWYGWidget
    label = _(u"title_add_slider_portlet",
              default=u"Add slider portlet")
    description = _(u"description_slider_portlet",
                    default=u"A portlet which can display a something "
                            u"for the user and when they hover, it'll "
                            u"slide down revealing other text.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ISliderPortlet)
    form_fields['over'].custom_widget = WYSIWYGWidget
    form_fields['under'].custom_widget = WYSIWYGWidget
    label = _(u"title_edit_slider_portlet",
              default=u"Edit slider portlet")
    description = _(u"description_slider_portlet",
                    default=u"A portlet which can display a something "
                            u"for the user and when they hover, it'll "
                            u"slide down revealing other text.")