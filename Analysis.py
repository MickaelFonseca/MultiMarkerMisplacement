# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 15:55:45 2019

@author: Mariette Bergere

(to be re-difined)


"""

#3 parts : - compare 2 angles computed (verification of different computation methods)
#            - computation of RMS and correlation coefficient
#            - show results curves

#   p: int (patient n°)
#   MARK: list of misplaced markers (MARK=Definition.definition_marker(current_path, method)[3])
#   data_path, result_path, analysis_path: str
#   Combi: list of misplacement combinaisons  (Combi=Definition.definition_combi(current_path)[0] or definition_combi_Della_Croce )
#   Ref, Sim: lists of data (1 angle; each frame)
#   Angle_Names: list of angle names defined in MAIN_Misplacement



import math 
import glob
import csv
import numpy as np
from operator import itemgetter
import numpy as np   
import matplotlib.pyplot as plt 
import Definition

import btk

def compute_difference(file1, file2, angle_name1, angle_name2):
    '''Check difference between 2 angles on c3d file'''
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(file1) 
    reader.Update()
    acq1=reader.GetOutput() 
    
    
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(file2) 
    reader.Update()
    acq2=reader.GetOutput() 
    
    angle1=acq1.GetPoint(angle_name1).GetValues()
    angle2=acq2.GetPoint(angle_name2).GetValues()
    
    nf=min(acq1.GetPointFrameNumber(), acq2.GetPointFrameNumber())
    diffx=0
    diffy=0
    diffz=0
    for f in range(nf):
        dx=angle1[f,0]-angle2[f,0] 
        dy=angle1[f,1]-angle2[f,1]
        dz=angle1[f,2]-angle2[f,2]
        if np.abs(dx)>np.abs(diffx):
            diffx=dx
        if np.abs(dy)>np.abs(diffy):
            diffy=dy
        if np.abs(dz)>np.abs(diffz):
            diffz=dz
    return (diffx, diffy, diffz)


        # RMS, Correlation Coefficient
        
def rms(Ref, Sim):
    '''RMS computation'''
    n=min(len(Ref), len(Sim))
    diff=0
    for frame in range(n):
        diff+=(Sim[frame]-Ref[frame])**2
    rms=math.sqrt(diff/n)
    return rms


def mean_rms_misplacement(MARK, result_path, Combi, Angle_sequence):
    '''RMS mean on simulations involving each marker misplacement'''
    RMS_Values=np.zeros((8,4))
    Repetition_number=np.zeros((8,4))
    with open(result_path+"\\RMS.csv") as rms_file:
        csv_reader=csv.reader(rms_file, delimiter=';', quotechar='|')
        next(csv_reader)[0].split(';')[1:12]
        for simu in csv_reader:
            if simu[0]=='':
                break
            else:
                mean=simu[14]
                mean=eval(mean.replace(',','.'))
                combi=Combi[eval(simu[0])-1]
                for m in range(len(MARK)):
                    pos=combi[m][1]
                    if pos in Angle_sequence:
                        index_pos=Angle_sequence.index(pos)
                        RMS_Values[m][index_pos]+=mean
                        Repetition_number[m][index_pos]+=1
        rms_file.close()
    return np.array(RMS_Values),np.array(Repetition_number)

    
def write_mean_rms_misplacement(MARK, data_path, result_path, analysis_path, Combi):
    '''Write file corresponding to RMS repetitions'''
    Angle_sequence = Definition.definition_combi(data_path)[1]
    Angle_sequence.remove([0, 0])
    RMS_Values,Repetition_number=mean_rms_misplacement(MARK, result_path, Combi, Angle_sequence)
    f=open(analysis_path+"\\repetition RMS on markers.txt", 'w')
    f.write('        '+'Repetition of worst positions from RMS'+'\n'+'\n')
    f.write('Angle sequence : '+str(Angle_sequence) +'\n'+'\n')
    for m in range(len(MARK)):
        f.write(str(MARK[m])+str(RMS_Values[m]/Repetition_number[m]))
        f.write('\n')
    f.write('\n')
    for m in range(len(MARK)):
        f.write(str(MARK[m])+str(Repetition_number[m]))
        f.write('\n')
    f.close()
    
            
def get_data(file, angle_index):
    '''Get data from file. 
    angle_index : 0->11'''
    with open(file) as f_result:
        f=csv.reader(f_result, delimiter=' ', quotechar='|')
        Data=[] 
        r=0
        for row in f:
            if r>0:
                line=row[1].split(';')
                Data.append(eval(line[angle_index+1]))
            r+=1
    f_result.close()
    return Data
 
           
def get_one_third_data(file, angle_index):
    '''Get data from file'''
    with open(file) as f_result:
        f=csv.reader(f_result, delimiter=';', quotechar='|')
        Data=[] 
        r=0
        next(f)
        for row in f:
            if  r<107:
                line=row[angle_index+1]
                Data.append(eval(line))
                next(f)
                next(f)
            r+=3
    f_result.close()
    return Data


def write_analysis_files(p, result_path, analysis_path, Angle_Names):
    '''For 1 patient, writes RMS and Correlation Coefficient files from all result files'''
    result_files=glob.glob(result_path+'\\'+'*.csv')
    Misplaced_Files=[]
    MeanRMS=[0]*12
    MaxRMS=[0]*12
    MeanCorr=[0]*12
    MinCorr=[1]*12
    
    for file in result_files:  
        if 'pyCGM1' in file:
            pyCGM_file=file
        elif 'simu' in file:
            if p<10:
                name=result_path+'\\p0'+str(p)+'_simu'
            else:
                name=result_path+'\\p'+str(p)+'_simu'
                
            simu=file.replace(name,'')
            simu=simu.replace('.csv','')
            First=['01','02','03','04','05','06','07','08','09']
            if simu in First:
                simu=eval(simu[1])
            else:
                simu=eval(simu)
            Misplaced_Files.append([simu, file])   
    f_rms=open(analysis_path+'\\RMS.csv','w')
    f_corr=open(analysis_path+'\\Correlation.csv','w')
    Misplaced_Files=sorted(Misplaced_Files, key=itemgetter(0))
    try:
        f_rms.write("Simu;")
        f_corr.write("Simu;")
        for angle in Angle_Names:
            f_rms.write(angle+";")
            f_corr.write(angle+";")
        f_rms.write(';'+'Mean')
        f_rms.write(';'+'Max')
        f_rms.write("\n")
        f_corr.write(';'+'Mean')
        f_corr.write(';'+'Min')
        f_corr.write("\n")
        
        All_pyCGM=[]
        for angle_index in range(12):
            All_pyCGM.append(get_data(pyCGM_file, angle_index))
            
        for mis_file in Misplaced_Files:
            s=mis_file[0]
            if s<=9:
                simu=str(0)+str(s)
            else:
                simu=str(s)
                
            f_rms.write(str(mis_file[0])+";")
            f_corr.write(str(Misplaced_Files.index(mis_file)+1)+";")
            
            SimuRmsMean=0
            SimuRmsMax=0
            
            SimuCorrMean=0
            SimuCorrMin=1
            
            for angle_index in range(12):
                pyCGM=All_pyCGM[angle_index]
                misplace=get_data(mis_file[1], angle_index)
                error=rms(pyCGM, misplace)
                correlation=np.corrcoef(pyCGM, misplace)[0][1]
                str_error=str(error).replace('.',',')
                str_correlation=str(correlation).replace('.',',')
                f_rms.write(str_error+";")
                f_corr.write(str_correlation+";")
                
                SimuRmsMean+=error
                if error>SimuRmsMax:
                    SimuRmsMax=error
                
                MeanRMS[angle_index]+=error
                if error>MaxRMS[angle_index]:
                    MaxRMS[angle_index]=error
                    
                SimuCorrMean+=correlation
                if correlation<SimuCorrMin:
                    SimuCorrMin=correlation
                
                MeanCorr[angle_index]+=correlation
                if correlation<MinCorr[angle_index]:
                    MinCorr[angle_index]=correlation
            
            SimuRmsMean=SimuRmsMean/12
            SimuCorrMean=SimuCorrMean/12
            f_rms.write(';')
            f_rms.write(str(SimuRmsMean).replace('.',',')+';')
            f_rms.write(str(SimuRmsMax).replace('.',','))
            f_rms.write("\n")
            
            f_corr.write(';')
            f_corr.write(str(SimuCorrMean).replace('.',',')+';')
            f_corr.write(str(SimuCorrMin).replace('.',','))
            f_corr.write("\n")
            if s%1000==0:
                print s
            
        f_rms.write('\n Mean ;')
        for angle_index in range(12):
            MeanRMS[angle_index]=MeanRMS[angle_index]/s
            f_rms.write(str(MeanRMS[angle_index]).replace('.',',')+';')
        f_rms.write('\n Max ;')
        for angle_index in range(12):
            f_rms.write(str( MaxRMS[angle_index]).replace('.',',')+';')
        f_rms.close() 
        
        f_corr.write('\n Mean ;')
        for angle_index in range(12):
            MeanCorr[angle_index]=MeanCorr[angle_index]/s
            f_corr.write(str(MeanCorr[angle_index]).replace('.',',')+';')
        f_corr.write('\n Min ;')
        for angle_index in range(12):
            f_corr.write(str(MinCorr[angle_index]).replace('.',',')+';')
        f_corr.close()
    except:
        f_rms.close()
        f_corr.close()
        return "code stoped"


           
        # Show curves
    
def get_min_max(result_path, n_simu):
    MinMaxPx,MinMaxPy,MinMaxPz=[],[],[]
    MinMaxHx,MinMaxHy,MinMaxHz=[],[],[]
    MinMaxKx,MinMaxKy,MinMaxKz=[],[],[]
    MinMaxAx,MinMaxAz=[],[]
    MinMaxFp=[]
    MinMax=[MinMaxPx,MinMaxPy,MinMaxPz,\
            MinMaxHx,MinMaxHy,MinMaxHz,\
            MinMaxKx,MinMaxKy,MinMaxKz,\
            MinMaxAx,MinMaxAz,\
            MinMaxFp]
    for a in range(12):
        data_angle=[]
        for s in range(1,n_simu+1):
            if s<10:
                simu='0'+str(s)
            else:
                simu=str(s)
            data_angle.append(get_data(result_path+"\\p01_simu"+simu+".csv", a))
        for frame in range(len(data_angle[0])):
            minimum=data_angle[0][frame]
            maximum=data_angle[0][frame]
            for s in data_angle:
               if s[frame]<minimum:
                   minimum=s[frame]
               elif s[frame]>maximum:
                   maximum=s[frame]
            MinMax[a].append([minimum,maximum])
        print 'angle OK'
    return MinMax
                
    
def show_shadow_courbes(Angle_Names, result_path):
    Scales=[[-30,30],[-30,30],[-30,30],\
            [-40,80],[-30,30],[-40,20],\
            [-20,80],[-40,20],[-30,50],\
            [-30,50],[-40,20],[-40,20]]
    Y=[i for i in range(109)] 
    MinMax=get_min_max(result_path,390625)
    print 'MinMax list OK'
    for a in range(12):        
        fig=plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        Min=[]
        Max=[]
        for frame in MinMax[a]:
            Min.append(frame[0])
            Max.append(frame[1])
        print Min
        print Max
        ax.set_ylim(Scales[a][0],Scales[a][1])
        ax.fill_between(Y,Min,Max,color='lightgrey') #,cmap=c
        ax.plot(Y,Min, color='black',linewidth=0.3)
        ax.plot(Y,Max, color='black',linewidth=0.3)
        ax.plot(Y,[0]*len(Y),color='black',linewidth=1)
        print 'angle OK'
        ax.set_title(Angle_Names[a+4])
        plt.savefig("C:\Users\Mariette Bergere\Documents\Stage Geneve\Git\Analysis\\"+Angle_Names[a]+".jpeg")
    plt.show()
    
    
def show_curves(ref_file, mis_file ,Angle_Names):
    Scales=[[-30,30],[-30,30],[-30,30],\
            [-40,80],[-30,30],[-40,20],\
            [-20,80],[-40,20],[-30,50],\
            [-30,50],[-40,20],[-40,20]]
    Y=[i for i in range(109)] 
    for a in range(12):        
        Data_ref=get_data(ref_file, a)
        Data_mis=get_data(mis_file, a)
        fig=plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_ylim(Scales[a][0],Scales[a][1])
        ax.plot(Y,Data_ref, color='red',linewidth=2)
        ax.plot(Y,Data_mis, color='blue',linewidth=1.5)
        ax.plot(Y,[0]*len(Y),color='black',linewidth=1)
        ax.set_title(Angle_Names[a])
        plt.savefig("C:\Users\Mariette Bergere\Documents\Stage Geneve\Memoire\Illustrations\\reference "+Angle_Names[a]+".jpeg")
    plt.show()


    












