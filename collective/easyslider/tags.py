try:
    from collective.templateengines.interfaces import ITag
except:
    from zope.interface import Interface as ITag

from zope.interface import implements
from zope.component import getMultiAdapter

class SliderTag(object):
    implements(ITag)
    
    def getName(self):
        return 'slider'

    def render(self, context, sliderpath, placeholder='slider-placeholder'):
        context = context.getTraversingContext()
        request = context.REQUEST
        object = context.restrictedTraverse(sliderpath, None)
        if not object:
            return placeholder

        slider_util = getMultiAdapter((object, request), name=u'slider_util')
        return slider_util.render_inline(object)

class SliderViewTag(object):
    implements(ITag)
    
    def getName(self):
        return 'sliderview'
        
    def render(self, context, sliderpath, placeholder='sliderview-placeholder'):
        context = context.getTraversingContext()
        request = context.REQUEST
        object = context.restrictedTraverse(sliderpath, None)
        if not object:
            return placeholder

        slider_util = getMultiAdapter((object, request), name=u'slider_util')
        return slider_util.render_sliderview_inline(object)
