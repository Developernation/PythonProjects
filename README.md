# Sans Notes and Indexing App

 <img width="569" alt="Screen Shot 2022-02-12 at 12 29 36 AM" src="https://user-images.githubusercontent.com/16394280/153698363-d1e68fc1-ae82-4879-968a-b0d756b543f7.png">

## Description

The Sans Notes App is a simple desktop applcication to make creating an index with notes and descriptions for SANS exams easier.  This application allows the user to:
- search through all of their notes and display the results
- insert and delete data based on specific user criteria
- create tables to store data in a sqlite database
- save data to an xlsx file

## Project Information

This python application utilizes a sqlite database on the backend to store records for easy access and utilization in other programs.

## Installation

1) [Install Python 3.6 or higher](https://www.python.org/downloads/)
2) [Install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and git clone https://github.com/Developernation/PythonProjects.git OR download the zip 
3) ```cd sans_tools``` and run ```pip install -r requirements.txt``` or ```pip3 install -r requirements.txt``` if you have more than one version of pip running on your system
* Note: if the ```pip``` command is not recognized you may need to [install pip](https://pip.pypa.io/en/stable/installation/)
* Note: if the ```python``` or ```python3``` command isn't recognized you may need to add Python to ```$PATH```

## Running the program
1) in the terminal ensure you are in the ```sans_tools``` folder and run ```python NotesAppFe.py``` or ```python3 NotesAppFe.py``` and you should seen the app on your screen!

## Usage
The app uses data tables to save and access your index and automatically sorts the entries alphabetically by topic as you add them.

The application has 3 tabs ```Add Data```, ```Search Data```, and ```Create Table```. 

By default the app creates the ```default_sans_table``` but you are able to create other tables specific to your class if you like in the ```Create Tables``` tab.

### Adding Data
In the ```Add Data``` tab, you can enter the data you would like to record and save it to the data table using the ```Add Data``` button.

### Searching, Deleting, and Saving Data to Excel
To view the data you just added you can select the ```Search Data``` tab, select the table you added data to using the drop down menu, and then click the ```Show All Data``` button or enter a search for your data and click ```Show Search Data```.

To save data to an excel file you much first search for the data you'd like to display by:
1) clicking the ```Search Data``` tab
2) selecting a table from the drop down menu
3) entering your search criteria (no fields are required and the search is a "fuzzy search" so partial words / numbers are okay). Alternatively, you can click ```Show All Data``` if you want everything from the table.
4) click ```Save Display To Excel```.  This will save the data displayed on the app to and excel file in your ```Downloads``` folder. 

To delete the displayed data you must first search for data to populate the display and then you can click the ```Delete Displayed Data``` button and the data will be removed from the table. 

### Creating and Deleting Tables

In the ```Create Table``` tab you can create or delete a table.

--------------------------------------------------------------------------------------------------------------------
That's it! Enjoy and let me know if you find bugs :)

Say hello on [LinkedIn](https://www.linkedin.com/in/sim-a-2aa9878a/) !

