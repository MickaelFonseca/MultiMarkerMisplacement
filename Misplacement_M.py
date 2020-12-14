# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:39:41 2019

@author: Mariette Bergere
MIS2 project
"""

#    acq: btk acquisition
#    mark: str
#    m: index of mark in MARK
#    angle, er: int. Error angle and magnitude
#    method: command_file or command_file_Della_Croce
    

import sys
sys.path.append(r'C:\Users\Mariette Bergere\Documents\Stage Geneve\pyCGM2')
import numpy as np
import Rotation_Matrix
import Definition

def move(acq, mark, m, angle, er, current_path, method):
    '''Misplace mark'''
        #marker definition 
    SEGMENT_origin=Definition.definition_marker(current_path, method)[0][m]
    Error_dir=Definition.definition_marker(current_path, method)[1][m]
    SEGMENT_name=Definition.definition_marker(current_path, method)[2][m]
    SEGMENT_proximal=SEGMENT_name+'_Z'
    SEGMENT_lateral=SEGMENT_name+'_Y'
    SEGMENT_anterior=SEGMENT_name+'_X'
    
        #GCS to LCS
    mark_MIS=np.zeros((acq.GetPointFrameNumber(),3))
    Mark=acq.GetPoint(mark)
    mark_GCS=acq.GetPoint(mark).GetValues() 
    ORIGIN_GCS=acq.GetPoint(SEGMENT_origin).GetValues()
    PROXIMAL_GCS=acq.GetPoint(SEGMENT_proximal).GetValues()
    LATERAL_GCS=acq.GetPoint(SEGMENT_lateral).GetValues()
    ANTERIOR_GCS=acq.GetPoint(SEGMENT_anterior).GetValues()
    Error=Definition.definition_error(angle, er, Error_dir)

    for n in range(0,acq.GetPointFrameNumber()): 
        
        #Rotation matrix from GCS to LCS (3x3) -> Transformation matrix (4x4)
        Ori=np.array(ORIGIN_GCS[n,:],dtype="float")
        Rot=Rotation_Matrix.rotation_mat(ORIGIN_GCS,PROXIMAL_GCS,LATERAL_GCS,ANTERIOR_GCS,n)[:,0]
        mat_left_fem=np.concatenate((Rot,Ori[:,None]),axis=1)
        T = np.concatenate((mat_left_fem,np.array([0,0,0,1])[None,:]),axis=0)
        Transf=np.linalg.inv(T)
        #Calculate marker coordinates in LCS
        mark_LCS = np.dot(Transf,np.append(mark_GCS[n,:],1))
        #Add an error on the marker in LCS
        mark_MIS_LCS=[mark_LCS[0]+Error[0],mark_LCS[1]+Error[1],mark_LCS[2]+Error[2],1]
        #Calculate marker coordinates in GCS
        mark_MIS_GCS=np.dot(np.linalg.inv(Transf),np.transpose(mark_MIS_LCS))
        #add new coordinates to point
        mark_MIS[n,:]=mark_MIS_GCS[:3]
        
    #set misplaced values
    Mark.SetValues(mark_MIS)









