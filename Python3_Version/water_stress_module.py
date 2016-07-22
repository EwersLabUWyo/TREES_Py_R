# -*- coding: utf-8 -*-
"""
Written by Matt Cook
Created July 5, 2016
mattheworion.cook@gmail.com
"""


# Module to simulate percent decline in stomatal conductance (water stress)
# due to declining soil water potential.

from os import chdir

from numpy import loadtxt, asarray, exp, column_stack, ones_like
from scipy.optimize import curve_fit
from statsmodels.api import OLS
import matplotlib.pyplot as plt


class WaterStress(object):
    """
    Module to create a simulated water stress model
    """
    def __init__(self, work_dir, csv_ws):
        """
        Stores information from Xylem Scalar module
        
        Attributes:
            xs_sim = List of simulated xylem scalars
            xs_obs = tuple of observed xylem scalars (faster and immutable)
            graph = plot of the simulated and observed xylem scalars
            coeff = coefficients for xylem scalar module
            r_sqr = r-squared value for the fittting of the model
        """
        # initialize variables
        self.sim = []
        self.obs = ()
        self.graph = None
        self.coeff = {}
        self.r_sqr = 0
        
        # Calculate variables
        self.water_stress_module(work_dir, csv_ws)
        
    def water_stress_module(self, work_dir, csv_ws):
        """
        Look in the readme to see how this works, for now.
        
        NOTE: When reading from csv, the script skips the first line (headers)
        so if you do not have headers and do not wish to lose the first row of 
        data points, add an extra row at the top of your CSV file.
        
        Inputs:
            work_dir = working directory for where you have your CSV files
                       stored
        
            csv_gr = the CSV file containing your temperature and observed 
                     blue stain xylem growth
        
            csv_sfd = the CSV containing columns for:
                       date as mm/dd/yyyy
                       mean daily air temperature in degrees C
                       xylem scalar
        
        Outputs:
            sim = the simulated xylem scalar model
            
            obs = the observed xylem scalar model
            
            r_sqr = r-squared of the simulated model
    """
    
        # Change the directory to your working directory
        chdir(work_dir)
        
        try:
            # read in the water potential and percent loss conductance (PLC) data from
            # laboratory xylem analysis (Heather Speckman)
            # psi = water potential (MPa)
            # plc = percent loss conductance within the plant xylem (%)
            psi_obs, plc_obs = loadtxt(csv_ws,
                                       delimiter=",",
                                       skiprows=1,
                                       dtype={'names':('psi_obs', 'plc_obs'),
                                              'formats':('float64', 'float64')},
                                       unpack=True)
        except Exception as e:
            print("Something went wrong.  Check that " + csv_ws + 
            " is in the correct format.")
            print("Here is the actual error: ", e)
            
        # Calculate water stress                       
        self.sim = sim = self.__water_stress(psi_obs, plc_obs)
        self.obs = obs = 1-(plc_obs/100)
        # Add column of zeros to simulate y-intercept?
        obs_stacked = column_stack((obs, ones_like(obs)))
        
        #calculate R^2
        summary = OLS(sim, obs_stacked).fit()
        self.r_sqr = summary.rsquared
    
    
    def plot(self):
        """
        Plots and saves the plot for later use
        """
        graph = self.graph
        graph.plot(self.sim, 'r-', label = 'simulated')
        graph.plot(self.obs, 'b.', label = 'observed')
        graph.title("Xylem Scalar")
        graph.legend()     
        graph.show()
        plt.savefig(graph)

    
    def __sigmoid(self, x, a, b):
        """
        Sigmoid function used in water stress curve fitting. 'x' is the vector,
        'a' and 'b' are the coefficient guesses for the model.
        """
        return 100/(1+a*exp(b*x))
    
    def __water_stress(self, x_obs, y_obs):
        """
        Takes observed water potential and percent loss conductance (PLC) data
        from laboratory xylem analysis (Heather Speckman) and returns the simulated
        water stress model.  Uses the sigmoid function for curve fitting.
    
        input:
        x_obs = observed water potential (MPa) (psi)
        y_obs = observed percent loss conductance within the plant xylem (%) (plc)
    
        output:
        sim = simulated water stress model
        """
    
        # fit water stress model paras to 'plc_data' data using a sigmoid function
        # (numerator is set to 1, in order to get 0-100%).
        plc_paras = asarray([11, -1], dtype='float64')
        plc_paras, plc_covar = curve_fit(self.__sigmoid,
                                         x_obs,
                                         y_obs,
                                         p0=plc_paras)
        self.coeff['a'] = a = plc_paras[0]
        self.coeff['b'] = b = plc_paras[1]
    
        # simulate the percent decline in sap flux as a function of decreasing
        # soil water potential
        sim = 1-((100/(1+a*exp(b*x_obs)))/100)
    
        return sim
       
