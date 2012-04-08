Hubway
------
The aim of this project is to solve a travelling salesman problem
around the Hubway bicycle rental stations in Boston, MA.

## Installing google or-tools ##

To install the google or-tools requires something like
[this](http://code.google.com/p/or-tools/wiki/AGettingStarted), on MacOS X:

    svn checkout http://or-tools.googlecode.com/svn/trunk/ google-or-tools
    cd google-or-tools
    cd dependencies/archives
    wget http://ftp.gnu.org/gnu/glpk/glpk-4.47.tar.gz
    wget http://download.mono-project.com/sources/mono/mono-2.10.9.tar.bz2
    cd ../../
    make third_party

You will have to accept a couple of certificates during the above step
Now to install the python modules. The first of these two lines will 
put it in your user ~/Library/Python/2.7/lib/python/site-packages/.
The second one will put it wherever pip puts stuff. Your choice:

	make install_python_modules
	pip install dependencies/sources/google-apputils/
	
At this point you can try a 

	make all

but it'll probably not find gmcs.
For some reason, mono doesn't seem to install, until you do:

	make dependencies/install/bin/gmcs

this will take a LONG time.
It still doesn't find the gmcs that you just spent ages building, until you do

	export PATH=$PATH:$PWD/dependencies/install/bin/

Now try another

	make all
	
The new tools will not be on your python path until you do something temporary like

    export PYTHONPATH=$PYTHONPATH:$PWD/src
    
Now try

    python2.7 examples/python/tsp.py