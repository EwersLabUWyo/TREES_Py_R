###############################
# Written by Matt Cook        #
# mattheworion.cook@gmail.com #
# Created July 22, 2016       #
###############################

# Update September 29, 2016
# Added unpack operator, ws_sim recalculation using psi_soil and bug fixes.
# Renamed from Gsv0 to Main.R 

rm(list=ls())

#Set directory of scripts
script_dir <- file.path("C:/Users/Someone/Documents/Github/TREES_Py_R/R_Version/scripts")

# Move up one directory(will work if your dir is formatted like ours)
setwd(script_dir)
setwd("..")

# Set directory of data
data_dir <- file.path(getwd(), "data/")

# Set working directory to data
setwd(data_dir)

#Get water stress simulation
pathname <- file.path(script_dir, 'water_stress_module_v_0_5.R')
source(pathname)

#Get xylem scalar
pathname <- file.path(script_dir, 'blue_stain_xylem_scaling_module_v1.R')
source(pathname)

#Get Gs_ref
pathname <- file.path(script_dir, 'Gs_ref_module_v_0_6.R')
source(pathname)

#Get soil_water_potential
pathname <- file.path(script_dir, "soil_water_potential.R")
source(pathname)

######## START Unpack hack
####Taken From: http://stackoverflow.com/questions/1826519/function-returning-more-than-one-value#15140507

':=' <- function(lhs, rhs) {
  frame <- parent.frame()
  lhs <- as.list(substitute(lhs))
  if (length(lhs) > 1)
    lhs <- lhs[-1]
  if (length(lhs) == 1) {
    do.call(`=`, list(lhs[[1]], rhs), envir=frame)
    return(invisible(NULL)) 
  }
  if (is.function(rhs) || is(rhs, 'formula'))
    rhs <- list(rhs)
  if (length(lhs) > length(rhs))
    rhs <- c(rhs, rep(list(NULL), length(lhs) - length(rhs)))
  for (i in 1:length(lhs))
    do.call(`=`, list(lhs[[i]], rhs[[i]]), envir=frame)
  return(invisible(NULL)) 
}

######## End of Unpack ##########
#calculate soil water potential
swp <- psi_soil

#calculate water stress simulation
# Unpack the coefficients and store in array for later use
c(a, b, ws_sim_orig) := water_stress(psi_obs,plc_obs)

# Recalculate the water stress simulation with soil water potential data
ws_sim <- simFunc(a, b, swp)

#calculate xylem scalar
xs_sim <- xylem_scalar(temp_obs,gr_obs,at_obs,xs_obs)

#calculate gs ref coefficient
Gs_ref <- Gs_ref_func(D_obs,Gs_obs)

# calculate m scalar                            
m = Gs_ref * 0.6

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

#print(gsv_0)

