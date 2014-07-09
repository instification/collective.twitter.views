from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TwitterViewlet(ViewletBase):
    index = ViewPageTemplateFile('twitter_viewlet.pt')
    
    def render(self):
        return self.index()