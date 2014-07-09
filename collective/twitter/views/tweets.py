from collective.prettydate.interfaces import IPrettyDate

from config import PROJECTNAME

from plone.registry.interfaces import IRegistry

from zope.component import getUtility
from zope.interface import alsoProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

import twitter

import logging
logger = logging.getLogger(PROJECTNAME)

class BaseTwitter(object):
    def getSearchResults(self,account=None,count=5):
        registry = getUtility(IRegistry)
        accounts = registry.get('collective.twitter.accounts', [])
        
        if len(accounts.keys())==0:
            return []
        
        if account is None:
            account = accounts.get(accounts.keys()[-1],{})
        else:
            account = accounts.get(account, {})
        results = []
    
        if account:
    
            tw = twitter.Api(consumer_key=account.get('consumer_key'),
                             consumer_secret=account.get('consumer_secret'),
                             access_token_key=account.get('oauth_token'),
                             access_token_secret=account.get('oauth_token_secret'),)
    
            try:
                results = tw.GetUserTimeline(screen_name='instification', count=count)
            except Exception, e:
                logger.info("Something went wrong: %s." % e)
                results = []
        return results


    def canEdit(self):
        return checkPermission('cmf.ModifyPortalContent', self.context)

    def getTweet(self, result):
        # We need to make URLs, hastags and users clickable.
        URL_TEMPLATE = """
        <a href="%s" target="blank_">%s</a>
        """
        HASHTAG_TEMPLATE = """
        <a href="http://twitter.com/#!/search?q=%s" target="blank_">%s</a>
        """
        USER_TEMPLATE = """
        <a href="http://twitter.com/#!/%s" target="blank_">%s</a>
        """

        full_text = result.GetText()
        split_text = full_text.split(' ')

        # Now, lets fix links, hashtags and users
        for index, word in enumerate(split_text):
            if word.startswith('@'):
                # This is a user
                split_text[index] = USER_TEMPLATE % (word[1:], word)
            elif word.startswith('#'):
                # This is a hashtag
                split_text[index] = HASHTAG_TEMPLATE % ("%23" + word[1:], word)
            elif word.startswith('http'):
                # This is a hashtag
                split_text[index] = URL_TEMPLATE % (word, word)

        return "<p>%s</p>" % ' '.join(split_text)

    def getTweetUrl(self, result):
        return "https://twitter.com/%s/status/%s" % \
            (result.user.screen_name, result.id)

    def getReplyTweetUrl(self, result):
        return "https://twitter.com/intent/tweet?in_reply_to=%s" % result.id

    def getReTweetUrl(self, result):
        return "https://twitter.com/intent/retweet?tweet_id=%s" % result.id

    def getFavTweetUrl(self, result):
        return "https://twitter.com/intent/favorite?tweet_id=%s" % result.id

    def getDate(self, result):
        date_utility = getUtility(IPrettyDate)
        date = date_utility.date(result.GetCreatedAt())
        return date

