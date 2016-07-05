# Written by Matt Cook
# Created June 27, 2016
# mattheworion.cook@gmail.com

"""
Module to downscale xylem conductance (transpiration) as a function of blue
stain fungal infection.
"""
import os

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define model function for Gaussian fit
def gauss(x, a, b, c):
    return a*np.exp(-0.5*((x-b)/c)**2)

# Define model function for Sigmoid fit
def sigmoid(x, a2, b2):
    return 1/(1+a2*np.exp(b2*x))
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#   full bark beetle-impact xylem scalar model function   #
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

def xylem_scalar(temp_gr, sf_decline):

    # fit blue stain growth model paras to 'temp_gr' data using a Guassian
    # function.  Covariance is unused.
    bs_gr_coef = np.asarray([450, 25, 5], dtype='float16')
    bs_gr_coef, bs_gr_covar = curve_fit(gauss,
                                        temp_gr['temp_obs'],
                                        temp_gr['gr_obs'],
                                        p0=bs_gr_coef)
    a = bs_gr_coef[0]
    b = bs_gr_coef[1]
    c = bs_gr_coef[2]

    # simulate cumulative daily blue stain fungal biomass
    # as function of temperature-dependent growth rate
    temp = sf_decline['at_obs']
    sim_bs_bm = np.empty_like(temp)
    for i in range(1, sim_bs_bm.shape[0]):
        sim_bs_bm[i] = sim_bs_bm[i-1] + a*np.exp(-0.5*((temp[i]-b)/c)**2)

    # fit model of simulated blue stain fungal growth to percent sapflux decline
    # using a sigmoid function (numerator is set to 1, in order to get 0-100%)
    xs_coef = np.asarray([0.04, 0.0006], dtype='float16')
    xs_coef, xs_covar = curve_fit(sigmoid,
                                  sim_bs_bm,
                                  sf_decline['xs_obs'],
                                  p0=xs_coef)
    a2 = xs_coef[0]
    b2 = xs_coef[1]

    # simulate the decline in sap flux as a function of simulated blue stain fungal biomass
    xs_sim = 1 / (1 + a2 * np.exp(b2 * sim_bs_bm))

    return xs_sim

# ------------------------------------------------------------------------

# CHANGE ME: Set your working directory to the directory in which this file is located.
os.chdir('\\Users\\Matthew\\Documents\\GitHub\\TREES_Py_R\\blue_stain_xylem_scaling_module')
# read in the temperature and growth rate of blue stain fungi from Moore and Six 2015
# temp = temperature (degrees C)
# gr = blue stain fungal growth rate (mm^2 d^-1)
temp_gr = np.loadtxt('blue_stain_temp_and_growth_rate.csv', delimiter=",",
                     skiprows=1,
                     dtype={'names':('temp_obs', 'gr_obs'),
                            'formats':('float32', 'float32')}
                    )

# read in observed mean daily percent sap flux decline with mean daily air temperatures
# *** as of 6/15/16, this data set is from Chimney Park 2009 ***
# date = mm/dd/yyyy
# at = mean daily air temperature (degrees C)
# 'xs' represents 'xylem scalar'
sf_decline = np.loadtxt('CP_daily_AT_and_perc_sap_flux_decline.csv',
                        delimiter=",",
                        skiprows=1,
                        dtype={'names':('dates', 'at_obs', 'xs_obs'),
                               'formats':('O', 'float64', 'float64')}
                       )

#::::::::::::::::::::::::::::::::::::::::::::::::#
#   create timeseries plot of obs and sim sfd    #
#::::::::::::::::::::::::::::::::::::::::::::::::#

CP_xs_sim = xylem_scalar(temp_gr, sf_decline)
CP_xs_obs = sf_decline['xs_obs']
CP_date = sf_decline['dates']


plt.plot(CP_xs_sim, 'r-')
plt.plot(CP_xs_obs, 'b.')
plt.show()

