# CPD_SO_Automated_Printing

Custom Software for Running a Customers High Volume Print Orders

The Program as whole will unlikely be of any use to anyone, 
however their may be portions that can be used, adapted, or spark ideas to fit your needs.


### TODO
* Documentation
* Tiding Up Code
* Stability 
* More Testing
* More Environment Checks

### Known Bugs:
* If the Order has Invalid* or Unrealistic inputs, if a human does not catch it, the order will be wrong. (Some/Most Invalid inputs will be caught by the script)
* Can't Print Password Locked or Corrupt Files.
### Explicit Feature Removals:
* No Jobs with Front or Back Covers (Low Volume, Job files Inconsistent, need to be able to detect blank pages, and determine when and where to insert them.)
* No Coil Books, Color Jobs or Posters (Low Volume)

#### Email.py 
Fetches The Emails and calls other functions to setup and preprocess jobs.
#### Print.py 
This is the Printing Utility. It prints mostly autonomously for the inputted orders, main aspects it still asks for are which printer to use and if the "Special Instructions" field cannot be automatically determined, it has an operator verify and input information.
#### EmailPrint.py  (Tickets)
Prints the Emails with Page Counts and a Duplicate sheet on a different color.
#### order.py  
Contains the object the contains all the information regarding the current order that is being processed.
#### printer.py
It processes the final commands that are sent to the printer, and also checks the status of the printer to ensure it doesn't get overloaded.
#### files.py 
Grabs list of files and folders
#### PostScript.py 
Converts the PDFS to PS Files, also merges postscript files when needed.
#### jsonData.py
Converts the Email text into a JSON file.
#### GDrive.py  
Downloads the files for the order from Google Drive
#### BannerSheet.py  
Generates a custom banner sheet for running these jobs. Outputted in front of each job before all the files get outputted.  
#### instructions.py
Determines the Job Specs, and Reads the Special Instructions, and determines information based on that. Also Translates Human Instructions into Printer Instructions.
#### booklets.py
Contains the specific workflow for running Saddle-Stitched Booklets.
#### log.py
Allows the software to log its actions.
#### integrity.py
Checks the environment to make sure it is suitable to run the software.
#### googleform/emailsender.js
This allows Google Sheets to send formatted emails for incoming orders.
#### shortcuts/*.bat
For Colored Text to work in windows python must be executed from within command prompt.
#### buildexe.bat
Generates the executable files for Windows.

## PJL_Commands 
This folder contains the resources for the Printer Job Language (PJL) Commands needed to output the postscript files on the printer.  
In our environment these PJL commands are for a Xerox D-Series (D110) Printer with a 
* High Capacity Stacker
* 3 Hole Punch Unit
* Booklet Maker Finisher	

#### BannerSheetPS.py
This file is a PJL template file for how the banner sheets print. This gets inserted as is* on to the file generated by BannerSheet.py  
The color can be changed based on the setting in BannerSheet.py*  
#### PJL_PS.py
This file is a PJL template file for how the job files print. The file gets modified by on the job parameters and then inserting onto each postscript file.  


## Tests
This folder contains all the test code and test files for running tests.


Last Updated: 20200801
