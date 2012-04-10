Hubway
------
The aim of this project is to solve a travelling salesman problem
around the Hubway bicycle rental stations in Boston, MA.

#[See the results at http://rwest.github.com/Hubway/](http://rwest.github.com/Hubway/)#

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
Now to install the python modules. 
The first of these three options will 
put it in your user ~/Library/Python/2.7/lib/python/site-packages/,
which you had better make sure is on your python path.
The second set of commands will put it wherever setuptools normally puts
stuff, without a `--user` flag.
The third uses pip, and puts it where pip
puts stuff, but it seems to miss the dependencies: "python-dateutil>=1.4",
"python-gflags>=1.4", "pytz>=2010".  You should only need one of the three:

	make install_python_modules
	
	cd dependencies/sources/google-apputils
	sudo python2.7 setup.py install
	cd ../../..
	
	pip install dependencies/sources/google-apputils/
	
At this point you can try a 

	make all

but it'll probably not find gmcs.
For some reason, mono doesn't seem to have been installed.
It is by no means certain that you actually need it - as we are only
interested in the python libraries not the C# ones, but if it turns out 
that you do, then this should build it:

	make dependencies/install/bin/gmcs

This will take a *LONG* time.
It still doesn't find the gmcs that you just spent ages building, until you do

	export PATH=$PATH:$PWD/dependencies/install/bin/

Now try another

	make all
	
The new tools will not be on your python path until you do something temporary like

    export PYTHONPATH=$PYTHONPATH:$PWD/src
    
Now try

    python2.7 examples/python/tsp.py