import z3c.form.widget
from z3c.form.interfaces import IMultiWidget
from zope.interface import Interface, implementer_only
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from collective.easyslider.utils import slider_settings_css
from zope.interface import implementer
from persistent.mapping import PersistentMapping


class PM2Obj(PersistentMapping):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError(f"No such attribute: {name}")


class ISlidesWidget(IMultiWidget):
    """
    """


@implementer_only(ISlidesWidget)
class SlidesWidget(z3c.form.widget.Widget):
    template = ViewPageTemplateFile('../browser/slides.pt')
    slider_url = ""
    settings = {}
    css = ""

    def render(self):
        self.slider_url = self.form.context.absolute_url()
        self.settings = PM2Obj(self.context)
        self.css = slider_settings_css(self.settings)
        return self.template(self)

    # def hasInput(self):
    #     """
    #     data should never change here....
    #     """
    #     return False

@implementer(z3c.form.interfaces.IFieldWidget)
def SlidesFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        SlidesWidget(request))