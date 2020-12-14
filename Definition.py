# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:09:43 2019

@author: Mariette Bergere
MIS2 project
"""

#See exemple of command_file. 
#Respect yaml indentation.

#   method: str. command_file or command_file_Della_Croce
#   a, E: int. angle and error magnitude
#   Error_dir: str. AP_ML, AP_DP or ML_DP


import numpy as np
import yaml
import glob
import itertools


def definition_method(data_path):
    '''see 2 existing command files'''
    File=glob.glob(data_path+"\\command_file"+"*.txt")
    if File==[]: 
        raise Exception ("command_file not found")
    else:
        method=File[0].replace(data_path+"\\",'')
        method=method.replace(".txt",'')
    return method

  
def definition_marker(data_path,method): 
    '''Takes info of the 1st part of command_file (Markers)'''
    Ori=[]
    Dir=[]
    Seg_name=[]
    Mark=[]
    file_path=data_path + '\\' + method+'.txt'
    
    if not glob.glob(file_path): 
        raise Exception ("command_file not found")
    else:
        with open(file_path, 'r') as file:      
            command_file = yaml.load_all(file)
            for command in command_file:
                for k,v in command.items():
                    if k=='Markers':
                        for m in range(len(v)):
                            M=v.items()[m][1].items()
                            for i in M:
                                if i[0]=='name':
                                    Mark.append(i[1])
                                elif i[0]=='dir':
                                    Dir.append(i[1])
                                elif i[0]=='segment_name':
                                    Seg_name.append(i[1])
                                elif i[0]=='ori':
                                    Ori.append(i[1])
    return (Ori, Dir, Seg_name, Mark)



def definition_combi(data_path):
    '''Takes info of the 2nd part of command_file (Error) and creates all the 
    combinaisons of error possible '''
    MARK=definition_marker(data_path, 'command_file' )[3]
    Er=[]
    Angles=[]
    file_path=data_path + '\\' + 'command_file.txt'
    
    if not glob.glob(file_path): 
        raise Exception ("command_file not found")
        
    else:
        with open(file_path, 'r') as file:      
            command_file = yaml.load_all(file)
            for command in command_file:
                for k,v in command.items():
                    if k=='Error':
                        A=v.items()[0][1].items()
                        E=v.items()[1][1].items()
                        for ang in A:
                            Angles.append(ang[1])
                        for er in E:
                            Er.append(er[1])
    Error_Succession=[]
    Combi=[]
    Er_poss=[]
    Combi_er=[]
    for e in Er:
        if e==0: 
            Er_poss.append([0,e])
        else:
            for a in Angles:
                Er_poss.append([a,e])
    for c in itertools.product(Er_poss,repeat=len(MARK)):
        Combi_er.append(c)
        Error_Succession.append(c)
    for c in Combi_er:
        Mark_mis=[]
        for m in range(len(MARK)):
            Mark_mis.append([MARK[m], c[m]])
        Combi.append(Mark_mis)
        
    return (Combi, Er_poss, Error_Succession)

    

def definition_error(a, E, Error_dir):
    '''Creates the error vector in the LCS to add to the marker's original values at each frames.'''
    a_cos=abs(np.cos(np.deg2rad(a)))
    a_sin=abs(np.sin(np.deg2rad(a)))
    if Error_dir == 'AP_DP':
        Error = np.array([[E*a_cos, 0, E*a_sin]])
    elif Error_dir == 'AP_ML':
        Error = np.array([[E*a_cos, E*a_sin, 0]])
    elif Error_dir == 'ML_DP':
        Error = np.array([[0, E*a_cos, E*a_sin]])
    return(Error[0])
    
    
    
def definition_combi_Della_Croce(data_path):
    '''Takes info of the 2nd part of command_file (Error) and creates all the 
    combinaisons of error possible '''
    MARK=definition_marker(data_path, 'command_file_Della_Croce')[3]
    Magn=[]
    file_path=data_path + '\\' + 'command_file_Della_Croce.txt'
    
    if not glob.glob(file_path): 
        raise Exception ("command_file not found")
        
    else:
        with open(file_path, 'r') as file:      
            command_file = yaml.load_all(file)
            for command in command_file:
                for k,v in command.items():
                    if k=='Markers':
                        for m in range(len(v)):
                            M=v.items()[m][1].items()
                            for i,j in M:
                                if i=='misplacement_magnitude':
                                    magn_mark=[]
                                    for magn in range(len(j)):
                                        m=j.items()[magn][1]
                                        if m!='None':
                                            magn_mark.append(j.items()[magn][1])
                                    Magn.append(magn_mark)
        file.close()
    Er_poss=[]
    
    for er in Magn:
        Er_Mark=[[0,0],[0,er[0]],[180,-er[0]],[90,er[1]],[270,-er[1]]]
        Er_poss.append(Er_Mark)
    Combi=[]
    Combi_er=[]
    for c in itertools.product(Er_poss[0],Er_poss[1],Er_poss[2],Er_poss[3],Er_poss[4],Er_poss[5],Er_poss[6],Er_poss[7]):#[Er_poss[i] for i in range(len(Er_poss))]):#,Er_poss[1],Er_poss[2],Er_poss[3],Er_poss[4],Er_poss[5],Er_poss[6],Er_poss[7]):#len(MARK)
        Combi_er.append(c)
    for c in Combi_er:
        Mark_mis=[]
        for m in range(len(MARK)):
            Mark_mis.append([MARK[m], c[m]])
        Combi.append(Mark_mis)
    return (Combi,Er_poss)
    
    
    
    
    
    
    
    
    
    