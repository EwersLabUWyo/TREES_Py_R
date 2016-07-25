# Written by Matt Cook
# Created June 27, 2016
# mattheworion.cook@gmail.com

# Update July 15, 2016
# added water stress and converted to object-oriented structure

# Update July 21, 2016
# added gs ref and gsv0 calculations

# Update July 22, 2016
# added gsv0 calculation and memory use reduction


import blue_stain_xylem_scaling_module as bsmod
import water_stress_module as wsmod
import gs_ref_module as gsr
import gsv0


# initialize gsv_0 object for storage
gsv_0 = gsv0.Gsv_0()

# define working directory
work_dir = 'C:\\Users\\Matthew\\Documents\\Github\\TREES_Py_R\\Python3_Version\\'

# xs calculates/stores a simulated xylem scalar model and its plot against the
# observed data                   
xs = bsmod.XylemScalar(work_dir + 'blue_stain_xylem_scaling_module',
                           'blue_stain_temp_and_growth_rate.csv',
                           'CP_daily_at_and_perc_sap_flux_decline.csv')

# Unpack info from xs calculation
gsv_0.xs['obs'] = xs.obs
gsv_0.xs['sim'] = xs.sim

# delete xs to reduce memory usage
del(xs)

# ws calculates/stores a simulated xylem scalar model and its plot against the
# observed data                   
ws = wsmod.WaterStress(work_dir + 'water_stress_module', 'PICO_ws_obs_data.csv')

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


