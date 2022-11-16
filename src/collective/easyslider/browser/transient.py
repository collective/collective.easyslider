from collective.easyslider.interfaces import ISlideContext
from collective.easyslider.interfaces import ISlidesContext
from OFS.SimpleItem import SimpleItem
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserPublisher


@implementer(ISlideContext, IBrowserPublisher)
class SlideContext(SimpleItem):
    """
    This is a transient item that allows us to traverse through (a wrapper of)
    a slide from a wrapper of a slides list on an object
    """

    def __init__(self, context, request, index=-1):
        # super().__init__(context, request)
        self.context = context
        self.request = request
        self.index = index

    def publishTraverse(self, traverse, name):
        """shouldn't go beyond this so just call the parent"""
        return super(SlideContext, self).publishTraverse(traverse, name)

    def browserDefault(self, request):
        """Can't really traverse to anything else"""
        return self, ("@@edit",)

    def absolute_url(self):
        return self.context.absolute_url() + "/--slides--/" + str(self.index)


@implementer(ISlidesContext, IBrowserPublisher)
class SlidesContext(SimpleItem):
    """
    This is a transient item that allows us to traverse through (a wrapper of)
    a slides list on an object
    """

    def __init__(self, context, request):
        super().__init__(context, request)
        self.context = context
        self.request = request

    def publishTraverse(self, traverse, index):
        """Look up the index whose name matches the next URL and wrap it."""
        return SlideContext(self.context, self.request, int(index)).__of__(self)

    def browserDefault(self, request):
        """if nothing specified, just go to the regular slides view"""
        return self, ("@@view",)

    def absolute_url(self):
        return self.context.absolute_url() + "/--slides--"
