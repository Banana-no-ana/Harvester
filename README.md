Harvester
=========

Harvester usage: 


Distributed Crowd sourcing twitter data harvester
This app aims to make gathering tweets easier by utilizing more developer API keys. 

The credentials will never leave the client computer. 

Setup environment:
	1. sudo apt-get install python-dev
	2. Download libevent
	3. unpack libevent with tar zxvf libevent
	4. libevent/configure
	5. sudo libevent/make
	6. sudo libevent/make install
	7. sudo pip install gevent

Needed packages:
	1. IPy (Used for checking ip addresses)
	2. Termcolor (used by clients to color server messages)
	3. python-twitter (Used to authenticate clients)
	4. easytime (Used to log time)
	5. Need pyodbc (This is the hard part)
		a. sudo pip install python-pyodbc (this might work)
	6. Need ODBC driver 
		wget ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-2.3.2.tar.gz
		tar -zxvf unixODBC-2.3.2.tar.gz
		./configure
		make
		sudo make install
	7. Need FreeTDs for pyodbc to talk with ODBC
		wget ftp://ftp.freetds.org/pub/freetds/stable/freetds-0.91.96.tar.gz
		tar -zxvf freetds-0.91.96.tar.gz
		./configure
		sudo make
		sudo make install
		

		

Additional things:
	1. Make sure there's a "log" folder
	
