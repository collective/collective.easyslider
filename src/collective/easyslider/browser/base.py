from plone.memoize.view import memoize


class AbstractSliderView(object):
    """
    must have settings attribute specified
    """

    @property
    @memoize
    def uid(self):
        try:
            return self.context.UID()
        except AttributeError:
            return "nouid"

    def css(self):
        width = self.settings.width or 0
        height = self.settings.height or 0
        try:
            border_width = self.settings.border_width
        except AttributeError:
            border_width = 0

        try:
            padding = self.settings.padding
        except AttributeError:
            padding = 0

        css_str = """
#slider-container.slider-%(uid)s{
    width: %(width)ipx;
    height: %(height)ipx;
    margin: %(centered)s;
    border: %(border_width)ipx solid #f2f2f2;
    padding: %(padding)ipx;
}
#slider.slider-%(uid)s, #slider.slider-%(uid)s li.slide{
    width:%(slider_width)ipx;
    height:%(slider_height)ipx;
}
.slider-%(uid)s #nextBtn{
    left:%(slider_width)ipx;
    top:-%(next_top)ipx
}
.slider-%(uid)s #prevBtn{
    top:-%(prev_top)ipx;
}
    """ % {
            "width": self.settings.width,
            "height": self.settings.height,
            "next_top": ((self.settings.height / 2) + 75) + 50,
            "prev_top": ((self.settings.height / 2) + 50),
            "centered": self.settings.centered and "auto" or "0",
            "uid": self.uid,
            "border_width": border_width,
            "padding": padding,
            "slider_width": width - (2*border_width) - (2*padding),
            "slider_height": height - (2*border_width) - (2*padding),
        }
        return css_str

    def js(self):
        return """
jQuery(document).ready(function(){
    jQuery("#slider.slider-%(uid)s").easySlider({
        speed : %(speed)i,
        odd_speed : %(odd_speed)i,
        vertical: %(vertical)s,
        auto : %(auto)s,
        pause : %(pause)i,
        odd_pause : %(odd_pause)i,
        continuous : %(continuous)s,
        navigation_type: '%(navigation_type)s',
        effect: '%(effect)s',
        fadeNavigation: %(fade_navigation)s,
        navigation_buttons_rendering_type:
            '%(navigation_buttons_rendering_type)s',
        resume_play: %(resume_play)s,
        randomize: %(randomize)s,
        hoverPause: %(hover_pause)s
    });
});
        """ % {
            "speed": self.settings.speed,
            "odd_speed": self.settings.odd_speed,
            "vertical": str(self.settings.vertical).lower(),
            "auto": str(self.settings.auto).lower(),
            "pause": self.settings.pause,
            "odd_pause": self.settings.odd_pause,
            "continuous": str(self.settings.continuous).lower(),
            "navigation_type": self.settings.navigation_type,
            "effect": self.settings.effect,
            "fade_navigation": str(self.settings.fade_navigation).lower(),
            "uid": self.uid,
            "navigation_buttons_rendering_type": self.settings.navigation_buttons_rendering_type.lower(),
            "resume_play": str(self.settings.resume_play).lower(),
            "randomize": str(self.settings.randomize).lower(),
            "hover_pause": str(self.settings.hover_pause).lower(),
        }
