from collective.easyslider.interfaces import ISliderPage
from collective.easyslider.interfaces import ISliderSettings
from collective.easyslider.interfaces import ISliderUtil
from collective.easyslider.interfaces import ISliderUtilProtected
from persistent.mapping import PersistentMapping
from plone.app.customerize import registration
from plone.protect.interfaces import IDisableCSRFProtection
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import noLongerProvides
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.viewlet.interfaces import IViewlet


@implementer(ISliderUtilProtected)
class SliderUtilProtected(BrowserView):
    """
    a protected traverable utility for
    enabling and disabling sliders
    """

    def init_default_settings(self):
        registry = getUtility(IRegistry)
        annotations = IAnnotations(self.context)
        settings = annotations.get("collective.easyslider", None)
        if settings:
            return
        defaults = PersistentMapping()
        field_names = self._get_field_names_from_schema()
        for k in field_names:
            defaults[k] = registry.get(
                "collective.easyslider.easy_slider_settings.{}".format(k)
            )
        defaults["slides"] = []
        annotations["collective.easyslider"] = defaults

    def _get_field_names_from_schema(self):
        names = ISliderSettings.names()
        return names

    def enable(self):
        utils = getToolByName(self.context, "plone_utils")

        if utils.browserDefault(self.context)[1][0] == "sliderview":
            utils.addPortalMessage(
                "You can not add a slider to a page with a" "Slider view already!"
            )
            self.request.response.redirect(self.context.absolute_url())

        elif not ISliderPage.providedBy(self.context):
            alsoProvides(self.request, IDisableCSRFProtection)
            alsoProvides(self.context, ISliderPage)
            self.context.reindexObject(idxs=["object_provides"])
            self.init_default_settings()
            utils.addPortalMessage(
                "You have added a slider to this page. "
                " To customize, click the 'Slider "
                "Settings' button."
            )
            self.request.response.redirect(
                "%s/@@slider-settings" % (self.context.absolute_url())
            )
        else:
            self.request.response.redirect(self.context.absolute_url())

    def disable(self):
        utils = getToolByName(self.context, "plone_utils")

        if ISliderPage.providedBy(self.context):
            noLongerProvides(self.context, ISliderPage)
            self.context.reindexObject(idxs=["object_provides"])

            # now delete the annotation
            annotations = IAnnotations(self.context)
            metadata = annotations.get("collective.easyslider", None)
            if metadata is not None:
                del annotations["collective.easyslider"]

            utils.addPortalMessage("Slider removed.")

        self.request.response.redirect(self.context.absolute_url())


@implementer(ISliderUtil)
class SliderUtil(BrowserView):
    """
    a public traverable utility that checks if a
    slide is enabled
    """

    def enabled(self):
        return ISliderPage.providedBy(self.context)

    def view_enabled(self):
        utils = getToolByName(self.context, "plone_utils")
        try:
            return utils.browserDefault(self.context)[1][0] == "sliderview"
        except:
            return False

    def should_include(self):
        return self.enabled() or self.view_enabled()

    def get_viewlet(self, name, context=None):
        if context is None:
            context = self.context

        views = registration.getViews(IBrowserRequest)
        viewlet = None
        for v in views:
            if v.provided == IViewlet and v.name == name:
                viewlet = v
                break
        factory = viewlet.factory
        try:
            return factory(context, self.request, self, None).__of__(context)
        except:
            return None

    def render_slider_resources(self):
        return """
<style type="text/css" media="screen">
@import url(%(url)s/++resource++easySlider.css);</style>
<script type="text/javascript" src="%(url)s/++resource++easySlider.js">
</script>
        """ % {
            "url": self.context.absolute_url()
        }

    def render_inline(self, context=None):
        if context is None:
            context = self.context
        slider = self.get_viewlet("collective.easyslider", context)
        slider.override_hidden = True
        head = self.get_viewlet("collective.easyslider.head", context)
        head.override_hidden = True
        return "%s\n%s\n%s" % (
            self.render_slider_resources(),
            head.render(),
            slider.render(),
        )

    def render_sliderview_inline(self, context=None):
        if context is None:
            context = self.context
        sliderview = getMultiAdapter((context, self.request), name="sliderview")
        sliderview = sliderview.__of__(context)
        return sliderview.sliderinline_template(sliderview=sliderview)
