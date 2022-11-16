from zope.i18nmessageid import MessageFactory

import logging


logger = logging.getLogger("collective.easyslider")


_ = MessageFactory("collective.easyslider")

# try:
#     from .tags import SliderTag
#     from .tags import SliderViewTag
#     from collective.easytemplate.engine import getEngine

#     engine = getEngine()
#     engine.addTag(SliderTag())
#     engine.addTag(SliderViewTag())
#     logger.info("Installed slider easytemplate tag")
# except:
#     logger.info("easytemplate not installed. Can not install slider tag")


def initialize(context):
    pass
