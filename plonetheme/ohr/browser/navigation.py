from plone.app.portlets.portlets.navigation import Renderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName

class MyRenderer(Renderer):
    _template = ViewPageTemplateFile('templates/navigation.pt')
    recurse = ViewPageTemplateFile('templates/navigation_recurse.pt')
    
    @memoize
    def getMetaTypesNotToList(self):
        context = self.context
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        return list(navtree_properties.metaTypesNotToList)

    @memoize
    def getIdsNotToList(self):
        context = self.context
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        return list(navtree_properties.idsNotToList)