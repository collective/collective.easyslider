from collective.easyslider import _ as _
from OFS.interfaces import IItem
from zope import schema
from zope.interface import Attribute
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ISliderLayer(Interface):
    """
    marker interface for slider layer
    """


class ISliderPage(Interface):
    """
    marker interface for a page that implements
    the Slider
    """


class IViewEasySlider(Interface):
    """
    marker interface for content types that can use
    easyslider view
    """


class ISliderUtilProtected(Interface):
    def enable():
        """
        enable slider on this object
        """

    def disable():
        """
        disable slider on this object
        """


class ISliderUtil(Interface):
    def enabled():
        """
        checks if slider is enabled on the peice of content
        """

    def view_enabled():
        """
        checks if the slider view is selected
        """

    def should_include():
        """
        if the slider files should be included
        """

    def render_inline(context=None):
        """
        Render a slide in a template somewhere else(a page template
        or easytemplate). Even if the slider is set to hidden, this will
        render it.
        """

    def render_sliderview_inline(context=None):
        """
        Render the slider view inline.
        """


class ISlider(Interface):
    """Marker interface"""


class ISliderSettings(Interface):
    """
    The actual slider settings
    """

    width = schema.Int(
        title=_("label_width_title_slider_setting", default="Width"),
        description=_(
            "label_width_description_slider_setting",
            default="The fixed width of the slider.",
        ),
        default=600,
        required=True,
    )

    height = schema.Int(
        title=_("label_height_title_slider_setting", default="Height"),
        description=_(
            "label_height_description_slider_setting",
            default="The fixed height of the slider.",
        ),
        default=230,
        required=True,
    )

    show = schema.Bool(
        title=_("label_show_title_slider_setting", default="Show it?"),
        description=_(
            "label_show_description_slider_setting",
            default="Do you want the easy slider to show on this " "page?",
        ),
        default=True,
        required=True,
    )

    effect = schema.Choice(
        title=_("label_effect_title_slider_setting", default="Effect Type"),
        description=_(
            "label_effect_description_slider_setting",
            default=_(
                "I know the product is called easySLIDER, "
                "but we decided to let you choose multiple "
                "effects now"
            ),
        ),
        default="Slide",
        vocabulary=SimpleVocabulary.fromValues(["Slide", "Fade", "Crossfade"]),
    )

    vertical = schema.Bool(
        title=_("label_vertical_title_slider_setting", default="Vertical?"),
        description=_(
            "label_vertical_description_slider_setting",
            default="Should the slide transition vertically?",
        ),
        required=False,
        default=False,
    )

    speed = schema.Int(
        title=_("label_speed_title_slider_setting", default="Speed"),
        description=_(
            "label_speed_description_slider_setting",
            default="Speed at which the slide will transition.",
        ),
        default=800,
    )

    odd_speed = schema.Int(
        title=_("label_odd_speed_title_slider_setting", default="Odd Slide Speed"),
        description=_(
            "label_odd_speed_description_slider_setting",
            default="Speed at which the slide will transition for "
            "odd numbered slides (0 to use normal speed "
            "setting).",
        ),
        default=0,
    )

    auto = schema.Bool(
        title=_("label_auto_title_slider_setting", default="Auto?"),
        description=_(
            "label_auto_description_slider_setting",
            default="Should the slider automatically transition?",
        ),
        required=False,
        default=True,
    )

    pause = schema.Int(
        title=_("label_pause_title_slider_setting", default="Pause"),
        description=_(
            "label_pause_description_slider_setting",
            default="How long the slide should pause before it is "
            "automatically transitioned.",
        ),
        default=4000,
    )

    odd_pause = schema.Int(
        title=_("label_odd_pause_title_slider_setting", default="Odd Slide Pause"),
        description=_(
            "label_odd_pause_description_slider_setting",
            default="How long the slide should pause before it is "
            "automatically transitioned for odd numbered "
            "slides (0 to use normal pause setting).",
        ),
        default=0,
    )

    continuous = schema.Bool(
        title=_("label_continuous_title_slider_setting", default="Continuous?"),
        description=_(
            "label_continuous_description_slider_setting",
            default="Should the slider continuously loop?",
        ),
        required=False,
        default=True,
    )

    centered = schema.Bool(
        title=_("label_centered_title_slider_setting", default="Centered?"),
        description=_(
            "label_centered_description_slider_setting",
            default="Should the easyslider be centered?",
        ),
        required=False,
        default=True,
    )

    navigation_type = schema.Choice(
        title=_(
            "label_navigation_type_title_slider_setting", default="Type of Navigation."
        ),
        description=_(
            "label_navigation_type_description_slider_setting",
            "Choose the type of navigation to use.",
        ),
        default="Navigation Buttons",
        vocabulary=SimpleVocabulary.fromValues(
            [
                "Big Arrows",
                "Small Arrows",
                "Navigation Buttons",
                "Navigation Bullets",
                "Bullets Only",
                "No Buttons",
            ]
        ),
    )

    navigation_buttons_rendering_type = schema.Choice(
        title=_(
            "label_navigation_buttons_rendering_type_title",
            default="Navigation Buttons Rendering Type",
        ),
        description=_(
            "label_navigation_buttons_rendering_type_description",
            default="Only for 'Navigation Buttons' navigation "
            "type. Used to customize the rendering of "
            "navigation buttons.",
        ),
        default="standard",
        vocabulary=SimpleVocabulary(
            [
                SimpleTerm(value="standard", token="standard", title="Standard"),
                SimpleTerm(
                    value="skip_even", token="skip_even", title="Skip Even Slides"
                ),
                SimpleTerm(value="skip_odd", token="skip_odd", title="Skip Odd Slides"),
            ]
        ),
    )

    fade_navigation = schema.Bool(
        title=_(
            "label_fade_navigation_title_slider_settings", default="Fade Navigation?"
        ),
        description=_(
            "label_fade_navigation_description_slider_settings",
            default="Should the navigation fade in and out when a "
            "user hovers of the slider?",
        ),
        required=False,
        default=False,
    )

    hover_pause = schema.Bool(
        title=_("label_hover_pause_title_slider_setting", default="Pause on mouseover"),
        description=_(
            "label_hover_pause_description_slider_setting",
            default="If this is enabled images will not change "
            "when mouse is over the slide",
        ),
        required=False,
        default=False,
    )

    resume_play = schema.Bool(
        title=_("label_resume_play_title_slider_settings", default="Resume Play"),
        description=_(
            "label_replay_description_slider_settings",
            default="Resume playing the slider after the user has "
            "manually clicked on slides (normally this "
            "behavior will disabling playing the slider)",
        ),
        required=False,
        default=False,
    )

    randomize = schema.Bool(
        title=_("label_randomize_title_slider_settings", default="Randomize"),
        description=_(
            "label_randomize_desc_slider_settings",
            default="Randomize slide order when playing",
        ),
        required=False,
        default=False,
    )


