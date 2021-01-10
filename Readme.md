## Inventory Manager Project
This is a project that grew out of a need to create a solution for a local homeless shelter. They needed a way to track their food donations easily and quickly using a laptop and cheap ($18 on Amazon) handheld barcode scanner. Later, while looking for a book at a used book store the owner couldn't tell me if they had a certain title in stock so I came home and re-wrote this software to make it web based and easier to deploy / use.

## About
The user interface is written in HTML and CSS, and is rendered using Python 3.x. The database backend is implemented using MongoDB on the local machine.

## Included Files
Under the libre_py directory you'll find libre.py and a directory called webify.
libre.py is a command line only, OOP version of the software.
webify includes all the files and directories needed to use the software as a standalone product that is web based.
Please note that at this time there is still a lot of work to be done on this project, and I'm already working 60+ hours a week at my normal job.


## Stretch Goals and Todo List
* ~~Add DB auto incrementation~~
* ~~Code functionality with radio button for stocking / sales to stocking page~~
* ~~Add sanity check on enrollment page (callable method shared by stock page?)~~
* ~~Add issue tracking~~
* Finish CSS, improve visual appearance
* Create owner dashboard
* ~~Create end user browsing pages~~
* ~~Convert to MongoDB~~
* ~~Add seperate table with business info~~
* ~~Add seperate table with users~~
* ~~Signup page~~
* Add flash feedback for all pages
* ~~Change index to choose user or owner~~
* ~~fix DB creation issues~~
* Dockerize DB ~~and Web app~~

## Usage and Installation
1.  This software can be used several different ways. The simplest is to navigate to someurl.com and sign up for a free account.
2. To use this software locally without an online account choose the method below that works best for you:
	1. Standalone using Python 3.x
		1. Install the latest version of Python 3.x for your Operating System.
		2. Install sqlite3 for your Operating System.
		3. Open Powershell or a terminal emulator. *As admin on windows*
		4. Install pip
			1. Change to your home directory and execute the following:
				1. `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
				2. `python get-pip.py`
		5. Run: `python -m pip install flask`
		6. Clone the repository for bookfinder: `git clone https://github.com/jzakilla/bookfinder.git`
		7. Set your flask app environmental variable:
			1. Windows Powershell: `$env:FLASK_APP = "\path\to\webify"`
			2. Unix/Linux/Mac: `export FLASK_APP=\path\to\webify`
		8. Start the website:
			1. For use on the local computer only: `flask run`
			2. For use on the local network: `flask run --host=0.0.0.0`
	2. Using Docker.
		1. Once created instructions for downloading and running docker image.