"""
Written by Matthew Cook
Created August 2, 2016
mattheworion.cook@gmail.com
"""

# Update September 22, 2016
# Removed hardcoded theta values, replaced with test data from
# TEST_DATA_090216-Edit.csv
# Also, refactored to be Object-Oriented.

# Update September 27, 2016
# Moved simulation calculation into simFunc for outside use with soil water
# potential data.

# TODO: Decide whether or not we need to recalculate R^2 everytime we change
# the simulation data?

# TODO: Refactor for input of user-inputted variables (hard-coded right now)
# TODO: Maybe refactor calculations out of init into different methods/functions

from math import exp
from os import chdir
from pandas import read_csv


class SoilWaterPotential(object):
    
    def __init__(self, work_dir, swp_csv):
        # Define user-inputted variables (hard-code for now)
        por = 0.5 #porosity
        pClay = 0.25 #percent clay
        pSand = 0.25 #percent sand
        
        #Calculate their squares
        por2 = por*por
        pClay2 = pClay*pClay
        pSand2 = pSand*pSand
        
        # Calculate ks
        ks = 19.52348*por 
        ks -= 8.96847 - 0.028212*pClay 
        ks += 0.00018107*pSand2 
        ks -= 0.0094125*pClay2 
        ks -= 8.395215*por2 
        ks += 0.077718*pSand*por 
        ks -= 0.00298*pSand2*por2 
        ks -= 0.019492*pClay2*por2 
        ks += 0.0000173*pSand2*pClay 
        ks += 0.02733*pClay2*por 
        ks += 0.001434*pSand2*por 
        ks -= 0.0000035*pClay2*pSand
        
        # calculate e^ks
        ks = exp(ks)
        
        # Calculate bubbling pressure
        bubbling_pressure = 5.33967 + 0.1845 * pClay 
        bubbling_pressure -= 2.483945*por 
        bubbling_pressure -= 0.00213853*pClay2 
        bubbling_pressure -= 0.04356*pSand*por 
        bubbling_pressure -= 0.61745*pClay*por 
        bubbling_pressure += 0.00143598*pSand2*por2 
        bubbling_pressure -= 0.00855375*pClay2*por2 
        bubbling_pressure -= 0.00001282*pSand2*pClay 
        bubbling_pressure += 0.00895359*pClay2*por 
        bubbling_pressure -= 0.00072472*pSand2*por 
        bubbling_pressure += 0.0000054*pClay2*pSand 
        bubbling_pressure += 0.50028*por2*pClay
        
        # Calculate e^bubbling_pressure
        bubbling_pressure = exp(bubbling_pressure)
        
        # Calculate pore_size_index
        pore_size_index = -0.7842831 + 0.0177544*pSand 
        pore_size_index -= 1.062498*por 
        pore_size_index -= 0.00005304*pSand2 
        pore_size_index -= 0.00273493*pClay2 
        pore_size_index += 1.111349*por2 
        pore_size_index -= 0.03088295*pSand*por 
        pore_size_index += 0.00026587*pSand2*por2 
        pore_size_index -= 0.00610522*pClay2*por2 
        pore_size_index -= 0.00000235*pSand2*pClay 
        pore_size_index += 0.00798746*pClay2*por 
        pore_size_index -= 0.00674491*por2*pClay
        
        # calculate e^pore_size_index
        pore_size_index = exp(pore_size_index)
        
        # Calculate the residual
        residual = -0.0182482 + 0.00087269*pSand 
        residual += 0.00513488*pClay 
        residual += 0.02939286*por 
        residual -= 0.00015395*pClay2 
        residual -= 0.0010827*pSand*por 
        residual -= 0.00018233*pClay2*por2 
        residual += 0.00030703*pClay2*por 
        residual -= 0.0023584*por2*pClay
        
        # Notes:
        #
        # So below, ‘theta’ will need its own module(s) to be calculated,
        # but we can get to that later on.
        
        # set the current working directory - make sure to change this as needed
        chdir(work_dir)
        
        # Theta was calculated elsewhere, this is from a set of test data
        # It's still temporary
        
        theta = read_csv(swp_csv)
        theta = theta["0-15_cm_VWC"]
        
        S = [((t - residual) / (por - residual)) for t in theta]
        
        n = pore_size_index + 1
        
        m = pore_size_index / n
        
        # Create generators to calculate S^n and S^m at each index         
        Sn = self.__Sn(S, n)
        Sm = self.__Sm(S, m)
        
        #using the generators above, calculate each index of ku
        self.ku = [(ks * sn * sm) for sn, sm in zip(Sn, Sm)]
        
        self.psi_soil = self.__soil_water_potential(por,
                                                     bubbling_pressure, 
                                                     pore_size_index,
                                                     residual,
                                                     theta)
        #FOR DEBUGGING
        #print(psi_soil)
        
        
    def __Sn(self, S, n):
        """Calculate S^n for each item in S"""
        for s in S:
            yield s ** n


    def __Sm(self, S, m):
        """Calculate [1-(1 - S^(1/m))^m]^2"""
        for s in S:
            tmp = s ** (1/m)
            tmp = 1 - tmp
            tmp = tmp ** m
            tmp = 1 - tmp
            tmp = tmp ** 2.0
            yield tmp
    
    
    def __soil_water_potential(self,
                               porosity,
                               bubbling_pressure,
                               pore_size_index,
                               residual,
                               theta=2):
        """
        Calculate soil water potential, MPa. Assumes bubbling pressure in cm
        """
        
        #initialize variables
    #    psi_soil, n, m, S = None
        
        S = (theta - residual) / (porosity - residual)
        
        for s in S:
            if s < 0.001:
                S[s] = 0.001
            
            elif s > 1.0:
                S[s] = 1.0
    
        n = pore_size_index + 1
        m = pore_size_index / n
    
        #Use van Ganuchten model of soil water potential
        psi_soil = -0.0001019977334*bubbling_pressure 
    
        sPow = S ** (-1/m) - 1    
        psi_soil *= sPow ** (1/n)
        
        # If psi_soil is 0.0, it is actually -0.0
        # so we need to take the absolute value to get a correct value of 0.0
        for p in psi_soil:
            if p == -0.0:
                psi_soil[p] = 0.0
        
            if p < -10:
                psi_soil[p] = -10
        
        return(psi_soil)
