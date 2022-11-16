ORIGINAL_SCALE_NAME = "--ORIGINAL--"


def slider_settings_css(settings):
    """
    defined here because then it can be used in the widget
    and view that use the same .pt
    """
    try:
        border_width = settings.border_width
    except AttributeError:
        border_width = 0

    try:
        padding = settings.padding
    except AttributeError:
        padding = 0

    css_str = """
    .slider-container,
        width: %(container_width)ipx;
        height: %(container_height)ipx;
        border: %(border_width)ipx solid #f2f2f2;
        padding: %(padding)ipx;
    }
    .slider,
    .slider li.slide {
        width: %(slider_width)ipx;
        height: %(slider_height)ipx;
    }
    """ % {
        "container_width": settings.width,
        "container_height": settings.height,
        "border_width": border_width,
        "padding": padding,
        "slider_width": settings.width - border_width - padding,
        "slider_height": settings.height - border_width - padding,
    }
    return css_str
