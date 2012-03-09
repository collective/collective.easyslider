from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

def format_size(size):
    return "image_" + "".join(size).split(' ')[0]

def ImageSizesVocabulary(context):
    site = getSite()
   
    portal_properties = getToolByName(site, 'portal_properties', None)
    if 'imaging_properties' in portal_properties.objectIds():
        sizes = portal_properties.imaging_properties.getProperty('allowed_sizes')
        terms = [ SimpleTerm(value=format_size(pair), token=format_size(pair), title=pair) for pair in sizes ]
        return SimpleVocabulary(terms)
    else:
        return SimpleVocabulary([
            SimpleTerm('image_mini', 'image_mini', u"Mini"),
            SimpleTerm('image_preview', 'image_preview', 'Preview'),
            SimpleTerm('image_large', 'image_large', 'Large')
        ])