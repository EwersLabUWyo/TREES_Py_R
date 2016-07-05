# -*- coding: utf-8 -*-
"""
Written by Matt Cook
Created July 5, 2016
mattheworion.cook@gmail.com
"""

import os
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

# David Millar - July 2, 2016
# dave.millar@uwyo.edu

# NOTES: - ggplot code at the end is just used for evaluation and plotting, and can be omitted 
#          or commented out when integrating this module into TREES_Py_R
#        - Non-linear least squares regression are currently used to determine empirical model
#          parameter estimates.  

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#                                                                                                                  #
# Module to simulate percent decline in stomatal conductance (water stress) due to declining soil water potential. #
#                                                                                                                  #
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

def sigmoid(x,a,b):
    return 100/(1+a*exp(b*x))

#-----------------------------------------------------------------------------------------------------
# CHANGE ME: Set your working directory to the directory in which this file is located.
os.chdir('\\Users\\Matthew\\Documents\\GitHub\\TREES_Py_R\\blue_stain_xylem_scaling_module')

# read in the water potential and percent loss conductance (PLC) data from
# laboratory xylem analysis (Heather Speckman)
# psi = water potential (MPa)
# plc = percent loss conductance within the plant xylem (%)
psi_obs, plc_obs= np.loadtxt('PICO_ws_obs_data.csv',delimiter=",",
                        skiprows=1,
                        dtype={'names':('psi_obs','plc_obs'),
                        'formats':('float32','float64')},
                        unpack=True)

#-----------------------------------------------------------------------------------------------------

#:::::::::::::::::::::::::::::::::#
#   water stress model function   #
#:::::::::::::::::::::::::::::::::#

def water_stress(psi_obs,plc_obs,psi_input):
  
  # fit water stress model paras to 'plc_data' data using a sigmoid function 
  # (numerator is set to 1, in order to get 0-100%).
  plc_gr_coef = np.asarray([11,-1],dtype='float16')
  plc_coef, plc-covar = curve_fit(sigmoid,
                                  psi_obs,
                                  plc_obs,
                                  p0=plc_coef)
  a = plc_coef[1]
  b = plc_coef[2]
  
  # simulate the percent decline in sap flux as a function of decreasing soil water potential
  ws_sim = 1-((100/(1+a*np.exp(b*psi_input)))/100)
  return(ws_sim)
  

#-----------------------------------------------------------------------------------------------------

#::::::::::::::::::::::::::::::::::::::::::::::::#
#   evaluate fit and plot of obs and sim sfd     #
#::::::::::::::::::::::::::::::::::::::::::::::::#
psi_input = psi_obs
ws_sim = water_stress(psi_obs,plc_obs,psi_input)
ws_obs = 1-(plc_obs/100)
psi_obs = psi_obs

#calculate R^2
summary = summary(lm(ws_sim~ws_obs))
R2 <- eval$r.squared
R2

# put data in ggplot format
ggdata <- cbind.data.frame(psi_obs,ws_sim,ws_obs)

#plot using ggplot
ws_test_plot <- ggplot(ggdata) + 
  geom_point(aes(x=psi_obs, y=ws_obs, shape ='observed', linetype = 'observed', color ='observed',size ='observed')) + 
  geom_line(aes(x=psi_obs, y=ws_sim, shape ='simulated', linetype = 'simulated', color ='simulated',size ='simulated')) +
  scale_shape_manual(values=c(19, NA)) + 
  scale_linetype_manual(values=c(0, 1)) +
  scale_size_manual(values=c(4,1.5)) +
  scale_color_manual(values=c("blue","springgreen3")) +
  xlab("water potential (MPa)") + 
  ylab("fraction of potential conductance") +
  ggtitle("water stress function evaluation") +
  theme(axis.text=element_text(size=18),
        strip.text=element_text(size=18),
        title=element_text(size=18),
        text=element_text(size=18),
        legend.text=element_text(size=18),
        legend.title=element_blank(),
        legend.key = element_blank())

ws_test_plot

#-----------#
# save plot #
#-----------#

#ggsave("PICO_water_stress_PLC_obs_and_sim.png",width=10,height=4,units='in',dpi=500)
#dev.off()


