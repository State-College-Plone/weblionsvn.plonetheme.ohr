from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.layout.viewlets import common
from AccessControl import getSecurityManager
from urllib import quote_plus
from Acquisition import aq_acquire, aq_inner

class SiteActionsViewlet(ViewletBase):
    render = ViewPageTemplateFile('templates/site_actions.pt')
    
    def update(self):
        super(SiteActionsViewlet, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        
        sm = getSecurityManager()

        self.user_actions = context_state.actions().get('user', None)

        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor

        self.anonymous = self.portal_state.anonymous()
        context_state = getMultiAdapter((self.context, self.request),
                             name=u'plone_context_state')
        self.site_actions = context_state.actions().get('site_actions', None)

    
class FooterViewlet(ViewletBase):
    render = ViewPageTemplateFile('templates/footer.pt')

class PathBarViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/path_bar.pt')

    def update(self):
        super(PathBarViewlet, self).update()
        
        self.navigation_root_url = self.portal_state.navigation_root_url()

        self.is_rtl = self.portal_state.is_rtl()

        breadcrumbs_view = getMultiAdapter((self.context, self.request),
                                           name='breadcrumbs_view')
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()


    
class PersonalBarViewlet(ViewletBase):
    render = ViewPageTemplateFile('templates/personal_bar.pt')

    def update(self):
        super(PersonalBarViewlet, self).update()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        
        sm = getSecurityManager()

        self.user_actions = context_state.actions().get('user', None)

        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor

        self.anonymous = self.portal_state.anonymous()

        if not self.anonymous:
        
            member = self.portal_state.member()
            userid = member.getId()
            
            if sm.checkPermission('Portlets: Manage own portlets', self.context):
                self.homelink_url = self.site_url + '/dashboard'
            else:
                self.homelink_url = self.site_url + '/author/' + quote_plus(userid)
            
            member_info = tools.membership().getMemberInfo(member.getId())
            # member_info is None if there's no Plone user object, as when
            # using OpenID.
            if member_info:
                fullname = member_info.get('fullname', '')
            else:
                fullname = None
            if fullname:
                self.user_name = fullname
            else:
          		self.user_name = userid

