
ORIGINAL_SCALE_NAME = '--ORIGINAL--'


def slider_settings_css(settings):
    """
    defined here because then it can be used in the widget
    and view that use the same .pt
    """
    return """
    .slider-container,
    .slider {
        width: %(width)ipx;
        height: %(height)ipx;
    }
    .slider li.slide {
        width: %(slidewidth)ipx !important;
        height: %(height)ipx;
    }
    
    """ % {
        'width': settings.width,
        'height': settings.height,
        'slidewidth' : (settings.width) / (settings.horizontal_slides),
    }
