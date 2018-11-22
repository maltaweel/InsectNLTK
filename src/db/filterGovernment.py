'''
This is a filter used to choose document by material type, which represents types of 
government ogranizations in relation to given text. For example, Federal texts could be a government type searched for 
using the filter.

Created on May 11, 2018

@author: 
'''


def filterGovernmentType(gT, return_list):
    '''
    Method to apply the filter based on government type (i.e., material type in MPB_Source_Doc.csv"
    gT-- government type
    return_list containing text and data about texts
    '''
    result=[]
    
    
    for r in return_list:
        govLevel=r["Material"]
        code=r['Code']
        for gType in gT:
            
            if gType not in govLevel:
                print(code)
                result.append(r) 
    
    return result