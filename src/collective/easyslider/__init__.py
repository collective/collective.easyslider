from zope.i18nmessageid import MessageFactory

import logging


logger = logging.getLogger("collective.easyslider")


_ = MessageFactory("collective.easyslider")


def _patch_richtext_widgetbase():
    """Compatibility fix for some Plone 6.1 rich text widget stacks.

    In affected installations the ``richtext_input.pt`` template renders
    ``view/richtext_value`` also for the internal ``RichTextWidgetBase``
    textarea widget, but that class may not expose the attribute.  This makes
    ``@@edit-slide`` fail before the form is displayed.
    """
    try:
        from plone.app.z3cform.utils import remove_invalid_xml_characters
        from plone.app.z3cform.widgets.richtext import RichTextWidgetBase
    except ImportError:
        return

    if hasattr(RichTextWidgetBase, "richtext_value"):
        return

    def richtext_value(self):
        value = self.value
        if not value:
            return ""
        raw = getattr(value, "raw", value)
        return remove_invalid_xml_characters(raw)

    RichTextWidgetBase.richtext_value = property(richtext_value)


_patch_richtext_widgetbase()

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
