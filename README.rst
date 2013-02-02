Introduction
============
This product allows you to easily add an easySlider content rotator to any page on a plone site using a WYSIWYG editor to design each slide.

How-to
------
On a page, click actions -> Add Slider.  It should bring you to a slider settings page where you can modify different aspects of the slider and add/remove slides using a WYSWGY editor.  Keep in mind that the slides are fixed width so you need to specify the size you want.  Then you'll want to start adding your slides.  To do this just click ``add new slide`` near the bottom of the page.  Once you've finished adding slides and re-ordering slides, click ``save`` and you should see the slider on your page now.

You can also select a slider view for Folder and Collection content types.  Then the slider settings for that page will include settings to limit the amount of slides to have and to limit the type of slides used.

Examples
--------
Examples of this being used in the wild.

* http://www.fbi.gov/
* http://www.chicagohistory.org
* http://www.reamp.org
* http://www.rehabpro.org
* http://swca.org/

Installation
------------
* add collective.easyslider to your eggs and zcml sections
* re-run buildout
* install the product like you would any other Plone product

Uninstall
---------
* Uninstall like normal
* go to portal_setup in the zmi, click the 'import' tab, select "collective.easyslider uninstall" and click the "Import all steps" button at the bottom to perform clean up.


Easy Template Integration
-------------------------

If you'd like to add dynamic content to your slides, add collective.easytemplate
to your eggs section in buildout, re-run buildout and restart your installation.
Then in the slider settings make sure you enable Easy Template.

You can also render sliders in a Easy Template. The syntax is:

    {{ slider("../front-page") }}

And for the sliderview

    {{ sliderview("../a-collection") }}


Rendering Slider in Templates
-----------------------------

You can also easily render your slider in a page template
if you'd like even more control over how it is displayed:

    <tal:slider tal:content="structure context/../front-page/@@slider_util/render_inline" />
    
And for the sliderview

    <tal:slider tal:content="structure context/../front-page/@@slider_util/render_sliderview_inline" />


Credits and Contributions
-------------------------
* a lot of the credit for the inspiration, styling and insight into this product belongs to Espen Moe-Nilssen 
