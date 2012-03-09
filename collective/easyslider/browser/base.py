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
            return 'nouid'

    def css(self):
        return """
#slider-container.slider-%(uid)s{
    width: %(width)ipx;
    height: %(height)ipx;
    margin: %(centered)s;
}
#slider.slider-%(uid)s, #slider.slider-%(uid)s li.slide{
    width:%(width)ipx;
    height:%(height)ipx;
}
.slider-%(uid)s #nextBtn{
    left:%(width)ipx;
    top:-%(next_top)ipx
}
.slider-%(uid)s #prevBtn{
    top:-%(prev_top)ipx;
}
    """ % {
                'width': self.settings.width,
                'height': self.settings.height,
                'next_top': ((self.settings.height / 2) + 75) + 50,
                'prev_top': ((self.settings.height / 2) + 50),
                'centered': self.settings.centered and 'auto' or '0',
                'uid': self.uid
            }

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
        randomize: %(randomize)s
    });
});
        """ % {
            'speed': self.settings.speed,
            'odd_speed': self.settings.odd_speed,
            'vertical': str(self.settings.vertical).lower(),
            'auto': str(self.settings.auto).lower(),
            'pause': self.settings.pause,
            'odd_pause': self.settings.odd_pause,
            'continuous': str(self.settings.continuous).lower(),
            'navigation_type': self.settings.navigation_type,
            'effect': self.settings.effect,
            'fade_navigation': str(self.settings.fade_navigation).lower(),
            'uid': self.uid,
            'navigation_buttons_rendering_type':
                self.settings.navigation_buttons_rendering_type.lower(),
            'resume_play': str(self.settings.resume_play).lower(),
            'randomize': str(self.settings.randomize).lower()
        }
