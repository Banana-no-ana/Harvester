'''
Created on Nov 23, 2013

@author: Daniel Piao
'''

import twiAuth


class HarvesterIDGrabber(object):
    '''
    classdocs
    ID Grabber is the object that will grab all IDs given a search string. 
    Grabber takes a location (Lat, long, radius)
    
    '''

    def grabOneSet(self):
        API = self.API
        mygeo = self.location
        tweetID = self.lastID
        stauses = API.search_tweets(q=' ', geocode=mygeo, since_id=tweetID, lang='en', count=100)
        return stauses
    
    def testGrabbing(self):
        statuses = self.grabOneSet(111000)
        print statuses

    def __init__(self,location, lastID):
        '''
        Constructor
        ID grabber needs a location to search on
        '''
        self.location = location
        self.TwiAuth = twiAuth.twiAuth("TweetPony")
        self.API = self.TwiAuth.Api
        self.lastID = lastID
        