# Written by Matt Cook
# Created June 27, 2016
# mattheworion.cook@gmail.com

# NOTES: - ggplot code at the end is just used for evaluation and plotting, and can be omitted
#          or commented out when integrating this module into TREES_Py_R
#        - Non-linear least squares regression are currently used to determine empirical model
#          parameter estimates.

"""
Module to downscale xylem conductance (transpiration) as a function of blue
stain fungal infection.
"""
import os
import numpy as np
from scipy.optimize import curve_fit
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#from dateutil import parser

# Define model function for Gaussian fit
def gauss(x,a,b,c):
    return a*np.exp(-((x-b)/c)**2)

# Define model function for Sigmoid fit
def sigmoid(x,a2,b2):
    return 1/(1+a2*np.exp(b2*x))
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#   full bark beetle-impact xylem scalar model function   #
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

def xylem_scalar (temp_obs, gr_obs, at_obs, xs_obs):

    # fit blue stain growth model paras to 'temp_gr' data using a Guassian function
    bs_gr_coef = np.asarray([450,25,5],dtype='float16')
    bs_gr_coef, bs_gr_covar = curve_fit(gauss, 
                                        temp_obs,
                                        gr_obs,
                                        p0=bs_gr_coef)

    a = bs_gr_coef[0]
    b = bs_gr_coef[1]
    c = bs_gr_coef[2]
    
    #DEBUG
    print('a: ' + str(a))
    print('b: ' + str(b))
    print('c: ' + str(c))    
    
    # simulate cumulative daily blue stain fungal biomass
    # as function of temperature-dependent growth rate
    sim_bs_bm = np.empty_like(at_obs)
    sim_bs_bm = sim_bs_bm + gauss(at_obs,a,b,c)
    print(sim_bs_bm)
    # fit model of simulated blue stain fungal growth to percent sapflux decline
    # using a sigmoid function (numerator is set to 1, in order to get 0-100%)
    xs_coef = np.asarray([0.04, 0.0006],dtype='float16')   
    xs_coef, xs_covar = curve_fit(sigmoid,
                                  sim_bs_bm,
                                  xs_obs,
                                  p0=xs_coef)
    a2 = xs_coef[0]
    b2 = xs_coef[1]
    
    #DEBUG
    print('a2: ' + str(a2))
    print('b2: ' + str(b2))

    # simulate the decline in sap flux as a function of simulated blue stain fungal biomass
    xs_sim = 1 / (1 + a2 * np.exp(b2 * sim_bs_bm))

    return (xs_sim)

# -----------------------------------------------------------------------------------------------------

# CHANGE ME: Set your working directory to the directory in which this file is located.
os.chdir('\\Users\\Matthew\\Documents\\GitHub\\TREES_Py_R\\blue_stain_xylem_scaling_module')
# read in the temperature and growth rate of blue stain fungi from Moore and Six 2015
# temp = temperature (degrees C)
# gr = blue stain fungal growth rate (mm^2 d^-1)
temp_obs, gr_obs= np.loadtxt('blue_stain_temp_and_growth_rate.csv',delimiter=",",
                        skiprows=1,
                        dtype={'names':('temp_obs','gr_obs'),'formats':('float32','float32')},
                        unpack=True)

# read in observed mean daily percent sap flux decline with mean daily air temperatures
# *** as of 6/15/16, this data set is from Chimney Park 2009 ***
# date = mm/dd/yyyy
# at = mean daily air temperature (degrees C)
# 'xs' represents 'xylem scalar'
dates, at_obs, xs_obs = np.loadtxt('CP_daily_AT_and_perc_sap_flux_decline.csv',
                            delimiter=",",
                            skiprows=1,
                            dtype={'names':('dates','at_obs','xs_obs'),
                            'formats':('O','float64','float64')},
                            unpack=True)

#TO DO: Convert Date into format to be used with matplotlib so that we
# can plot our data with dates
# To prevent errors caused by date representation
# dates = dates.astype(str)
# To prevent errors caused by date representation
# replace /  with a space and convert to numbeer representation
# for i in range(0,dates.shape[0]):
#    dates[i] =  parser.datetime (dates[i])
# .replace('/',' '),'%m%d%Y'

#::::::::::::::::::::::::::::::::::::::::::::::::#
#   create timeseries plot of obs and sim sfd    #
#::::::::::::::::::::::::::::::::::::::::::::::::#

CP_xs_sim = xylem_scalar(temp_obs, gr_obs, at_obs, xs_obs)
CP_xs_obs = xs_obs
#CP_date = mdates.datestr2num()
#
#print(CP_xs_sim)
#print(CP_xs_obs)
#print(dates)

#
#plt.plot(CP_xs_sim,'r-')
#plt.plot(CP_xs_obs,'b.')
#plt.show()

