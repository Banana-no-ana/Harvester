Harvester
=========

Harvester usage: 
```
python Harvester.py client
```

Distributed Crowd sourcing twitter data harvester
This app aims to make gathering tweets easier by utilizing more developer API keys. 

The credentials will never leave the client computer. 

Setup environment in <b>Linux</b> (these steps will work for a fresh install on ubuntu 12.04 or ubuntu 13):

You should get pip for python package management

	sudo apt-get install python-dev	

Download and install libevent:
	
	download link: https://github.com/downloads/libevent/libevent/libevent-2.0.21-stable.tar.gz

Unpack libevent:

	cd to location where you downloaded libevent-2.0.21-stable.tar.gz
	tar zxvf libevent-2.0.21-stable.tar.gz
	sudo ./libevent-2.0.21-stable/configure
	sudo ./libevent-2.0.21-stable/make
	sudo ./libevent-2.0.21-stable/make install
	sudo pip install gevent

Needed packages:

	sudo pip install IPy (Used for checking ip addresses)	
	sudo pip install Termcolor (used by clients to color server messages)	
	sudo pip install python-twitter (Used to authenticate clients)	
	sudo pip install easytime (Used to log time)
	sudo apt-get install python-mysqldb (Need python-mysqldb)
	

Additional things:

	Make sure there's a "log" folder	
	Make sure there's a "IDfiles" folder	

To setup the twitter Authentication: 
Change the contents of the Auth file. AuthFile lines are tab delimited and have the form:

	Consumer_key	YYYYYYYYYYYYYYYYYYYYY
	Consumer_secret	ttttttttttttttttttttttttttttttttttttttttttt
	Access_token	222222222-oooooooooooooooooooooooooooooooooooooooo
	Access_token_secret	RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
	
You should be ready to go at this point. 
	
