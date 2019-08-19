from APS import APS

PRX=APS(abbrev='prx')
PRX.indexVolumes()
PRX.indexIssues(verbose=True,skip=3)

print('link current issue:',PRX.link())
print('link volume 3 issue 2:',PRX.link(vol=2,iss=4))
print('total number of volumes:',PRX.nVolumes)
print('total number of issues:',PRX.nIssues)
