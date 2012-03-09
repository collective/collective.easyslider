from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.form.browser.textwidgets import IntWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from collective.easyslider.utils import slider_settings_css

class HiddenWidget(IntWidget):
    
    def __call__(self):
        return self.hidden()

class SlidesWidget(SimpleInputWidget):
    """
    this widget pretty much is the same as the Slides view
    In itself, it does not provide any data manipulatation, but
    it does provide the correct urls to perform the editing action
    for each slide
    """
    
    template = ViewPageTemplateFile('browser/slides.pt')

    def __init__(self, field, request):
        
        SimpleInputWidget.__init__(self, field, request)

        self.slider_url = self.context.context.context.absolute_url() # field/settings/context
        self.settings = self.context.context # field/settings
        self.css = slider_settings_css(self.settings) # since this uses the same .pt file

    def __call__(self):
        return self.template(self)

    def hasInput(self):
        """
        data should never change here....
        """
        return False
