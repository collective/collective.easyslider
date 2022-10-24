# -*- coding: utf-8 -*-
from collective.easyslider import _
from collective.easyslider.interfaces import ISliderLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import adapter
from zope.interface import Interface
from zope import schema

class IEasySliderSettings(Interface):
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
                      default=u"Do you want the easy slider to show on this "
                              u"page?"),
        default=True,
        required=False,
    )

    effect = schema.Choice(
        title=_(u"label_effect_title_slider_setting", default=u"Effect Type"),
        description=_(u"label_effect_description_slider_setting",
                      default=_(u"I know the product is called easySLIDER, "
                                u"but we decided to let you choose multiple "
                                u"effects now")),
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
        required=False,
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
                      default=u"Speed at which the slide will transition for "
                              u"odd numbered slides (0 to use normal speed "
                              u"setting)."),
        default=0
    )

    auto = schema.Bool(
        title=_(u"label_auto_title_slider_setting", default=u"Auto?"),
        description=_(u"label_auto_description_slider_setting",
                      default=u"Should the slider automatically transition?"),
        required=False,
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
                              u"slides (0 to use normal pause setting)."),
        default=0
    )

    continuous = schema.Bool(
        title=_(u"label_continuous_title_slider_setting",
                default=u"Continuous?"),
        description=_(u"label_continuous_description_slider_setting",
                      default=u"Should the slider continuously loop?"),
        required=False,
        default=True
    )

    centered = schema.Bool(
        title=_(u"label_centered_title_slider_setting", default=u"Centered?"),
        description=_(u"label_centered_description_slider_setting",
                      default=u"Should the easyslider be centered?"),
        default=True,
        required=False,
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
            'Bullets Only',
            'No Buttons'
        ])
    )

    navigation_buttons_rendering_type = schema.Choice(
        title=_(u"label_navigation_buttons_rendering_type_title",
                default=u"Navigation Buttons Rendering Type"),
        description=_(u"label_navigation_buttons_rendering_type_description",
                      default=u"Only for 'Navigation Buttons' navigation "
                              u"type. Used to customize the rendering of "
                              u"navigation buttons."),
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
                      default=u"Should the navigation fade in and out when a "
                              u"user hovers of the slider?"),
        required=False,
        default=False
    )

    hover_pause = schema.Bool(
        title=_(u"label_hover_pause_title_slider_setting",
                default=u"Pause on mouseover"),
        description=_(u"label_hover_pause_description_slider_setting",
                      default=u"If this is enabled images will not change "
                              u"when mouse is over the slide"),
        required=False,
        default=False
    )

    resume_play = schema.Bool(
        title=_(u"label_resume_play_title_slider_settings",
                default=u"Resume Play"),
        description=_(u"label_replay_description_slider_settings",
                      default=u"Resume playing the slider after the user has "
                              u"manually clicked on slides (normally this "
                              u"behavior will disabling playing the slider)"),
        required=False,
        default=False
    )

    randomize = schema.Bool(
        title=_(u"label_randomize_title_slider_settings",
                default=u"Randomize"),
        description=_(u"label_randomize_desc_slider_settings",
                      default=u"Randomize slide order when playing"),
        required=False,
        default=False
    )


class EasySliderSettings(RegistryEditForm):
    schema = IEasySliderSettings
    schema_prefix = "collective.easyslider.easy_slider_settings"
    label = _("Easy Slider Settings")


EasySliderSettingsView = layout.wrap_form(
    EasySliderSettings, ControlPanelFormWrapper
)



@adapter(Interface, ISliderLayer)
class EasySliderSettingsConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = IEasySliderSettings
    configlet_id = "easy_slider_settings-controlpanel"
    configlet_category_id = "Products"
    title = _("Easy Slider Settings")
    group = ""
    schema_prefix = "collective.easyslider.easy_slider_settings"
