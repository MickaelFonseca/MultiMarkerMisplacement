# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 15:13:09 2019

@author: Mariette Bergere
MIS2 project
"""
#    Combi: list of misplacement combinaisons  (Combi=Definition.definition_combi(current_path)[0] or definition_combi_Della_Croce )
#    Angle_Names: list of angle names defined in MAIN_Misplacement
#    Values: list of list. len(Values)=12 (each angle). len(Values[0])=frame_number.
#    simu: int, simulation n°
#    patient: int, patient n°

    
def combinaisons(result_path,Combi):
    """n° simulation -> [mark1, [angle_direction, magnitude]],.. [mark8, [angle_direction, magnitude]] """
    with open(result_path+"\\"+"combinaisons.txt","w") as f:
        for c in Combi:
            f.write(str(c))
            f.write("\n")
    f.close()


def store_angles(Angle_Names, Values, simu, patient, result_path):
    if patient<=9:
        pat=str(0)+str(patient)
    else:
        pat=str(patient)
    f=open(result_path+"\\"+"p"+pat+"_"+ str(simu)+'.csv', 'w')  
    frame_number=len(Values[0])
    for angle in Values:
        if len(angle)<frame_number:
            frame_number=len(angle)
    f.write(";") 
    for angle_name in Angle_Names:
        f.write(angle_name+";")
    f.write("\n")
    for frame in range(frame_number):
        f.write("frame "+str(frame+1)+";")
        for angle in range(len(Values)):
            f.write(str(Values[angle][frame])+";")
        f.write("\n")
    f.close()

        
    




            

    


