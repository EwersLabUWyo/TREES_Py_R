# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 12:13:42 2016

@author: Matt
"""
import os.path as path
import tkinter
from tkinter import filedialog as fd
from tkinter import Label, Button, Entry, Frame
from tkinter.constants import BOTTOM, BOTH
from tkinter import StringVar, E, W

import matplotlib.pyplot as plt

import mbox
import blue_stain_xylem_scaling_module as xsmod
import water_stress_module as wsmod
import gsv0
import gs_ref_module as gsr

def makeMain(root, fields, calcs, **opts):
   """
   Populates main window.
   
   Inputs:
       root = main window
       fields = titles of rows to populate
   
   Outputs:
       Populated main window
   """
   entries = []
   row = 0
   dirOpt = opts['dirOpts']
   fileOpt = opts['fileOpts']
   # initialize array for stringVariables
   StrVar = []
   
   
   #create a Frame to hold the widgets
   frame = Frame(root)
   frame.pack(expand=True,
              fill=BOTH)
   frame.columnconfigure(1, weight=1)
   
   #create a Frame to hold the calculate buttons
   frame2 = Frame(root)
   frame2.pack(expand=True,
               fill=BOTH)
   frame2.columnconfigure(0, weight=1)
   
   for field in fields:
      # initialize textVariable for the entry
      StrVar.insert(row, StringVar(''))

      lab = Label(frame,
                  text=field)
      ent = Entry(frame,
                  textvariable=StrVar[row])
      lab.grid(row=row,
               column=0,
               sticky=W)
      ent.grid(row = row, 
               column = 1,
               sticky=W+E)
      if "Directory" in field:
          btn = Button(frame,
                       text = 'Select the directory',
                       command = lambda row=row : __dir2Ent(StrVar[row],
                                                                **dirOpt))
          fileOpt['initialdir'] = btn   
      else:
          btn = Button(frame,
                       text = 'Select the file',
                       command = lambda row=row : __filename_2_ent(StrVar[row],
                                                                 **fileOpt))
      btn.grid(row = row,
               column = 3,
               sticky = E)
      entries.append((field, ent, btn))
      row += 1
      if row == len(fields):
          for calc in calcs:
              runBtn = Button(frame2,
                              text = "Calculate " + calc,
                              command = lambda field=calc : calculate(StrVar,
                                                                      field))
              runBtn.pack(side = BOTTOM)


def calculate(StrVar, title):
    """
    Button function to calculate the Xylem Scalar or Water Stress.
    Input:
       StrVar = tuple of String Variables holding names of directory and files
       title = title of calculation to perform
    Output:
        Graph of the equation chosen
    """
    # TO DO: MAKE THIS SCALABLE
    # Set the appropriate working directory
    if title == 'Xylem Scalar':
        work_dir = StrVar[0].get()
    elif title == 'Water Stress':
        work_dir = StrVar[5].get()
    elif title == 

    # Get all the file and directory names        
    if __checkDir(work_dir):
        xs_obs = StrVar[0].get()
        sf_obs = StrVar[1].get()
        ws_obs = StrVar[2].get()
        atm = StrVar[3].get()
        xs_obs = str(xs_obs)
        sf_obs = str(sf_obs)
        ws_obs = str(ws_obs)
        atm = str(atm)        
        
    # Choose the calculation to do using name of button
    if title == 'Gsref' and __checkFile(atm):
        if __checkFile(ws_obs) and __checkFile(xs_obs) and __checkFile(sf_obs):
            # Calculate gsv0
            gsv_0 = gsv0.Gsv_0()
            xs = xsmod.XylemScalar(work_dir, xs_obs, sf_obs)
            # Unpack info from xs calculation
            gsv_0.xs['obs'] = xs.obs
            gsv_0.xs['sim'] = xs.sim
            
            # delete xs to reduce memory usage
            del(xs)

            ws = wsmod.WaterStress(work_dir, ws_obs)
            
            # Unpack info from ws calculation
            gsv_0.ws['obs'] = ws.obs
            gsv_0.ws['sim'] = ws.sim
            gsv_0.r_sqrs['ws'] = ws.r_sqr
            
            # delete ws to reduce memory usage
            del(ws)
            
            # calculate and store gs_ref and the results 
            gs = gsr.GsRef(work_dir, 'PICO_atm_demand_data.csv')  
            
            gsv_0.gs['obs'] = gs.gs_obs
            gsv_0.gs['sim'] = gs.gs_sim
            gsv_0.d_obs = gs.d_obs
            gsv_0.r_sqrs['gs'] = gs.r_sqr
            gsv_0.gs['ref'] = gs.gs_ref
            
            # delete gs to reduce memory usage
            del(gs)
            
            # Calculate gsv_0                     
            gsv_0.calculate()
            
            
    elif title == 'Water Stress' and __checkFile(ws_obs):
        ws = wsmod.WaterStress(work_dir, ws_obs)
        mod = ws
    elif title == 'Xylem Scalar' and __checkFile(xs_obs):
        xs = xsmod.XylemScalar(work_dir, xs_obs, sf_obs)
        mod = xs
                     
    # Ask user if they want to plot when not Gsref
    if not title == "Gsref":
        toPlot = mbox.mbox("Do you want to plot the models?",
                             ('Yes','yes'),
                             ('No','no'))
        if toPlot == 'yes' :
            plot(mod, title)
    # TO DO:  Add more functionality to this.
    # Maybe give a list with radio buttons for user to choose?

def plot(mod, title):
    """
    Plots the simulated and observed models using matplotlib.  Window
    will popup and user has option to save the plot.
    
    Inputs:
        mod = class to store graph with
        title = title of the graph
        
    Outputs:
        Pyplot graph which can be saved by the user.
    
    """
    mod.graph = plt.figure()
    plt.plot()
    plt.plot(mod.sim, 'r-', label = 'simulated')
    plt.plot(mod.obs, 'b.', label = 'observed')
    plt.title(title)
    plt.legend()     
    plt.show() 
     
    
def closeWindow(window): 
    window.destroy()


def makeMenuBar(window):
    """
    Create a menu bar with an Exit command
    """
    menubar = tkinter.Menu(window)
    filemenu = tkinter.Menu(menubar, tearoff = 0)
    filemenu.add_command(label = "Exit", command = window.destroy)
    menubar.add_cascade(label = "File", menu = filemenu)
    window.config(menu = menubar)

#
#def set_protocols(window):
#    """
#    Sets protocols for TREES root window and binds them.
#    """
#    # make the top right close button close the main window
#    # make Esc exit the program
#    window.bind('<Escape>', lambda e: window.destroy())
#    window.protocol("WM_DELETE_WINDOW", closeWindow(window))


