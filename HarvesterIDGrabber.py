'''
Created on Nov 23, 2013

@author: Daniel Piao
'''

import twiAuth
import random
from termcolor import colored

class HarvesterIDGrabber(object):
    '''
    classdocs
    ID Grabber is the object that will grab all IDs given a search string. 
    Grabber takes a location (Lat, long, radius)
    
    '''
    def getEndNum(self):
        pass
    
    def randomStart(self, startID):
        start = startID
        #start should be 253018723156381696, which is on 2012-10-02
        #end shoudl be 415486363714590720, which is on 2013, 11-28
        #TODO: Change the end date to the most current, or iSettable
        end = 415486363714590720
        mynum = random.randrange(start, end)
        #print "random number is: ", mynum
        return mynum
    
    def getLastID(self, statuses):
        status = statuses[-1]
        ID = status[u'id']        
        return ID

    def grabOneSet(self):
        API = self.API
        mygeo = self.location
        tweetID = self.lastID
        try:
            stauses = API.search_tweets(q=' ', geocode=mygeo, since_id=tweetID, lang='en', count=100)
        except (twiAuth.tweetpony.APIError, Exception) as e:
            msg = "Errror occured: " + str(e)
            print colored(msg, "red")
            self.log(msg)
            return []
        self.lastID = self.getLastID(stauses)
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
        self.lastID = self.randomStart(lastID)
        