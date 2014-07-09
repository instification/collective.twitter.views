from collective.twitter.views.tweets import BaseTwitter

from plone.app.layout.viewlets.common import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TwitterViewlet(BaseTwitter, ViewletBase):
    index = ViewPageTemplateFile('twitter_viewlet.pt')
    
    def render(self):
        self.tweets = self.getSearchResults(count=3)
        return self.index()