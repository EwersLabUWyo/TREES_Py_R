# Written by Matt Cook
# Created June 27, 2016
# mattheworion.cook@gmail.com

# Update 7/15/16
# added water stress and converted to object-oriented structure

# Update 7/21/16
# added gs ref and gsv0 calculations

from numpy import log

import blue_stain_xylem_scaling_module as bsmod
import water_stress_module as wsmod
import gs_ref_module as gsr
#import TREES_utils as utils


# bs calculates/stores a simulated xylem scalar model and its plot
xs = bsmod.XylemScalar('C:\\Users\\Matthew\\Documents'
                           +'\\Github\\TREES_Py_R\\Python3_Version\\'
                           +'blue_stain_xylem_scaling_module',
                           'blue_stain_temp_and_growth_rate.csv',
                           'CP_daily_at_and_perc_sap_flux_decline.csv')

                   
ws = wsmod.WaterStress('C:\\Users\\Matthew\\Documents'
                           +'\\Github\\TREES_Py_R\\Python3_Version\\'
                           +'water_stress_module',
                           'PICO_ws_obs_data.csv')
                      
gs_ref, r_sqr, d_obs = gsr.gsRef('C:\\Users\\Matthew\\Documents'
                            +'\\Github\\TREES_Py_R\\Python3_Version',
                            'PICO_atm_demand_data.csv')

# calculate m scalar                            
m = gs_ref * 0.6

# duplicate d_obs readings to match size of gs_ref
ws_sim_len = len(ws.sim)
d_obs_len = len(d_obs)
time_steps = int(ws_sim_len/d_obs_len)
i = 0
j = 1
d_extend = []
rem = ws_sim_len % d_obs_len
goal_len = (ws_sim_len - rem)

while len(d_extend) < goal_len:  
    while j <= time_steps:
        d_extend.append(d_obs[i])
        j += 1
    j = 1
    i += 1


while rem > 0:
    d_extend.append(d_obs[i-1])
    rem -= 1

# calculate gsv0 for each time step
gsv_0 = ws.sim * gs_ref - (m * log(d_extend)) 

print(gsv_0)
                          
#plot(ws.sim, ws.obs)