# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:41:28 2019

@author: Mariette Bergere
MIS2 project
"""
#    Points_To_Keep: list of str. Defined in MAIN


import Point_Manipulation
import btk
import File_Processing


def clear_acq(file):
    '''Simplifies an existing file'''
    acq=File_Processing.reader(file) 
    Point_Manipulation.remove_unused_makers(acq)
    Point_Manipulation.remove_meta_data(acq)
    File_Processing.writer(acq, file) 
    
    
def new_stat(stat_file, Points_To_Keep, frame_number):
    '''Overwrites a new static file from nothing, with elements 
    (points, frequency, frame number) to define'''
    acq=File_Processing.reader(stat_file) 
    f0=acq.GetFirstFrame()
    metadata=acq.GetMetaData()
    Values=[]
    Points=[]
    
    for p in range(acq.GetPointNumber()):
        Points.append(acq.GetPoint(p).GetLabel())
        
    NewPoints=[]
    for p in Points_To_Keep:
        if p in Points:
            values=acq.GetPoint(p).GetValues()[f0:f0+frame_number,:]
            Values.append(values)
            NewPoints.append(p)
    acq.Reset()
    acq.Init(len(Points_To_Keep), frame_number)
    acq.SetPointFrequency(20)
    acq.SetMetaData(metadata)
    for p in range(len(NewPoints)):
        new_point=btk.btkPoint(NewPoints[p],acq.GetPointFrameNumber())
        new_point.SetValues(Values[p])
        acq.AppendPoint(new_point)
    File_Processing.writer(acq, stat_file) 
    
    
def new_dyn(dyn_file, Points_To_Keep):
    '''Overwrites a new static file from nothing, with elements (points, frequency) to define. 
    Contains 1 gait cycle starting from event : Left foot strike.'''
    acq=File_Processing.reader(dyn_file) 
    Ev=acq.GetEvents()
    f0=acq.GetFirstFrame()
    metadata=acq.GetMetaData()
    lfs=1
    for ev in range(Ev.GetItemNumber()):
        event=Ev.GetItem(ev)
        if event.GetLabel()=='Foot Strike' and event.GetContext()=='Left' and lfs==1:
            first_lfs_frame=event.GetFrame() 
            lfs+=1
        elif event.GetLabel()=='Foot Strike' and event.GetContext()=='Left' and lfs==2:
            sec_lfs_frame=event.GetFrame()
            lfs+=1
    try:
        frame_numb=sec_lfs_frame+5-(first_lfs_frame-5)
        if first_lfs_frame-5-f0>=0:
            first_frame=first_lfs_frame-5-f0
        else:
            first_frame=first_lfs_frame-f0
        Values=[]
        Points=[]
        for p in range(acq.GetPointNumber()):
            Points.append(acq.GetPoint(p).GetLabel())
        NewPoints=[]
        for p in Points_To_Keep:
            if p in Points:
                values=acq.GetPoint(p).GetValues()[first_frame:sec_lfs_frame+1+5-f0,:]
    #            print values
                Values.append(values)
                NewPoints.append(p)
        acq.Reset()
        acq.Init(len(Points_To_Keep), frame_numb)
        acq.SetPointFrequency(20) #reduce computation time
        acq.SetMetaData(metadata)
        for p in range(len(NewPoints)):
            new_point=btk.btkPoint(NewPoints[p],acq.GetPointFrameNumber())
            new_point.SetValues(Values[p])
            acq.AppendPoint(new_point)
        File_Processing.writer(acq, dyn_file)             
    except:
        print("No last left foot strike detected")
    
    
   
    

    
    
    
    
    
    