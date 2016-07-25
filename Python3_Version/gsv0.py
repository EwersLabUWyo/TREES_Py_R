import sys
import traceback

from numpy import log

class Gsv_0(object):
    """
    Stores variables to calculate Gsv_0.  Once all variables have been
    calculated. It will return the vector containing Gsv_0 for each time step.
    """
    
    def __init__(self):
        self.xs = {}        # will store xs_sim, xs_obs
        self.ws = {}        # will store ws_sim, ws_obs
        self.r_sqrs = {}    # will store r_sqrs for calculations
        self.gs = {}        # will store gs_ref, gs_sim
        self.d_obs = []     # will store d_obs
        
      
        
    def calculate(self):
        try:
            # calculate m scalar                            
            m = self.gs['ref'] * 0.6
            
            # initialize local variables
            ws_sim = self.ws['sim']
            d_obs = self.d_obs
            xs_sim = self.xs['sim']
            gs_ref = self.gs['ref']  
            
            # initialize the length variables and calculate time step difference
            ws_sim_len = len(ws_sim)
            d_obs_len = len(d_obs)
            time_steps = int(ws_sim_len/d_obs_len)
            rem = ws_sim_len % d_obs_len
            goal_len = (ws_sim_len - rem)
            
            # initialize control variables
            i = 0
            j = 1
            
            # initialize new vector for storage of time step adjustment
            d_extend = []
            d_ext_len = len(d_extend)
            # duplicate d_obs readings to match size of gs_ref
            while d_ext_len < goal_len:  
                while j <= time_steps:
                    d_extend.append(d_obs[i])
                    j += 1
                j = 1
                i += 1
                d_ext_len = len(d_extend)
            
            # if the time steps don't divide evenly, tack on values at the end to correct
            while rem > 0:
                d_extend.append(d_obs[i-1])
                rem -= 1
            
            
            # calculate gsv_0
            self.gsv_0 = ws_sim * gs_ref - (m * log(d_extend))
            
            #Debug
#            print("Xylem Scalar:          ", len(xs_sim))
#            print("Water Stress:          ", ws_sim_len)
#            print("D observed (extended): ", len(d_extend))
#            print("gsv_0 :                ", len(self.gsv_0))
            # TO DO:  Make this work for xylem scalar as well.
#            if not self.xs:
#                self.gsv_0 = ws_sim * gs_ref - (m * log(d_extend))         
#            
#            else:
#                xs_sim = self.xs['sim']
#                print(xs_sim)
#                # calculate gsv0 for each time step with xylem scalar
#                self.gsv_0 = xs_sim * ws_sim * gs_ref - (m * log(d_extend))  
            
            print(self.gsv_0)
        
        except ValueError as v:
            print("""
                    Check that these following sizes match.  If they don't
                    match, your time steps may be the problem.
                    """)
            print("Xylem Scalar:          ", len(xs_sim))
            print("Water Stress:          ", ws_sim_len)
            print("D observed (extended): ", d_ext_len)
            print(v)
        
        except Exception as e:
            tb = sys.exc_info()[-1]
            pr_tb = traceback.extract_tb(tb, limit=1)[-1][1]
            print("Something went wrong on line: ", pr_tb , "in gsv0.py")
            print(e)
            
        
     

