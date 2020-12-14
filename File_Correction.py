# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 09:03:24 2020

@author: Mariette Bergere
MIS2 project
"""
import glob
import csv
import os


def rectify_file_index(result_path,n):
    '''offset of n (int) between true simulation number and file name'''
    
    result_files=glob.glob(result_path+'\\'+'*.csv')
    for file in result_files:
        if 'simu' in file:
            numb=file.replace(result_path+'\\p01_simu','')
            numb=numb.replace('.csv','')
            correct_numb=eval(numb)+n
            os.rename(file,result_path+'\\p01_simu'+str(correct_numb)+'.csv')


def get_missing_files(path,List):
    '''missed files in global result file (remove other files)
    List given by controle_result_files'''
    
    result_files=glob.glob(path+'\\'+'*.csv')
    for file in result_files:
        simu=file.replace('p01_simu','')
        simu=simu.replace('.csv','')
        if simu not in List:
            os.remove(path+file)
        
        
def controle_result_files(result_path,n1,n2):
    '''controle if there is files from n1 to n2 (ex 1 to 390625) (missing ?)'''
    
    result_files= os.listdir(result_path)
    Simu=[]    
    Missing_Simulations=[]
    for file in result_files:
        if 'simu' in file:
            simu=file.replace('p01_simu','')
            simu=simu.replace('.csv','')
            Simu.append(simu)
    print "Simu -> ok"
    for suff in range(n1,n2):
        if str(suff) not in Simu:
            Missing_Simulations.append(suff)
    return Missing_Simulations


def change_angle_names(result_path, wrong_result_path, Angle_Names_tochange,Right_Angle_Names, n1, n2):
    '''Correction of angle names in files of simu n1 to n2
    Angle names: lists of str
    wrong_result_path: path were to move wrong files'''
    
    for s in range(n1,n2):
        if s<10:
            simu='0'+str(s)
        else:
            simu=str(s)
        with open("D:\Stage Geneve\Initial Angle Names\\p01_wrongnames_"+simu+'.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            first_line=next(csv_reader)[0].split(';')[1:12]
            if first_line[0] in Angle_Names_tochange:
                csv_file.close()
                os.rename(wrong_result_path+"\\p01_simu"+simu+'.csv',\
                          result_path+"\\p01_wrongnames_"+simu+'.csv')
                right_file=open(result_path+"\\p01_simu"+simu+'.csv', "w")
                right_file.write(';Pelvis tilt;Pelvis obliquity;Pelvis rotation;'+\
                                 'Hip flexion/extention;Hip adduction/abduction;Hip rotation;'+\
                                 'Knee flexion/extention;Knee valgus/varus;Knee rotation;'+\
                                 'Ankle dorsi/plantar flexion;Ankle rotation;Foot progression') #right angle names
                right_file.write('\n')
                for line in csv_file:
                    right_file.write(line)
                csv_file.close() 
                right_file.close()