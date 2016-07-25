# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 16:09:08 2016

@author: Matt
"""
# TO DO:  Buttons and white boxes for selection of files and directory
import tkinter
#from tkinter import filedialog as fd
#from tkinter import constants, Label, Button, Entry

import TREES_utils as utils



class MainMenu(object):

    def __init__(self):
        
        root = self.root = tkinter.Tk()
        root.title('Welcome to the TREES Graphical User Interface')
        
        # width x height + x_offset + y_offset:
        root.minsize(width=800, height=100) 
                
        # defining options for opening a directory
        self.dirOpt = dirOpt = {}
        dirOpt['mustexist'] = False
        dirOpt['parent'] = root
        dirOpt['title'] = 'Please choose your working directory' 
        
        # define options for opening or saving a csv file
        self.fileOpt = fileOpt= {}
        fileOpt['defaultextension'] = '.csv'
        fileOpt['filetypes'] = [('csv files', '*.csv'),
                                ('text files', '*.txt')]
        fileOpt['initialdir'] = '\\'
        fileOpt['parent'] = root
        fileOpt['title'] = 'Please select your file'
        
        # Store opts as one dicitionary to pass into make
        self.opts = opts = {}
        opts['dirOpts'] = dirOpt
        opts['fileOpts'] = fileOpt
        
        # defining titles for frames
        self.frame_titles = titles = []
        
        titles.insert(0, 'Blue Stain Xylem:                   ')
        titles.insert(1, 'Daily Sap Flux Decline:             ')
        titles.insert(2, 'Water Stress:                       ')
        titles.insert(3, 'Gsv0:                               ')
        titles.insert(4, 'Working Directory for Xylem Scalar: ')
        titles.insert(5, 'Working Directory for Water Stress: ')
        titles.insert(6, 'Working Directory for Gsv0:         ')
        
        # Hard code this for now, come back and changelater
        calcs = ['Xylem Scalar', 'Water Stress', 'Gsv0']
        
        # populate window with widgets
        utils.makeMain(root, titles, calcs, **opts)




mainGUI = MainMenu()
root = mainGUI.root
# set protocols for root window
#utils.set_protocols(mainGUI.root)
root.bind('<Escape>', lambda e: root.destroy())
#bind("<Configure>", utils.frame_resize)

root.mainloop()