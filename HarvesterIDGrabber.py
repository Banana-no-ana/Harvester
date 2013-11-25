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

    def grabOneSet(self, InputID):
        API = self.API
        mygeo = self.location
        tweetID = InputID
        myq = "q=geocode:" + mygeo + "&since_id:"+ str(tweetID) + "&lang=en&count=100"
        print "Searching on:", myq
        stauses = API.search(q=myq)
        print stauses
        return stauses

    def __init__(self,location):
        '''
        Constructor
        ID grabber needs a location to search on
        '''
        self.location = location
        self.TwiAuth = twiAuth.twiAuth()
        self.API = self.TwiAuth.Api
        