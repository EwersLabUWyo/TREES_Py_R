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


# clear everything out of memory
rm(list=ls())

# call to ggplot package
library(ggplot2)

#-----------------------------------------------------------------------------------------------------
# set the current working directory - make sure to change this as needed
setwd("C:\\Users\\Matthew\\Documents\\GitHub\\TREES_Py_R\\water_stress_module")


# read in the water potential and percent loss conductance (PLC) data from laboratory xylem analysis (Heather Speckman)
# psi = water potential (MPa)
# plc = percent loss conductance within the plant xylem (%)
plc_data <- read.csv("PICO_ws_obs_data.csv")
names(plc_data)=c("psi_obs", "plc_obs")

psi_obs <-plc_data$"psi_obs"
plc_obs <- plc_data$"plc_obs"


#-----------------------------------------------------------------------------------------------------

#:::::::::::::::::::::::::::::::::#
#   water stress model function   #
#:::::::::::::::::::::::::::::::::#

water_stress <- function(psi_obs,plc_obs,psi_input){
  
  # fit water stress model paras to 'plc_data' data using a sigmoid function 
  # (numerator is set to 1, in order to get 0-100%).
  
  plc.fit <- nls(plc_obs ~ 100/(1+a*exp(b*psi_obs)), start = list(a = 11, b = -1))
  plc.paras <- coef(plc.fit)
  a <- plc.paras[1]
  b <- plc.paras[2]
  
  # simulate the percent decline in sap flux as a function of decreasing soil water potential
  ws_sim <- 1-((100/(1+a*exp(b*psi_input)))/100)
  return(ws_sim)
  
}

#-----------------------------------------------------------------------------------------------------

#::::::::::::::::::::::::::::::::::::::::::::::::#
#   evaluate fit and plot of obs and sim sfd     #
#::::::::::::::::::::::::::::::::::::::::::::::::#
psi_input <- psi_obs
ws_sim <- water_stress(psi_obs,plc_obs,psi_input)
ws_obs <- 1-(plc_obs/100)
psi_obs <- psi_obs

#calculate R^2
eval = summary(lm(ws_sim~ws_obs))
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


