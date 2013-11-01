'''
Created on Oct 27, 2013
client commands are command objects that the client will execute. 
It's queued up by the client, and distributed to the network
@author: dan
'''
import twitter

class clientCommands(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        