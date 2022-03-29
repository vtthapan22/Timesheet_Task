from tkinter import *
from tkinter import Tk, mainloop, LEFT, TOP
from tkinter.ttk import *
import tkinter.scrolledtext as scrolledtext
import tkinter as tk
import glob
import os, subprocess
from datetime import datetime
import re
import sys
import xml.etree.ElementTree as ET
import os
import xml.etree.ElementTree as gfg 
import shutil
import XML

#This is to read the Myxml file which contain information about various temporary paths in windows

f = XML.Delete_Tempfiles()
root_drive = f.root_path()
user_name = f.user_info()
root = gfg.Element("Paths")
    
m1 = gfg.Element("RootDrive")
m1.text = root_drive
root.append (m1)
m2 = gfg.Element("WindowsTempLoc")
m2.text = root_drive+'windows\temp'
root.append (m2)
m3 = gfg.Element("AppDataTempLoc")
m3.text = user_name+'\AppData\Local\Temp'
root.append (m3)
xml_str = gfg.ElementTree(root)
  
save_path_file = "Settings.xml"
  
with open(save_path_file, "wb") as f:
    xml_str.write(f)
    #f.check_file_status('Settings.xml')
tree = ET.parse('Settings.xml')
    #This to read the root node information from Myxml file 
root = tree.getroot()
    # Reading each temporary path information below the root node
for elem in root:
    path_name = elem.text.lower()
print(path_name)
files = filter( os.path.isfile, glob.glob( path_name + '/**/*'))
    # find the largest file in the given path
largest_file = max( files, key =  lambda x: os.stat(x).st_size)
    #find Largest file size of the largest file
largest_file_size = os.stat( largest_file).st_size
    # count hte no.of files in the path
no_of_files=len([name for name in os.listdir(path_name) if os.path.isfile(os.path.join(path_name, name))])
    # logic to find total No.of bytes freed
total = 0
for entry in os.scandir(path_name):
    if entry.is_file():
        total += entry.stat().st_size
    Bytes_freed = total

def report():

    folder = 'C:/Users/'+os.getlogin()+'/AppData/Local/Temp'
    deleteFileCount = 0
    deleteFolderCount = 0

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        indexNo = file_path.find('\\')
        itemName = file_path[indexNo+1:]
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print( folder, '%s file deleted' % itemName )
                deleteFileCount = deleteFileCount + 1

            elif os.path.isdir(file_path):
                if file_path.__contains__('chocolate'):  continue
                shutil.rmtree(file_path)
                print( folder, '%s folder deleted' % itemName )
                deleteFolderCount = deleteFolderCount + 1

        except Exception as e:
            print( folder, 'Access Denied: %s' % itemName )

#function to create a application window 
def create_applicationwindow():
    # Create a GUI app
    app = tk.Tk()
    # Give a title to your app
    app.title("Cleanup utility - Non Admin Mode")
    # The window size is specified
    app.geometry("800x400")  
    #placing the application window in center of the screen
    app.eval('tk::PlaceWindow . center')
    # specified the window to resizable
    app.resizable(True, True)
    
    labelframe1 = LabelFrame(app, text="Summary Statistics")  
    labelframe1.pack(fill="both", expand="yes")  
    
    L1 = Button(labelframe1, text = 'Scan', command = report).grid(row = 1, column = 5)
    #Files detected field
    L1 = Label(labelframe1, text = ' Files Deleted', width = "25", anchor = "center").grid(row = 1, column = 1,padx = 7, pady = 60)
    #no.of files deleted
    #report()
    L1 = Label(labelframe1, text = no_of_files, width = "25", anchor = "center").grid(row = 1, column = 2)
    

    
    L2 = Label(labelframe1, text = ' Bytes Freed', width = "25", anchor = "center").grid(row = 2, column = 1)
    #No.of bytes freed
    L2 = Label(labelframe1, text = Bytes_freed, width = "25", anchor = "center").grid(row = 2, column = 2, padx = 5)
    
    L3 = Label(labelframe1, text = ' Large File Size', width = "25", anchor = "center").grid(row = 1, column = 3, padx = 7)
    #size of the largest file
    L3 = Label(labelframe1, text = largest_file_size, width = "25", anchor = "center").grid(row = 1, column = 4)
    
    L4 = Label(labelframe1, text = ' Large file Path', width = "25", anchor = "center").grid(row = 2, column = 3)
    #Path of the largest file
    L4 = Label(labelframe1, text = largest_file).grid(row = 2, column = 4)
    
    #report field
        
    labelframe2 = LabelFrame(app, text = "Report")
    labelframe2.pack(fill="both", expand = "yes")

    scrollbar = Scrollbar(app)
    scrollbar.pack(side=RIGHT, fill=Y)
    textbox = Text(app)
    textbox.pack()
    folder = 'C:/Users/'+os.getlogin()+'/AppData/Local/Temp'
    for the_file in os.listdir(folder):
        textbox.insert(END, folder, f"\{the_file}\n", the_file)
        print("\n")
    # attach textbox to scrollbar
    textbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=textbox.yview)
    #log of the files deleted
    #L1 = Label(labelframe2, text =report, width = "25", anchor = "center").grid(row = 1, column = 1, padx = 10, pady = 10)
    # Make the loop for displaying app
    app.mainloop()
create_applicationwindow()