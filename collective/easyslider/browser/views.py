from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.ATContentTypes.interface.topic import IATTopic
from Products.ATContentTypes.interface.folder import IATFolder, IATBTreeFolder

from collective.easyslider.settings import PageSliderSettings
from collective.easyslider.settings import ViewSliderSettings
from collective.easyslider.utils import slider_settings_css
from collective.easyslider.utils import ORIGINAL_SCALE_NAME
from collective.easyslider.browser.base import AbstractSliderView

try:
    from plone.app.collection.interfaces import ICollection
    from plone.app.querystring import queryparser
except ImportError:
    from zope.interface import Interface
    class ICollection(Interface):
        pass


class SliderView(BrowserView, AbstractSliderView):
    sliderinline_template = ViewPageTemplateFile('sliderview-inline.pt')

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.settings = ViewSliderSettings(context)

    @property
    def scale(self):
        scale = self.settings.image_scale
        if not scale:
            return '/image_preview'
        if scale == ORIGINAL_SCALE_NAME:
            return ''
        return '/' + scale

    def get_items(self):
        context = aq_inner(self.context)
        if IATFolder.providedBy(context) or \
                IATBTreeFolder.providedBy(context):
            res = self.context.getFolderContents(
                contentFilter={
                    'sort_on': 'getObjPositionInParent',
                    'portal_type': self.settings.allowed_types,
                    'limit': self.settings.limit
                }
            )
        elif IATTopic.providedBy(context):
            if self.settings.limit and self.settings.limit > 0:
                res = context.queryCatalog(batch=True,
                                           b_size=self.settings.limit,
                                           portal_type=
                                           self.settings.allowed_types,
                                           )
            else:
                res = context.queryCatalog(
                    portal_type=self.settings.allowed_types,
                    limit=self.settings.limit
                )
        elif ICollection.providedBy(context):
            query = queryparser.parseFormquery(
                context, context.getRawQuery())
            query['portal_type'] = self.settings.allowed_types
            query['limit'] = self.settings.limit
            if self.settings.limit and self.settings.limit > 0:
                res = context.queryCatalog(batch=True,
                                           b_size=self.settings.limit)
            else:
                res = context.queryCatalog(query)

        return res


class SlidesView(BrowserView):
    """
    View of all the slides
    This uses the same page template as the slides widget--just a different
    __init__ method to setup the call_context and css members
    """
    template = ViewPageTemplateFile('slides.pt')

    def __init__(self, context, request):
        super(SlidesView, self).__init__(context, request)

        self.settings = PageSliderSettings(context.context)
        self.call_context = self.context.context
        self.slider_url = self.context.context.absolute_url()
        # since this uses the same .pt file
        self.css = slider_settings_css(self.settings)

    def __call__(self):
        return self.template()


class SlideView(BrowserView):
    """
    For doing operations on a slide
    """

    slides_template = ViewPageTemplateFile('slides.pt')

    def __init__(self, context, request):
        super(SlideView, self).__init__(context, request)
        self.settings = PageSliderSettings(self.context.context)

    def move_up(self, ajax=None):
        index = self.context.index
        if index > 0:
            slides = self.settings.slides

            tmp = slides[index - 1]
            slides[index - 1] = slides[index]
            slides[index] = tmp

            self.settings.slides = slides

            if ajax is None:
                self.request.response.redirect(
                    self.context.context.absolute_url() + "/@@slider-settings")
            else:
                return 'done'
        else:
            self.request.response.setStatus(status=403,
                                            reason="Cannot move up")

    def move_down(self, ajax=None):
        index = self.context.index
        next_index = index + 1
        if next_index < len(self.settings.slides):
            slides = self.settings.slides

            tmp = slides[next_index]
            slides[next_index] = slides[index]
            slides[index] = tmp

            self.settings.slides = slides

            if ajax is None:
                self.request.response.redirect(
                    self.context.context.absolute_url() + "/@@slider-settings")
            else:
                return 'done'
        else:
            self.request.response.setStatus(status=403,
                                            reason="Cannot move down")

    def remove(self, ajax=None):
        index = self.context.index

        if index < len(self.settings.slides) and index >= 0:
            slides = self.settings.slides
            del slides[index]
            self.settings.slides = slides

            if ajax is None:
                self.request.response.redirect(
                    self.context.context.absolute_url() + "/@@slider-settings")
            else:
                return 'done'
        else:
            self.request.response.setStatus(status=403,
                                            reason="Cannot remove slide")


class OrderSlides(BrowserView):

    def __call__(self):
        order = [int(i) for i in self.request.get('order[]')]
        settings = PageSliderSettings(self.context)
        # first verify same size
        slides = settings.slides
        if len(order) != len(slides):
            self.request.response.setStatus(status=403,
                                            reason="missing slides")

        newslides = []
        for index in order:
            newslides.append(slides[index])

        settings.slides = newslides
        return 'done'
