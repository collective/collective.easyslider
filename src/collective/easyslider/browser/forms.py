# from zope.formlib import form
from collective.easyslider import _ as _
# from collective.easyslider.interfaces import IPageSliderSettings
# from collective.easyslider.interfaces import ISlide
# from collective.easyslider.interfaces import ISliderPage
# from collective.easyslider.interfaces import IViewSliderSettings
from collective.easyslider.settings import PageSliderSettings
# from collective.easyslider.widgets import HiddenWidget
# from collective.easyslider.widgets import SlidesWidget
# from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget
# from plone.app.form import base as ploneformbase
# from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
# from Products.CMFDefault.formlib.schema import SchemaAdapterBase
# from zope.component import adapts
# from zope.component import getMultiAdapter
# from zope.interface import implements

# import zope.lifecycleevent


class AddSlideAdapter():
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
