from zope.i18nmessageid import MessageFactory
easyslider_message_factory = MessageFactory('collective.easyslider')

import logging
logger = logging.getLogger('collective.easyslider')

try:
    from collective.easytemplate.engine import getEngine 
    from tags import SliderTag, SliderViewTag
    engine = getEngine()
    engine.addTag(SliderTag())
    engine.addTag(SliderViewTag())
    logger.info("Installed slider easytemplate tag")
except:
    logger.info("easytemplate not installed. Can not install slider tag") 

def initialize(context):
    pass
