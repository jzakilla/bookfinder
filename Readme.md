## Inventory Manager Project
This is a project that grew out of a need to create a solution for a local homeless shelter. They needed a way to track their food donations easily and quickly using a laptop and cheap ($18 on Amazon) handheld barcode scanner. Later, while looking for a book at a used book store the owner couldn't tell me if they had a certain title in stock so I came home and re-wrote this software to make it web based and easier to deploy / use.

## About
The user interface is written in HTML and CSS, and is rendered using Python 3.x and Flask. The database backend is implemented using SQLite3 on the local machine.

## Included Files
Under the libre_py directory you'll find libre.py and a directory called webify.
libre.py is a command line only, OOP version of the software.
webify includes all the files and directories needed to use the software as a standalone product that is web based.
Please note that at this time there is still a lot of work to be done on this project, and I'm already working 60+ hours a week at my normal job.


## Stretch Goals / Todo List
* Add DB auto incrementation
* Add Jira issue tracking
* Dockerize DB / Web app
* Finish CSS, improve visual appearance
* Convert to MongoDB at later date