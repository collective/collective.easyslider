import random
from zope.interface import implements
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from collective.easyslider import easyslider_message_factory as _
from plone.portlet.collection.collection import ICollectionPortlet
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter, getUtility
from AccessControl import getSecurityManager
from plone.i18n.normalizer.interfaces import IIDNormalizer


class ICollectionSliderPortlet(ICollectionPortlet):
    """A portlet which renders the results of a collection object using a
       slider view.
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    target_collection = schema.Choice(
        title=_(u"Target collection"),
        description=_(u"Find the collection which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': 'Topic'},
            default_query='path:'))

    limit = schema.Int(
        title=_(u"Limit"),
        description=_(u"Specify the maximum number of items to show in the "
                      u"portlet. Leave this blank to show all items."),
        required=False)

    random = schema.Bool(
        title=_(u"Select random items"),
        description=_(u"If enabled, items will be selected randomly from the "
                      u"collection, rather than based on its sort order."),
        required=True,
        default=False)

    show_more = schema.Bool(
        title=_(u"Show more... link"),
        description=_(u"If enabled, a more... link will appear in the footer "
                      u"of the portlet, linking to the underlying "
                      u"Collection."),
        required=True,
        default=True)

    show_dates = schema.Bool(
        title=_(u"Show dates"),
        description=_(u"If enabled, effective dates will be shown underneath "
                      u"the items listed."),
        required=True,
        default=False)

    hide = schema.Bool(
        title=_(u"Hide portlet"),
        description=_(u"Tick this box if you want to temporarily hide "
                      "the portlet without losing your text."),
        required=True,
        default=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ICollectionSliderPortlet)

    header = _(u"title_collection_slider_portlet",
        default=u"Collection slider portlet")
    target_collection = None
    limit = None
    random = False
    show_more = True
    show_dates = False
    hide = False

    def __init__(self, header=u"", target_collection=None, limit=None,
                 random=False, show_more=True, show_dates=False, hide=False):
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.random = random
        self.show_more = show_more
        self.show_dates = show_dates
        self.hide = hide

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('collectionslider.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @property
    def available(self):
        return not self.data.hide and len(self.results())

    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return None
        else:
            return collection.absolute_url()

    def css_class(self):
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return "portlet-collection-%s" % normalizer.normalize(header)

    @memoize
    def results(self):
        if self.data.random:
            return self._random_results()
        else:
            return self._standard_results()

    def _standard_results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            limit = self.data.limit
            if limit and limit > 0:
                # pass on batching hints to the catalog
                results = collection.queryCatalog(batch=True, b_size=limit)
                results = results._sequence
            else:
                results = collection.queryCatalog()
            if limit and limit > 0:
                results = results[:limit]
        return results

    def _random_results(self):
        # intentionally non-memoized
        results = []
        collection = self.collection()
        if collection is not None:
            results = collection.queryCatalog(sort_on=None)
            if results is None:
                return []
            limit = self.data.limit and min(len(results), self.data.limit) or 1

            if len(results) < limit:
                limit = len(results)
            results = random.sample(results, limit)

        return results

    @memoize
    def collection(self):
        collection_path = self.data.target_collection
        if not collection_path:
            return None

        if collection_path.startswith('/'):
            collection_path = collection_path[1:]

        if not collection_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(collection_path, unicode):
            # restrictedTraverse accepts only strings
            collection_path = str(collection_path)

        result = portal.unrestrictedTraverse(collection_path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ICollectionSliderPortlet)
    label = _(u"title_add_collection_slider_portlet",
              default=u"Add collection slider portlet")
    description = _(u"description_collection_slider_portlet",
                    default=u"A portlet which can display a collection "
                            u"using a slider view.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ICollectionSliderPortlet)
    label = _(u"title_edit_collection_slider_portlet",
              default=u"Edit collection slider portlet")
    description = _(u"description_collection_slider_portlet",
                    default=u"A portlet which can display a collection "
                            u"using a slider view.")
