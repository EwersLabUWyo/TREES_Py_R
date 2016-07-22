# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 16:09:08 2016

@author: Matt
"""

import tkinter
from tkinter import filedialog as fd
from tkinter import constants

import TREES_utils as utils


class Main_Menu(object):

    def __init__(self):
        root = self.root = tkinter.Tk()
        root.title('Test')
        # make Esc exit the program
        root.bind('<Escape>', lambda e: root.destroy())
        
        
        #TO DO: Set up buttons to select directory and files
        # options for buttons
        button_opt = {'side': constants.RIGHT}
    
#         define buttons
        tkinter.Button(root,
                       text = 'Simulate Blue Stain Xylem Scaling',
                       command = None).pack(**button_opt)
#        tkinter.Button(self,
#                       text='askopenfilename',
#                       command=self.askopenfilename).pack(**button_opt)
#        tkinter.Button(self,
#                       text = 'asksaveasfile',
#                       command=self.asksaveasfile).pack(**button_opt)
#        tkinter.Button(self,
#                       text = 'asksaveasfilename',
#                       command = self.asksaveasfilename).pack(**button_opt)
#        tkinter.Button(self,
#                       text = 'askdirectory',
#                       command = self.askdirectory).pack(**button_opt)
#    
 
        # defining options for opening a directory
        self.dir_opt = options = {}
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'Please choose your working directory'      
        
        # define options for opening or saving a csv file
        self.file_opt = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('csv files', '.csv'), ('text files', '.txt')]
        options['initialdir'] = '\\'
        options['parent'] = root
        options['title'] = ''
        
        # create a menu bar with an Exit command
        menubar = tkinter.Menu(root)
        filemenu = tkinter.Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Exit", command = root.destroy)
        menubar.add_cascade(label = "File", menu = filemenu)
        root.config(menu = menubar)
             
        # select the working directory
        self.working_dir = fd.askdirectory(**self.dir_opt)
        
        # TO DO: Add functionality to Cancel button to go back to main page
        isTrue = utils.check_dir(self.working_dir)
        if not isTrue:
            self.working_dir = fd.askdirectory(**self.dir_opt)
            
        # set current directory to working directory
        self.file_opt['initialdir'] = self.working_dir
        
        # TO DO: add functionality for cancel button to skip while loop     
        # Check if a working directory has been set
        if not utils.check_dir(self.working_dir):
            self.working_dir = fd.askdirectory(parent = root,initialdir = "/",
                                            title = 'Please select a directory')
        
        # select the blue stain file
        self.bs_gr = fd.askopenfilename(**self.file_opt) 
        
        # TO DO: add functionality for cancel button to skip while loop                                
        # make sure file type is correct                   
        if not utils.check_file(self.bs_gr) :
            self.bs_gr = fd.askopenfilename(parent = root,
                                            initialdir = self.working_dir,
                                            title='Please select your blue stain fungal growth file',
                                            )
                                            
        # select sapflux decline file                                    
        self.bs_sfd = fd.askopenfilename(parent = root,
                                         initialdir = self.working_dir,
                                         title='Please select your sap flux decline file')
                                         
        # TO DO: add functionality for cancel button to skip while loop                                
        # make sure file type is correct                  
        if not utils.check_file(self.bs_sfd) :                                            
            self.bs_sfd = fd.askopenfilename(parent = root,
                                             initialdir = self.working_dir,
                                             title='Please select your sap flux decline file')
         # select sapflux decline file                                    
        self.ws_obs = fd.askopenfilename(parent = root,initialdir = self.working_dir,
                                            title='Please select your sap flux decline file')
        # TO DO: add functionality for cancel button to skip while loop                                
        # make sure file type is correct                  
#        while not utils.check_file(self.bs_sfd) or CANCEL:                                            
#            self.bs_sfd = fd.askopenfilename(parent = root,
#                                             initialdir = self.working_dir,
#                                             title='Please select your sap flux decline file')
    def close_window(root): 
        root.destroy()

    # make the top right close button close the main window
        root.protocol("WM_DELETE_WINDOW", root.close_window(root))

    

    

mainGUI = Main_Menu()
mainGUI.root.mainloop()