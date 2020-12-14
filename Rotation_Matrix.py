# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 09:25:20 2019

@author: Mariette Bergere
MIS2 project
"""

#    all defined id Misplacement

import numpy as np


def rotation_mat(SEGMENT_origin, SEGMENT_proximal, SEGMENT_lateral, SEGMENT_anterior, m):
    
    x=SEGMENT_anterior[m,:]-SEGMENT_origin[m,:]
    X=x/np.linalg.norm(x)

    y=SEGMENT_lateral[m,:]-SEGMENT_origin[m,:]
    Y=y/np.linalg.norm(y)
    
    z=SEGMENT_proximal[m,:]-SEGMENT_origin[m,:]
    Z=z/np.linalg.norm(z)
    
    mat_rot=np.array(np.transpose(([X],[Y],[Z])))
    return mat_rot