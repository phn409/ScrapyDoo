from APS import APS
import pandas as pd

PRX=APS(abbrev='prx')
PRX.indexVolumes()
PRX.indexIssues(verbose=True,skip=3)

print('link current issue:',PRX.link())
print('link volume 3 issue 2:',PRX.link(vol=2,iss=4))
print('total number of volumes:',PRX.nVolumes)
print('total number of issues:',PRX.nIssues)

#%%

vol_iss = {'Vol': list(reversed([*PRX.volumes,])), 'Iss':[], 'Yr':[]}
for v in vol_iss['Vol']:
    #Print number of issues in each volume
    PRX.indexIssues(All = False, num = int(v))
    ni = PRX.volumes[v].nIssues
    vol_iss['Iss'].append(ni)
    print('Volume: {}, Issues: {}'.format(v, ni))
    for i in range(1, ni+1):
        print(PRX.link(vol=v, iss=i))
        r = PRX.monthRange(v, i)
    #Append to year column
    vol_iss['Yr'].append(r[1])        
VIDF = pd.DataFrame(vol_iss)
print(VIDF)
#%%
#Section to scrape a particular volume of a journal
#Print out the issue URL corresponding to each volume/issue
VL = 9
#for i in range(1, PRX.volumes[str(VL)].nIssues + 1):
print(PRX.link(vol=VL, iss=1))
PRX.monthRange(9, 1)    
PRX.issueListing(9, 1)
#to DF
#VIDF = pd.DataFrame(vol_iss)
#print(VIDF)
    
#Create paper objects with index ID