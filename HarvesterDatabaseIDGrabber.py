'''
Created on Dec 30, 2013

@author: root
'''

class HarvesterDatabaseIDGrabber(object):
    '''
    classdocs
    '''
    def log(self, msg):
        self.myClient.log(msg)
        
    def log2(self, msg):
        self.myClient.log2(msg)
    
    def getDBconnection(self):
        db = self.myClient.connectToDB()
        return db
    
    def parseRow(self, row):
        ID = row[0]
        Frequency = row[6]
        
        return ID, Frequency
    
    def closeDBConnection(self):
        self.dbConnection.close()
    
    def grabIDRow(self):
        cursor = self.getDBCurosr() 
        cursor.execute("SELECT * FROM UserID2 WHERE NotScanned=0 LIMIT 1")
        self.log2("[DB ID Grabber] Selected 1 rows from the Twitter Users database")
        row = cursor.fetchone()
        cursor.close()
         
        return row
    
    def updateRowIntoDatabase(self, ID):
        cursor = self.getDBCurosr()
        #TODO: Have a way to set the database tables
        cursor.execute("Update UserID2 SET NotScanned=1 Where UserID=%s ;", str(ID))
        
        logmsg = self.myName + "got the userID: " + str(ID) + " Updated that into database now"
        self.log2(logmsg)
        
        self.dbConnection.commit()
        cursor.close()   
    
    def getDBCurosr(self):
        return self.dbConnection.cursor()
        
    def __init__(self, Client, name):
        '''
        Constructor
        '''
        self.myClient = Client
        self.myName = name
        self.dbConnection = self.getDBconnection()
       
        