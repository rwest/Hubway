Hubway
------


To install the google or-tools requires something like
[this](http://code.google.com/p/or-tools/wiki/AGettingStarted):

    svn checkout http://or-tools.googlecode.com/svn/trunk/ google-or-tools
    cd google-or-tools
    cd dependencies/archives
    wget http://ftp.gnu.org/gnu/glpk/glpk-4.47.tar.gz
    wget http://download.mono-project.com/sources/mono/mono-2.10.9.tar.bz2
    cd ../../
    make third_party
    # you will have to accept a couple of certificates during the above step
	make install_python_modules
	# or, perhaps better (depending where you want things installing)
	pip install dependencies/sources/google-apputils/
	
	# You can try a 
	make all
	# at this point, but it'll probably not find gmcs.
	# For some reason, mono doesn't seem to install, until you do:
	make dependencies/install/bin/gmcs
	# this will take a LONG time
	# it still doesn't find the gmcs that you just built, until you do
	export PATH=$PATH:$PWD/dependencies/install/bin/
	#now this should work
	make all
	
The new things will not be on your python path until you do

    export PYTHONPATH=$PYTHONPATH:$PWD/src
    
Now try

    python2.7 examples/python/tsp.py