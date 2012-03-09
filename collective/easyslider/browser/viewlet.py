from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

from collective.easyslider.settings import PageSliderSettings
from collective.easyslider.interfaces import ISliderPage
from collective.easyslider.browser.base import AbstractSliderView

try:
    from collective.easytemplate.engine import getTemplateContext
    from collective.easytemplate.utils import applyTemplate
    easytemplate_installed = True
except:
    easytemplate_installed = False

import logging
logger = logging.getLogger('collective.easyslider')


class BaseSliderViewlet(ViewletBase):
    # show even if settings say not to.
    override_hidden = False

    @memoize
    def get_settings(self):
        return PageSliderSettings(self.context)

    settings = property(get_settings)

    @memoize
    def get_show(self):
        if not ISliderPage.providedBy(self.context):
            return False
        else:
            if len(self.settings.slides) == 0:
                return False
            else:
                return self.override_hidden or self.settings.show

    @property
    def slides(self):
        return self.settings.slides

    show = property(get_show)


class EasySlider(BaseSliderViewlet):

    def transform(self, text, mt='text/x-html-safe'):
        """
        Code from plone.portlet.static with adaptions
        Use the safe_html transform to protect text output. This also
        ensures that resolve UID links are transformed into real links.
        """
        #see if we have portal_transforms
        context = aq_inner(self.context)
        transformer = getToolByName(context, 'portal_transforms', None)
        if not transformer:
            return text

        orig = text
        if not isinstance(orig, unicode):
            # Don't really know if this code is needed here
            orig = unicode(orig, 'utf-8', 'ignore')
            logger.warn("Slider at %s has stored non-unicode text. "
                        "Assuming utf-8 encoding." % context.absolute_url())

        # Portal transforms needs encoded strings
        orig = orig.encode('utf-8')
        data = transformer.convertTo(mt, orig, context=context,
                                     mimetype='text/html')
        result = data.getData()

        if result:
            return unicode(result, 'utf-8')
        return u""

    def render_slide(self, slide):
        if easytemplate_installed and \
                self.settings.easytemplate_enabled:

            context = getTemplateContext(self.context, expose_schema=False)
            text, errors = applyTemplate(context, slide, logger)

            if not errors:
                slide = text

        return self.transform(slide)


class EasySliderHead(BaseSliderViewlet, AbstractSliderView):
    pass
