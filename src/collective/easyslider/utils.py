ORIGINAL_SCALE_NAME = "--ORIGINAL--"


def slider_settings_css(settings):
    """
    defined here because then it can be used in the widget
    and view that use the same .pt
    """
    return """
    .slider-container,
        width: %(width)ipx;
        height: %(height)ipx;
        border: %(border_width)ipx solid #f2f2f2;
        padding: %(padding)ipx;
    }
    .slider,
    .slider li.slide {
        width: %(width)ipx;
        height: %(height)ipx;
    }
    """ % {
        "width": settings.width,
        "height": settings.height,
        "border_width": settings.border_width,
        "padding": settings.padding,
    }
