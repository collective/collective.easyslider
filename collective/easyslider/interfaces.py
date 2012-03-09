from zope.interface import Interface, Attribute
from zope import schema
from collective.easyslider import easyslider_message_factory as _
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from OFS.interfaces import IItem


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


class ISliderSettings(Interface):
    """
    The actual slider settings
    """

    width = schema.Int(
        title=_(u'label_width_title_slider_setting', default=u"Width"),
        description=_(u"label_width_description_slider_setting", 
            default=u"The fixed width of the slider."),
        default=600,
        required=True
    )

    height = schema.Int(
        title=_(u'label_height_title_slider_setting', default=u"Height"),
        description=_(u"label_height_description_slider_setting", 
            default=u"The fixed height of the slider."),
        default=230,
        required=True
    )

    show = schema.Bool(
        title=_(u"label_show_title_slider_setting", default=u"Show it?"),
        description=_(u"label_show_description_slider_setting",
            default=u"Do you want the easy slider to show on this page?"),
        default=True,
        required=True
    )

    effect = schema.Choice(
        title=_(u"label_effect_title_slider_setting", default=u"Effect Type"),
        description=_(u"label_effect_description_slider_setting",
            default=_(u"I know the product is called easySLIDER, but we "
                      u"decided to let you choose multiple effects now")),
        default="Slide",
        vocabulary=SimpleVocabulary.fromValues([
            'Slide',
            'Fade',
            'Crossfade'
        ])
    )

    vertical = schema.Bool(
        title=_(u"label_vertical_title_slider_setting", default=u"Vertical?"),
        description=_(u"label_vertical_description_slider_setting", 
            default=u"Should the slide transition vertically?"),
        default=False
    )

    speed = schema.Int(
        title=_(u"label_speed_title_slider_setting", default=u"Speed"),
        description=_(u"label_speed_description_slider_setting",
            default=u"Speed at which the slide will transition."),
        default=800
    )

    odd_speed = schema.Int(
        title=_(u"label_odd_speed_title_slider_setting",
            default=u"Odd Slide Speed"),
        description=_(u"label_odd_speed_description_slider_setting",
            default=u"Speed at which the slide will transition for odd "
                    u"numbered slides(0 to use normal speed setting)."),
        default=0
    )

    auto = schema.Bool(
        title=_(u"label_auto_title_slider_setting", default=u"Auto?"),
        description=_(u"label_auto_description_slider_setting",
            default=u"Should the slider automatically transition?"),
        default=True
    )

    pause = schema.Int(
        title=_(u"label_pause_title_slider_setting", default=u"Pause"),
        description=_(u"label_pause_description_slider_setting",
            default=u"How long the slide should pause before it is "
                    u"automatically transitioned."),
        default=4000
    )

    odd_pause = schema.Int(
        title=_(u"label_odd_pause_title_slider_setting",
            default=u"Odd Slide Pause"),
        description=_(u"label_odd_pause_description_slider_setting",
            default=u"How long the slide should pause before it is "
                    u"automatically transitioned for odd numbered "
                    u"slides(0 to use normal pause setting)."),
        default=0
    )

    continuous = schema.Bool(
        title=_(u"label_continuous_title_slider_setting",
            default=u"Continuous?"),
        description=_(u"label_continuous_description_slider_setting",
            default=u"Should the slider continuously loop?"),
        default=True
    )

    centered = schema.Bool(
        title=_(u"label_centered_title_slider_setting", default=u"Centered?"),
        description=_(u"label_centered_description_slider_setting",
            default=u"Should the easyslider be centered?"),
        default=True
    )

    navigation_type = schema.Choice(
        title=_(u"label_navigation_type_title_slider_setting",
            default=u"Type of Navigation."),
        description=_(u"label_navigation_type_description_slider_setting",
            u"Choose the type of navigation to use."),
        default="Navigation Buttons",
        vocabulary=SimpleVocabulary.fromValues([
            'Big Arrows',
            'Small Arrows',
            'Navigation Buttons',
            'Navigation Bullets',
            'No Buttons'
        ])
    )

    navigation_buttons_rendering_type = schema.Choice(
        title=_(u"label_navigation_buttons_rendering_type_title",
            default=u"Navigation Buttons Rendering Type"),
        description=_(u"label_navigation_buttons_rendering_type_description", 
            default=u"Only for 'Navigation Buttons' navigation type. Used to "
                    u"customize the rendering of navigation buttons."),
        default=u"standard",
        vocabulary=SimpleVocabulary([
            SimpleTerm(value='standard', token='standard', title='Standard'),
            SimpleTerm(value='skip_even', token='skip_even',
                       title='Skip Even Slides'),
            SimpleTerm(value='skip_odd', token='skip_odd',
                       title='Skip Odd Slides')
        ])
    )

    fade_navigation = schema.Bool(
        title=_(u"label_fade_navigation_title_slider_settings",
            default=u"Fade Navigation?"),
        description=_(u"label_fade_navigation_description_slider_settings",
            default=u"Should the navigation fade in and out when a user "
                    u"hovers of the slider?"),
        default=False
    )

    resume_play = schema.Bool(
        title=_(u"label_resume_play_title_slider_settings",
            default=u"Resume Play"),
        description=_(u"label_replay_description_slider_settings",
            default=u"Resume playing the slider after the user has "
                    u"manually clicked on slides(normally this "
                    u"behavior will disabling playing the slider)"),
        default=False
    )

    randomize = schema.Bool(
        title=_(u"label_randomize_title_slider_settings",
            default=u"Randomize"),
        description=_(u"label_randomize_desc_slider_settings",
            default=u"Randomize slide order when playing"),
        default=False
    )


