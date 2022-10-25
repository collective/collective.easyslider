from collective.easyslider import _ as _
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.formlib import form
from zope.interface import implements


class ISliderPortlet(IPortletDataProvider):
    """A portlet which renders predefined static HTML.

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    over = schema.Text(
        title=_("Over"),
        description=_("The cover text. You might want an image here."),
        required=True,
    )

    under = schema.Text(
        title=_("Under"),
        description=_("The text you'll see when a user hovers."),
        required=True,
    )

    height = schema.Int(
        title=_("Height"),
        description=_(
            "Required since it is difficult to know the height "
            "when using two different over and under elements."
        ),
        required=True,
        default=200,
    )

    hide = schema.Bool(
        title=_("Hide portlet"),
        description=_(
            "Tick this box if you want to temporarily hide "
            "the portlet without losing your text."
        ),
        required=True,
        default=False,
    )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ISliderPortlet)

    header = _("title_slider_portlet", default="Slider portlet")
    over = ""
    under = ""
    hide = False

    def __init__(self, over="", under="", height=200, hide=False):
        self.over = over
        self.under = under
        self.hide = hide
        self.height = height

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return "Slider Portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile("slider.pt")

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
    form_fields["over"].custom_widget = WYSIWYGWidget
    form_fields["under"].custom_widget = WYSIWYGWidget
    label = _("title_add_slider_portlet", default="Add slider portlet")
    description = _(
        "description_slider_portlet",
        default="A portlet which can display a something "
        "for the user and when they hover, it'll "
        "slide down revealing other text.",
    )

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(ISliderPortlet)
    form_fields["over"].custom_widget = WYSIWYGWidget
    form_fields["under"].custom_widget = WYSIWYGWidget
    label = _("title_edit_slider_portlet", default="Edit slider portlet")
    description = _(
        "description_slider_portlet",
        default="A portlet which can display a something "
        "for the user and when they hover, it'll "
        "slide down revealing other text.",
    )
