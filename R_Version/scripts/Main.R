
rm(list=ls())

#Set directory of scripts
script_dir <- dirname(sys.frame(1)$ofile)

# Move up one directory(will work if your dir is formatted like ours)
setwd("..")

# Set directory of data
data_dir <- file.path(getwd(), "data")

# Set working directory to data
setwd(file.path(data_dir))

#Get water stress simulation
pathname <- file.path(script_dir, 'water_stress_module_v_0_5.R')
source(pathname)

#Get xylem scalar
pathname <- file.path(script_dir, 'blue_stain_xylem_scaling_module_v1.R')
source(pathname)

#Get Gs_ref
pathname <- file.path(script_dir, 'Gs_ref_module_v_0_6.R')
source(pathname)

#calculate water stress simulation
ws_sim <- water_stress(psi_obs,plc_obs)
ws_obs <- 1-(plc_obs/100)

#calculate R^2 for water stress
eval <- summary(lm(ws_sim~ws_obs))
R2 <- eval$r.squared
R2

#calculate xylem scalar
xs_sim <- xylem_scalar(temp_obs,gr_obs,at_obs,xs_obs)

#calculate gs ref coefficient
Gs_ref <- Gs_ref_func(D_obs,Gs_obs)

# calculate m scalar                            
m = Gs_ref * 0.6


#### From here down it doesn't work. Something is wrong with my logic in R####

# duplicate d_obs readings to match size of Gs_ref
ws_sim_len <- as.integer(length(ws_sim))
D_obs_len <- as.integer(length(D_obs))
time_steps <- as.integer((ws_sim_len/D_obs_len))
i <- 1
j <- 1
D_extend <- numeric()
rem <- ws_sim_len %% D_obs_len
goal_len <- (ws_sim_len - rem)
curr_len <- length(D_extend)

while (curr_len < goal_len)
  { 
    while (j <= time_steps)
  {
    D_extend <- append(D_extend, D_obs [i])
    j <- j + 1
  }
  j <- 1
  i <- i + 1
  curr_len <- length(D_extend)
}


while (rem > 0)
{
  D_extend <- append(D_extend, D_obs[i-1])
  rem <- rem - 1
}

# calculate gsv0 for each time step
gsv_0 <- ws_sim * Gs_ref - (m * log(D_extend)) 

print(gsv_0)

