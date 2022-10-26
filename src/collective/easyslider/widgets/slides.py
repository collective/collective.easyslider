from collective.easyslider.utils import slider_settings_css
from persistent.mapping import PersistentMapping
from z3c.form.interfaces import IMultiWidget
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.interface import implementer_only
from zope.interface import Interface
from plone.protect.utils import addTokenToUrl
import z3c.form.widget


class PM2Obj(PersistentMapping):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError(f"No such attribute: {name}")


class ISlidesWidget(IMultiWidget):
    """ """


@implementer_only(ISlidesWidget)
class SlidesWidget(z3c.form.widget.Widget):
    template = ViewPageTemplateFile("./slides.pt")
    slider_url = ""
    settings = {}
    css = ""

    def add_token(self, url):
        return addTokenToUrl(url)

    def render(self):
        self.slider_url = self.form.context.absolute_url()
        self.settings = PM2Obj(self.context)
        self.css = slider_settings_css(self.settings)
        return self.template(self)


@implementer(z3c.form.interfaces.IFieldWidget)
def SlidesFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, SlidesWidget(request))
