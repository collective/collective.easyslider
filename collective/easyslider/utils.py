
def slider_settings_css(settings):
    """
    defined here because then it can be used in the widget
    and view that use the same .pt
    """
    return """
    .slider-container,
    .slider,
    .slider li.slide {
        width: %(width)ipx;
        height: %(height)ipx;
    }
    """ % {
        'width' : settings.width,
        'height' : settings.height
    }


