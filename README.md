Harvester
=========

Harvester usage: 
```
python Harvester.py client
```

Distributed Crowd sourcing twitter data harvester
This app aims to make gathering tweets easier by utilizing more developer API keys. 

The credentials will never leave the client computer. 

Setup environment in <b>Linux</b>:

	You should get pip for python package management
	sudo apt-get install python-dev	
	Download libevent (https://github.com/downloads/libevent/libevent/libevent-2.0.21-stable.tar.gz)	
	unpack libevent (tar zxvf libevent)
	libevent/configure	
	sudo libevent/make	
	sudo libevent/make install	
	sudo pip install gevent


Needed packages:

	IPy (Used for checking ip addresses)	
	Termcolor (used by clients to color server messages)	
	python-twitter (Used to authenticate clients)	
	easytime (Used to log time)
	Need python-mysqldb (sudo apt-get install python-mysqldb)
	

Additional things:

	Make sure there's a "log" folder	
	Make sure there's a "IDfiles" folder
	


To setup the twitter Authentication: 

	Change the contents of the Auth file 
	
You should be ready to go at this point. 
	