class IPageSliderSettings(ISliderSettings):
    """
    difference here is the user creates all his slides
    """
    easytemplate_enabled = schema.Bool(
        title=_(u"label_easytemplate_enabled_title_slider_setting",
            default=u"Easy Template Enabled?"),
        description=_(u"label_easytemplate_enabled_description_slider_setting",
            default=u"If collective.easytemplate is installed, this will put "
                    u"it through the rendering engine"),
        default=False
    )

    slides = schema.List(
        title=_(u"label_slides_title_slider_setting", default=u"Slides"),
        description=_(u"label_slides_description_slider_settings",
            default=u"These are the slides that will show up in the "
                    u"easySlider for this page."),
        default=[]
    )


class IViewSliderSettings(ISliderSettings):
    """
    settings for the slider view on a collection or folder
    """

    allowed_types = schema.Tuple(
        title=_(u"label_allowed_types_title_slider_setting",
            default=u'Available Slide Types'),
        description=_(u"label_allowed_types_description_slider_setting", 
            default=u"Select the types that will be show in this slider."),
        required=True,
        missing_value=None,
        default=("News Item", "Image"),
        value_type=schema.Choice(
            vocabulary=SimpleVocabulary.fromValues([
                'Image',
                'News Item'
            ])
        )
    )

    limit = schema.Int(
        title=_(u"label_limit_title_slider_setting", default=u"Max Slides"),
        description=_(u"label_limit_description_slider_setting", 
            default=u"The max amount of content items to use for slides.  "
                    u"Set to 0 for unlimited."),
        default=0
    )

    image_scale = schema.Choice(
        title=_(u"label_image_scale_title_slider_setting",
            default=u"Image Scale."),
        description=_(u"label_image_scale_description_slider_setting",
            u"Choose the scale used for this image."),
        default="image_preview",
        vocabulary='collective.easyslider.imagesizes'
    )


class ISlide(Interface):

    slide = schema.Text(
        title=_(u"label_slide_title_slider_setting", default=u"Slide")
    )

    index = schema.Int(
        title=u'',
        required=False
    )


class ISlidesContext(IItem):
    """
    Context to allow traversing to the slides list
    """


class ISlideContext(IItem):
    """
    Context to allow traversing to a slide on a ISlidesContext object
    """
    index = Attribute("""Index of the slide on the object""")
