# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 16:46:18 2022

@author: oOMaikOo
"""

'''
This file will give you:
    
    ICM : Value
    ICM_Et : Value
    Mean : x | std : x | MinVal : x | MaxVal : x | cpk : x
    
    and a graphical plot
'''


import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

start = time.time()
print("################# START #################")

''' loads a full set of data. each row has seperate measurment vaules

    |NAME |
    |value|
    |value|
    
'''
data_full = pd.read_excel("data_full.xlsx")
''' loads a set of specification limits. each row has seperate specification limit

    |NAME   |
    |Nominal|
    |Lower  |
    |Upper  |
    
'''
data_spec = pd.read_excel("data_spec.xlsx")

tmp = list(data_full._get_numeric_data().columns.values.tolist())

def f(full, ctf, spec):
    cpk = 0 
### def f(x, y, z)
###        function input x = pd.DataFrame all measured values per variable in a row
###        function input y = series of characteristic names
###        function input z = pd.DataFrame all specification limites per variable in a row


    # USL = Upper Specification Limit | LSL = Lower Specification Limit | tvalue = Target Value (Nominal Value)
    USL=spec[ctf].max()
    LSL=spec[ctf].min()
    tvalue= spec[ctf].mean()
    
    # mu = Mean Value of given values | std = Standart Deviation of give Values
    mu = full[ctf].mean()
    std = full[ctf].std()
    
    # MIN = Minimum Value of given Values | MAX = Maximum Value if given Values
    MIN = full[ctf].min()
    MAX = full[ctf].max()
    
    # Mean deviation of mean value to the target value
    mean_deviation = mu - tvalue
    
    #crit = round((mean_deviation)*2,2)
    
    # If the Upper Specification Limit minus the Lower Specification Limit greater than 0
    if USL - LSL > 0:
        ''' ICM
        Multiply the deviation of the mean value from the nominal value by 
        a factor of 2 and divide this by the 
        result of the upper tolerance limit minus the lower tolerance limit.
        '''
        ICM = round((2 * mean_deviation) / (USL - LSL),2)
        
        ''' ICM_Et
        Calculate the maximum measured value minus the minimum measured value (distance).
        and divide this by the 
        result of the upper tolerance limit minus the lower tolerance limit.
        '''
        ICM_Et = round((MAX - MIN) / (USL - LSL) ,2)
        
        print("ICM : " + str(ICM))
        print("ICM_Et : " +str(ICM_Et))
        
    # IF std unequal 0 | bc dividing by 0 not possible
    if std != 0:
        cpk=np.min([(USL-mu)/(3*std),(mu-LSL)/(3*std)])
        
    # Summary in variable tmp
    tmp = "Mean : " + str(round(full[ctf].mean(),2)) + " | std : " + str(round(full[ctf].std(),2)) + " | MinVal : " + str(round(MIN,2)) + " | MaxVal : " + str(round(MAX,2)) + " | cpk : " + str(round(cpk, 2))
    
    return tmp

for selection in tmp:
    print("############################# ||"+selection+"|| #############################\n")
    
    print(f(data_full, selection, data_spec))
    
    plt.hist(data_full[selection], bins=20, color='c', edgecolor='k', alpha=0.65)
    plt.axvline(data_full[selection].mean(), color='k', linestyle='dashed', linewidth=1)
    plt.axvline(data_spec[selection].min(), color='r', linestyle='dashed', linewidth=3)
    plt.axvline(data_spec[selection].max(), color='r', linestyle='dashed', linewidth=3)
    
    min_ylim, max_ylim = plt.ylim()
    min_xlim, max_xlim = plt.xlim()
    
    plt.text(data_full[selection].mean(), (max_ylim*0.9), 'Mean: {:.2f}'.format(data_full[selection].mean()))
    plt.text(data_spec[selection].max(), (max_ylim*0.1), 'USL: {:.2f}'.format(data_spec[selection].max()))
    plt.text(data_spec[selection].min(), (max_ylim*0.1), 'LSL: {:.2f}'.format(data_spec[selection].min()))
    plt.show()

end = time.time()
print("################# FINISH #################")
print((end - start))