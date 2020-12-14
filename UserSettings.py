# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 14:54:42 2019

@author: Mariette Bergere
MIS2 project
"""
#    file: path and c3d file name (static or dyn; to get metadata)
#    settings_path: path to write user setting (current path)
#    static_file: path and c3d static file name
#    dynamic_files: path and c3d dynamic file name
#    suffix: used as int, can be str


import yaml
import File_Processing

def user_settings(file,settings_path, static_file, dynamic_files, suffix):
    '''Creates CGM1_1.userSettings to run pyCGM'''
    acq=File_Processing.reader(file)
    
    Required_to_write=["Bodymass","Height","LeftLegLength","RightLegLength","LeftKneeWidth","RightKneeWidth","LeftAnkleWidth","RightAnkleWidth","LeftSoleDelta","RightSoleDelta","LeftShoulderOffset","LeftElbowWidth","LeftWristWidth","LeftHandThickness","RightShoulderOffset","RightElbowWidth","RightWristWidth","RightHandThickness"]
    Optional_to_write=["InterAsisDistance","LeftAsisTrocanterDistance","LeftTibialTorsion","LeftThighRotation","LeftShankRotation","RightAsisTrocanterDistance","RightTibialTorsion","RightThighRotation","RightShankRotation","LeftKneeFuncCalibrationOffset","RightKneeFuncCalibrationOffset"]
    
    dictionary={}
    
    with open(str(settings_path)+"\\"+"CGM1_1.userSettings","w") as f:
        
        MP={}
        Required={}
        Optional={}
        Global={}
        metadata=acq.GetMetaData()
        for r in Required_to_write:
            Required[str(r)]=0
        for o in Optional_to_write:
               Optional[str(o)]=0
        Required["Bodymass"]=metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()[0]
        Required["Height"]=metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()[1]
        Required["LeftLegLength"]=metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()[4]
        Required["RightLegLength"]=metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()[7]
        Required["LeftKneeWidth"]=metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()[3]
        Required["RightKneeWidth"]=metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()[6]
        Required["LeftAnkleWidth"]=metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()[2]
        Required["RightAnkleWidth"]=metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()[5]
        MP[str("Required")]=Required
        MP[str("Optional")]=Optional
        dictionary["MP"]=MP
        Global["Marker diameter"]=14
        Global["Point suffix"]= suffix
        dictionary["Global"]=Global
        Calibration={}
        Calibration["StaticTrial"]=static_file.replace(settings_path,'')+'.C3D'
        Calibration["Left flat foot"]=True
        Calibration["Right flat foot"]=True
        Calibration["Head flat"]=True 
        dictionary["Calibration"]=Calibration
        Fitting={}
        Trials=[]
        File={}
        File["File"]=dynamic_files+'.C3D'
        File["Mfpa"]="XX"
        Trials.append(File)
        Fitting["Trials"]=Trials
        dictionary["Fitting"]=Fitting
        f.write(yaml.dump(dictionary, indent=4))
    f.close()
    
    
def set_user_settings(user_setting_file, static_file, dynamic_files, suffix):
    '''Modify existing CGM1_1.userSettings to run pyCGM. 
    Careful : only sets calibration and trial filenames, and suffix name'''
    with open(user_setting_file) as f:
        list_doc=yaml.load(f)
    f.close()
    list_doc['Calibration']['StaticTrial']=static_file+'.C3D'
    list_doc['Global']['Point suffix']=suffix
    list_doc['Fitting']['Trials'][0]['File']=dynamic_files+'.C3D'
    with open(user_setting_file, "w") as f:
        f.write(yaml.dump(list_doc, indent=4))
    f.close()
        
        
        
        
        
        
        
        