def __checkDir(working_dir):
    """
    Check if a working directory has been chosen
    
    Input:
        working_dir = a string containing name of the directory
        
    Output:
        True if directory has been chosen
        False if directory not chosen
    """
    if working_dir == '':
        # show popup to alert user of mistake
        mbox.mbox(msg = "Please choose a directory in which to work", b2=None)
        return False
    else:
        return True


def __checkFile(filename):
    """
    Check a file has been chosen and is a .csv or .txt file
    
    Input:
        working_dir = a string containing name of the file
        
    Output:
        True if filename ends in .csv or .txt
        False otherwise
    """
    try:    
       filename = filename.lower()
       if filename.endswith('.csv') or filename.endswith('.txt'):
           return True
       else:
           message = "Your file : " 
           message += filename + " is not in the correct format."
           message += "\nAccepted filetypes are .csv and .txt"
           # Show popup with message to alert user
           mbox.mbox(msg = message, b2=None)
           return False
           
    except Exception as e:
        print("The following error has occured: ")   
        print(e)


def __dir2Ent(var, **dirOpt):
    """
    Sets the entry's textvariable to selected working dir
    """
    var.set(__select_workdir(**dirOpt))

    
def __filename_2_ent(var, **fileOpt):
    """
    Sets the entry's textvariable to selected working dir
    """
    filename = __select_filename(**fileOpt)
    filename = path.basename(filename)
    var.set(filename)

    
def __select_workdir(**dirOpt):
    """
    Opens directory browser and warns user if no directory is chosen.
    Used to set working directory
    
    Input:
        dirOpt = a list of directory options
    Output:
        work_dir = working directory
    
    """
    working_dir = fd.askdirectory(**dirOpt)
    # check if directory was chosen
    if not __checkDir(working_dir):
        working_dir = fd.askdirectory(**dirOpt)
    return working_dir

def __select_filename(**fileOpt):
    """
    Opens file browser and checks chosen file is .csv. If not .csv, show
    warning popup
    
    Input:
        fileOpt = a list of directory options and acceptable filetypes
        
    Output:
        filename = filename in string format
    """
    filename = fd.askopenfilename(**fileOpt)
    # check file type is correct
    if not __checkFile(filename) :                                            
        filename = fd.askopenfilename(**fileOpt)
    return filename

