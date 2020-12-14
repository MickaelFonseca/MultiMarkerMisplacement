# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 08:47:29 2019

@author: Mariette Bergere
MIS2 project

Modified V1 Mickael Fonseca 06 Feb 2020

- Select manually files and copy to another folder (Results)
- Adapted name of the patient results folder
- defined argparse in order to call the function pyCGM2_CGM11_modelling
- automatised for batch processing
"""

import os
os.chdir('C:\\Users\\FONSECMI\\Projects\\MIS\\MIS2\\Code')
import glob
import Definition
import Simplify_acq
import File_Processing
import Misplacement_M
import Point_Manipulation
import pyCGM2_CGM11_modelling
import UserSettings
import time
import Write_Result_File
import numpy as np
import Analysis
import argparse

# define argparse to execute pyCGM modelling
parser = argparse.ArgumentParser(description='CGM1.1-pipeline')
parser.add_argument('-uf', '--userFile', type=str, help='userSettings', default="CGM1_1.userSettings")
parser.add_argument('-ef', '--expertFile', type=str, help='Local expert settings', default=None)
args = parser.parse_args()

    #1- PREPARATION OF FILES, VARIABLES, PATH
    
current_path=os.getcwd()
#result_path="D:\GITLAB\Marker_Misplacement_Lower_Limb_Simulation\Marker_Misplacement\Marker Misplacement Mariette\Results"
result_path="D:\\Data MarkerMisplacement Results\\06_00976_04402_20170523"
if not os.path.exists(result_path):
    os.mkdir(result_path)

    #Get markers to misplace and combinaison of errors
method=Definition.definition_method(current_path)
if method=='command_file':
    Combi=Definition.definition_combi(current_path)[0]
else: 
    #method=='command_file_Della_Croce'
    Combi=Definition.definition_combi_Della_Croce(current_path)[0]
MARK=Definition.definition_marker(current_path, method)[3]

    #Get static and dynamic files
Static_files=glob.glob(current_path+'\\'+'*'+'SB'+'*.c3d')
Dyn_files=glob.glob(current_path+'\\'+'*'+'GB'+'*.c3d')
    
Angle_names=['Pelvis tilt','Pelvis obliquity','Pelvis rotation',\
                   'Hip flexion/extention','Hip adduction/abduction','Hip rotation',\
                   'Knee flexion/extention','Knee valgus/varus','Knee rotation',\
                   'Ankle dorsi/plantar flexion','Ankle rotation','Foot progression']
PelvisAngles_x=[]
PelvisAngles_y=[]
PelvisAngles_z=[]
HipAngles_x=[]
HipAngles_y=[]
HipAngles_z=[]
KneeAngles_x=[]
KneeAngles_y=[]
KneeAngles_z=[]
AnkleAngles_x=[]
AnkleAngles_z=[]
Foot_Pro=[]
Angles=[PelvisAngles_x,PelvisAngles_y,PelvisAngles_z,\
                 HipAngles_x,HipAngles_y,HipAngles_z,\
                 KneeAngles_x,KneeAngles_y,KneeAngles_z,\
                 AnkleAngles_x,AnkleAngles_z,Foot_Pro]
                 
    #Creation of .txt file with simulation number and combinaison of marker positions associated
C=[]
suffix=1
first_suffix = suffix
Combi=Combi[suffix:390027]
for c in Combi:  
    C.append([suffix, '->', c ])
    suffix+=1
Write_Result_File.combinaisons(result_path, C)
T_combi=[]


            #1. GET SIMPLE C3D FILES AND REFERENCE
for p in range (1,len(Static_files)+1):
    patient_result_path=result_path+"\\Patient "+str(p)
    if not os.path.exists(patient_result_path):
        os.mkdir(patient_result_path)
    analysis_path=patient_result_path+"\\Analysis files"
    if not os.path.exists(analysis_path):
        os.mkdir(analysis_path)
    print (p)
    stat=Static_files[p-1]
    dyn=Dyn_files[p-1]        
    print (stat)
    print (dyn)
    
    s=stat.replace(current_path+'\\', '')
    s=s.replace('.C3D', '')
    d=dyn.replace(current_path+'\\', '')
    d=d.replace('.C3D', '')
    
        #1.1 Simplifie static and dynamic files 
    Point_To_Keep=['LTOE','LHEE','LMET','LMED','LMIF','LANK','LTIB',\
                   'RTOE','RHEE','RMET','RMED','RMIF','RANK','RTIB','RTTU','RKNE','RTHI',\
                   'LTTU','LKNE','LTHI','LASI','RASI','LPSI','RPSI']
    Simplify_acq.new_dyn(dyn,Point_To_Keep) 
#    Simplify_acq.new_stat(stat,Point_To_Keep,100) 
    Simplify_acq.clear_acq(dyn)
    Simplify_acq.clear_acq(stat)
    
        #1.2 pyCGM computation for original positions
    UserSettings.user_settings(dyn, current_path, s, d , 'pyCGM1')
    pyCGM2_CGM11_modelling.main(args)
    
        #1.3 Get initial pyCGM angles (reference) 
    acq_dyn=File_Processing.reader(dyn)
    
    LPelvisAngles=acq_dyn.GetPoint("LPelvisAngles_pyCGM1").GetValues() 
    LHipAngles=acq_dyn.GetPoint("LHipAngles_pyCGM1").GetValues() 
    LKneeAngles=acq_dyn.GetPoint("LKneeAngles_pyCGM1").GetValues() 
    LAnkleAngles=[]
    for frame in range(len(LKneeAngles[:,0])):
        LAnkleAngles.append([acq_dyn.GetPoint("LAnkleAngles_pyCGM1").GetValues()[frame,0],acq_dyn.GetPoint("LAnkleAngles_pyCGM1").GetValues()[frame,2]])
    LAnkleAngles=np.array(LAnkleAngles)
    LFootPro=[]
    for frame in range(len(LKneeAngles[:,0])):
        LFootPro.append([acq_dyn.GetPoint("LFootProgressAngles_pyCGM1").GetValues()[frame,2]])
    LFootPro=np.array(LFootPro)
    
    Angle_ori=[LPelvisAngles,LHipAngles,LKneeAngles,LAnkleAngles,LFootPro]
    Angle_Values_ori=[]
    for angle in Angle_ori:
        angle=angle.T
        for dir in angle:
            Angle_Values_ori.append(dir)
    for a in range(len(Angles)):
        Angles[a].append(Angle_Values_ori[a])
        
        #1.4 Store misplaced angles in csv files
    Write_Result_File.store_angles(Angle_names, Angle_Values_ori, "_pyCGM1", p, patient_result_path)
    Point_Manipulation.remove_angles(acq_dyn, "pyCGM1") 
    File_Processing.writer(acq_dyn,dyn)  
    
    
                #2- COMPUTATION OF SIMULATION
    
#    len_folder=15000
#    sInit=1
#    sEnd=len_folder-1+sInit
#    first_suffix=1
    for c in Combi:
        
            #2.1 Creation of new files, new file names
        new_stat=stat.replace('.C3D','_MIS')+'.C3D'
        new_dyn=dyn.replace('.C3D','_MIS')+'.C3D'
    
        new_s=new_stat.replace(current_path+'\\', '')
        new_s=new_s.replace('.C3D', '')
        new_d=new_dyn.replace(current_path+'\\', '')
        new_d=new_d.replace('.C3D', '')
        if first_suffix<=9:
            suffix=str(0)+str(first_suffix)
        else:
            suffix=str(first_suffix)
        tcombi0=time.time() 
        acq_stat=File_Processing.reader(stat)   
        acq_dyn=File_Processing.reader(dyn) 
        
            #2.1 Misplace markers
        for m in range(len(MARK)):  
            
            a=c[m][1][0]
            e=c[m][1][1]
            mark=c[m][0]
            Misplacement_M.move(acq_stat, mark, m, a, e, current_path, method)
            Misplacement_M.move(acq_dyn, mark, m, a, e, current_path, method)
            File_Processing.writer(acq_stat,new_stat)
            File_Processing.writer(acq_dyn,new_dyn)
                  
           #2.2 Remove virtual markers to compute them again from misplaced marker set
        acq_dyn=File_Processing.reader(new_dyn)        
        Point_Manipulation.remove_virtual_makers(acq_dyn)
        File_Processing.writer(acq_dyn,new_dyn)
        
        acq_stat=File_Processing.reader(new_stat)
        Point_Manipulation.remove_virtual_makers(acq_stat)       
        File_Processing.writer(acq_stat,new_stat) 
        
            #2.3 Kinematics computation
        UserSettings.set_user_settings(current_path+'\\CGM1_1.userSettings', new_s, new_d , str(suffix))
        pyCGM2_CGM11_modelling.main(args)
        
            #2.4 Get new angles 
        Angle_Values_mis=[]
        acq_dyn=File_Processing.reader(new_dyn)
         
        LPelvisAngles_mis=acq_dyn.GetPoint("LPelvisAngles_"+str(suffix)).GetValues() 
        LHipAngles_mis=acq_dyn.GetPoint("LHipAngles_"+str(suffix)).GetValues() 
        LKneeAngles_mis=acq_dyn.GetPoint("LKneeAngles_"+str(suffix)).GetValues() 
        LAnkleAngles_mis=acq_dyn.GetPoint("LAnkleAngles_"+str(suffix)).GetValues()[0]+acq_dyn.GetPoint("LAnkleAngles_"+str(suffix)).GetValues()[2]
        LFootPro_mis=acq_dyn.GetPoint("LFootProgressAngles_"+str(suffix)).GetValues()[3]
        
        LAnkleAngles_mis=[]
        for frame in range(len(LKneeAngles_mis[:,0])):
            LAnkleAngles_mis.append([acq_dyn.GetPoint("LAnkleAngles_"+str(suffix)).GetValues()[frame,0],acq_dyn.GetPoint("LAnkleAngles_"+str(suffix)).GetValues()[frame,2]])
        LAnkleAngles_mis=np.array(LAnkleAngles_mis)
        LFootPro_mis=[]
        for frame in range(len(LKneeAngles_mis[:,0])):
            LFootPro_mis.append([acq_dyn.GetPoint("LFootProgressAngles_"+str(suffix)).GetValues()[frame,2]])
        LFootPro_mis=np.array(LFootPro_mis)
        
        Angle_mis=[LPelvisAngles_mis,LHipAngles_mis,LKneeAngles_mis,LAnkleAngles_mis,LFootPro_mis] 
        for angle in Angle_mis:
            angle=angle.T
            for dir in angle:
                Angle_Values_mis.append(dir)
        for a in range(len(Angles)):
            Angles[a].append(Angle_Values_mis[a])
    
            #2.5 Store new angles in csv files (15000 files per folder)
    #    if first_suffix>sEnd:
    #        sInit=first_suffix
    #        sEnd+=len_folder
    #        separate_folder=patient_result_path+'\\results '+str(sInit)+' to '+str(sEnd)
    #        os.mkdir(separate_folder)
        Write_Result_File.store_angles(Angle_names, Angle_Values_mis, "simu"+str(suffix), p, patient_result_path)
        
        first_suffix+=1
        tcombi1=time.time()
        T_combi.append(tcombi1-tcombi0)
        
    Analysis.write_analysis_files(p, patient_result_path, patient_result_path+'\\Analysis files', Angle_names)
    
