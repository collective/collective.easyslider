from OFS.SimpleItem import SimpleItem
from zope.publisher.interfaces.browser import IBrowserPublisher
from collective.easyslider.interfaces import ISlideContext, ISlidesContext
from zope.interface import implements

class SlideContext(SimpleItem):
    """ 
    This is a transient item that allows us to traverse through (a wrapper of) a slide
    from a wrapper of a slides list on an object
    """
    # Implementing IBrowserPublisher tells the Zope 2 publish traverser to pay attention
    # to the publishTraverse and browserDefault methods.
    implements(ISlideContext, IBrowserPublisher)
    
    def __init__(self, context, request, index=-1):
        super(SlideContext, self).__init__(context, request)
        self.context = context
        self.request = request
        self.index = index
    
    def publishTraverse(self, traverse, name):
        """ shouldn't go beyond this so just call the parent
        """
        return super(SlideContext, self).publishTraverse(traverse, name)
    
    def browserDefault(self, request):
        """ Can't really traverse to anything else
        """
        return self, ('@@edit',)
        
    def absolute_url(self):
        return self.context.absolute_url() + "/--slides--/" + str(self.index)
    
    
class SlidesContext(SimpleItem):
    """ 
    This is a transient item that allows us to traverse through (a wrapper of) a slides
    list on an object
    """
    # Implementing IBrowserPublisher tells the Zope 2 publish traverser to pay attention
    # to the publishTraverse and browserDefault methods.
    implements(ISlidesContext, IBrowserPublisher)
    
    def __init__(self, context, request):
        super(SlidesContext, self).__init__(context, request)
        self.context = context
        self.request = request
    
    def publishTraverse(self, traverse, index):
        """ Look up the index whose name matches the next URL and wrap it.
        """
        return SlideContext(self.context, self.request, int(index)).__of__(self)
    
    def browserDefault(self, request):
        """ if nothing specified, just go to the regular slides view
        """
        return self, ('@@view',)
        
    def absolute_url(self):
        return self.context.absolute_url() + "/--slides--"