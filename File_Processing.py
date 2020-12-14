# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:23:14 2019

@author: Mariette Bergere
MIS2 project
"""

import btk

def reader(file):
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(file) 
    reader.Update()
    acq=reader.GetOutput()
    return acq

def writer (acq, new_filename):
    writer = btk.btkAcquisitionFileWriter()
    writer.SetInput(acq)
    writer.SetFilename(new_filename)
    writer.Update()  