class IPageSliderSettings(ISliderSettings):
    """
    difference here is the user creates all his slides
    """

    # easytemplate_enabled = schema.Bool(
    #     title=_(u"label_easytemplate_enabled_title_slider_setting",
    #             default=u"Easy Template Enabled?"),
    #     description=_(u"label_easytemplate_enabled_description_slider_setting",
    #                   default=u"If collective.easytemplate is installed, "
    #                           u"this will put it through the rendering "
    #                           u"engine"),
    #     required=False,
    #     default=False
    # )

    sliderposition = schema.Bool(
        title=_("label_sliderposition", default="Below Content?"),
        description=_(
            "label_sliderposition",
            default="Show the slider below the content instead of above?",
        ),
        required=False,
    )

    slides = schema.List(
        title=_("label_slides_title_slider_setting", default="Slides"),
        description=_(
            "label_slides_description_slider_settings",
            default="These are the slides that will show up in the "
            "easySlider for this page.",
        ),
        value_type=schema.TextLine(
            title="",
        ),
        required=False,
        default=[],
    )


class IViewSliderSettings(ISliderSettings):
    """
    settings for the slider view on a collection or folder
    """

    allowed_types = schema.Tuple(
        title=_(
            "label_allowed_types_title_slider_setting", default="Available Slide Types"
        ),
        description=_(
            "label_allowed_types_description_slider_setting",
            default="Select the types that will be shown in this " "slider.",
        ),
        required=True,
        missing_value=None,
        default=("News Item", "Image"),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary.fromValues(["Image", "News Item"])
        ),
    )

    limit = schema.Int(
        title=_("label_limit_title_slider_setting", default="Max Slides"),
        description=_(
            "label_limit_description_slider_setting",
            default="The max amount of content items to use for "
            "slides.  Set to 0 for unlimited.",
        ),
        default=0,
    )

    image_scale = schema.Choice(
        title=_("label_image_scale_title_slider_setting", default="Image Scale."),
        description=_(
            "label_image_scale_description_slider_setting",
            "Choose the scale used for this image.",
        ),
        default="image_preview",
        vocabulary="collective.easyslider.imagesizes",
    )

    hidetext = schema.Bool(
        title=_("label_easyslider_hide_text_title", default="Hide text"),
        description=_(
            "label_easyslider_hide_text_settings",
            default="Hide Title and description text on the " "slides",
        ),
        required=False,
        default=False,
    )


class ISlide(Interface):

    slide = schema.Text(title=_("label_slide_title_slider_setting", default="Slide"))

    overlay = schema.Text(
        title=_("label_slide_overlay_slider_settings", default="Slide Overlay"),
        description=_(
            "desc_slide_overlay_slider_setting",
            default="Will be overlayed onto the bottom of slide",
        ),
        required=False,
        default="",
    )

    on_hover = schema.Bool(
        title=_(
            "label_slide_onhover_slider_settings", default="Only show overlay on hover"
        ),
        required=False,
        default=False,
    )

    index = schema.Int(title="", required=False)


class ISlidesContext(IItem):
    """
    Context to allow traversing to the slides list
    """


class ISlideContext(IItem):
    """
    Context to allow traversing to a slide on a ISlidesContext object
    """

    index = Attribute("""Index of the slide on the object""")
