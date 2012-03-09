from zope.formlib import form
from zope.interface import implements
from zope.component import adapts
import zope.lifecycleevent
from zope.component import getMultiAdapter

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
from plone.app.form import base as ploneformbase
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget

from collective.easyslider.interfaces import ISliderPage, ISlide, \
    IPageSliderSettings, IViewSliderSettings
from collective.easyslider import easyslider_message_factory as _
from collective.easyslider.widgets import SlidesWidget, HiddenWidget
from collective.easyslider.settings import PageSliderSettings

    
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
        if self.index == -1: # creating new
            return ""
        else:
            return self.settings.slides[self.index]

    def set_slide(self, value):
        """
        saved in the form handler since there is no real store
        for the index
        """
        pass

    slide = property(get_slide, set_slide)

    def get_index(self):
        return int(self.request.get('index', '-1'))
        
    def set_index(self, value):
        pass
        
    index = property(get_index, set_index)

class AddSlideForm(ploneformbase.EditForm):
    """
    The add/edit form for a slide
    """
    form_fields = form.FormFields(ISlide)
    form_fields['slide'].custom_widget = WYSIWYGWidget
    form_fields['index'].custom_widget = HiddenWidget
    
    label = _(u'heading_add_slide_form', default=u"")
    description = _(u'description_add_slide_form', default=u"")
    form_name = _(u'title_add_slide_form', default=u"Add/Update Slide")
    
    @form.action(_(u"label_save", default="Save"),
                 condition=form.haveInputWidgets,
                 name=u'save')
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
        index = data.get('index', -1)
        value = data['slide']
        
        if index == -1:
            slides.append(value)
            index = len(slides) - 1
        else:
            slides[index] = value

        settings.slides = slides
        
        url = getMultiAdapter((self.context, self.request), name='absolute_url')() + "/@@slider-settings"
        self.request.response.redirect(url)
        

class SliderPageSettingsForm(ploneformbase.EditForm):
    """
    The page that holds all the slider settings
    """
    form_fields = form.FormFields(IPageSliderSettings)
    #our revised SlidesWidget that only displays slides really
    form_fields['slides'].custom_widget = SlidesWidget 

    label = _(u'heading_slider_settings_form', default=u"Slider Settings")
    description = _(u'description_slider_settings_form', default=u"Configure the parameters for this slider.")
    form_name = _(u'title_slider_settings_form', default=u"Slider settings")
    
        
class SliderViewSettingsForm(ploneformbase.EditForm):
    """
    The page that holds all the slider settings
    """
    form_fields = form.FormFields(IViewSliderSettings)
    #our revised SlidesWidget that only displays slides really
    form_fields['allowed_types'].custom_widget = MultiCheckBoxVocabularyWidget 

    label = _(u'heading_slider_settings_form', default=u"Slider Settings")
    description = _(u'description_slider_settings_form', default=u"Configure the parameters for this slider.")
    form_name = _(u'title_slider_settings_form', default=u"Slider settings")
    