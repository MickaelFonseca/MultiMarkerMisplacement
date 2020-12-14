# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 10:11:48 2019

@author: Mariette Bergere
MIS2 project
"""


def remove_unused_makers(acq):
    for p in range(acq.GetPointNumber()):
        try:
            label=acq.GetPoint(p).GetLabel()
            if 'uname' in label:
                acq.RemovePoint(label)
        except:
            print('error in point '+str(p))


def remove_meta_data(acq):
    MD=['ANALOG','FORCE_PLATFORM']
    meta_data=acq.GetMetaData()
    for md in MD:
        child=meta_data.FindChild(md)
        meta_data.RemoveChild(child)
    p=meta_data.GetChild('POINT')
    p.RemoveChild(p.FindChild('POWERS'))
    p.RemoveChild(p.FindChild('POWERS_UNITS'))
    p.RemoveChild(p.FindChild('FORCES'))
    p.RemoveChild(p.FindChild('FORCES_UNITS'))
    p.RemoveChild(p.FindChild('MOMENTS'))
    p.RemoveChild(p.FindChild('MOMENTS_UNITS'))
    
    
def remove_virtual_makers(acq):
    VM=['midASIS','LHJC', 'RHJC', 'LKJC', 'RKJC','midHJC','LAJC','PELVIS_X','PELVIS_Y','PELVIS_Z', \
        'LFEMUR_X','LFEMUR_Y','LFEMUR_Z','RFEMUR_X','RFEMUR_Y','RFEMUR_Z',\
        'LTIBIA_X','LTIBIA_Y','LTIBIA_Z','RTIBIA_X','RTIBIA_Y','RTIBIA_Z',\
        'RTIBIA_X','RTIBIA_Y','RTIBIA_Z','LTIBIAPROX_X','LTIBIAPROX_Y','LTIBIAPROX_Z',\
        'RTIBIAPROX_X','RTIBIAPROX_Y','RTIBIAPROX_Z','LFOOT_X','LFOOT_Y','LFOOT_Z','RFOOT_X','RFOOT_Y','RFOOT_Z']
    for vm in VM:
        acq.RemovePoint(vm)    


def remove_angles(acq, suffix):
    Angles=['LHipAngles','RHipAngles','LKneeAngles', 'RKneeAngles', 'LAnkleAngles', 'RAnkleAngles',\
            'LFootProgressAngles','RFootProgressAngles','LPelvisAngles','RPelvisAngles']
    for angle in Angles:
        acq.RemovePoint(angle+"_"+str(suffix))


    
    
    
    
    
    
    
    
    
    
    
    
    
    
        

