###cleaning dob_ecb_viol.csv

import pandas as pd

df = pd.read_csv('~/mcnulty/dob_ecb_viol.csv', usecols=['ISN_DOB_BIS_EXTRACT', 'ECB_VIOLATION_STATUS', 'BIN', 'BORO', 'BLOCK', 'LOT', 'ISSUE_DATE', 'SEVERITY', 'VIOLATION_TYPE', 'AGGRAVATED_LEVEL', 'CERTIFICATION_STATUS'])
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#if empty, fill with negative values
df['AGGRAVATED_LEVEL'].fillna('NO', inplace=True)
df['CERTIFICATION_STATUS'].fillna('NO COMPLIANCE RECORDED', inplace=True)

df.drop_duplicates(inplace=True)

#getting rid of spaces
dev['ISSUE_DATE'] = dev['ISSUE_DATE'].astype(str).replace(' ','')

import re
#normalizing date
date_re = re.compile('[1-2][0-9][0-9][0-9][0-9][0-9][0-3][0-9]')
dev = dev[dev['ISSUE_DATE'].str.contains(date_re)]

#extracting year
dev['ISSUE_YEAR'] = dev['ISSUE_DATE'].str[0:4]
dev['ISSUE_YEAR'] = dev['ISSUE_YEAR'].astype(int, inplace=True)
#making sure years make sense
mask1 = dev['ISSUE_YEAR'] > 1899
mask2 = dev['ISSUE_YEAR'] < 2019
dev = dev[mask1 & mask2]

#extracting month and day
dev['ISSUE_MONTH'] = dev['ISSUE_DATE'].astype(str).str[4:6]
dev['ISSUE_DAY'] = dev['ISSUE_DATE'].astype(str).str[6:]

dev['ISSUE_YEAR'] = dev['ISSUE_YEAR'].astype(str)

#making sure month and day make sense
mask1 = dev['ISSUE_DAY'].astype(int) < 31
mask2 = dev['ISSUE_MONTH'].astype(int) < 12
dev = dev[mask1 & mask2]

#list of months with different days
thirtyone = [1,3,5,7,8,10,12]
thirty = [4,6,9,11]
twentynine = [2]

#sanity check to make sure all month make sense/fixing to latest day possible if larger than expected
mask1 = dev['ISSUE_DAY'].astype(int) > 29
mask2 = dev['ISSUE_DAY'].astype(int) > 30
mask3 = dev['ISSUE_DAY'].astype(int) > 31

mask4 = dev['ISSUE_MONTH'].astype(int).isin(thirtyone)
mask5 = dev['ISSUE_MONTH'].astype(int).isin(thirty)
mask6 = dev['ISSUE_MONTH'].astype(int).isin(twentynine)

dev[dev[mask1 & mask6]]['ISSUE_DAY']=29
dev[dev[mask2 & mask5]]['ISSUE_DAY']=30
dev[dev[mask3 & mask4]]['ISSUE_DAY']=31

#formatting date to convert to datetime format
dev['ISSUE_DATE_NEW'] = dev['ISSUE_MONTH'].astype(str) + '/' + dev['ISSUE_DAY'].astype(str) + '/' + dev['ISSUE_YEAR'].astype(str)

dev['ISSUE_DATE'] = pd.to_datetime(dev['ISSUE_DATE_NEW'], format='%m/%d/%Y', errors='coerce')

dev.head()

#dropping old columns
dev.drop(columns=['ISSUE_YEAR', 'ISSUE_MONTH', 'ISSUE_DAY', 'ISSUE_DATE_NEW'], inplace=True)

#no 6th borough
dev = dev[dev['BORO']!=6]
#not useful
dev.drop(columns=['BORO', 'BLOCK', 'LOT'], inplace=True)

df = df.reset_index(drop=True)

df.to_csv(‘~/mcnulty/dob_ecb_viol.csv’)

del df

###cleaning housing lits

import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#reformatting
hl = pd.read_csv('~/mcnulty/housing_litigations.csv')
hl['Boro'] = hl['Boro'].astype(str)
hl['Block'] = hl['Block'].astype(str)
hl['Lot'] = hl['Lot'].astype(str)

#creating BBL
hl['Block'] = hl['Block'].str.pad(5,fillchar='0')
hl['Lot'] = hl['Lot'].str.pad(4,fillchar='0')
hl['BBL2'] = hl['Boro']+hl['Block']+hl['Lot']
hl['BBL'] = hl['BBL2'].astype(int)

#converting to datetime
hl['CaseOpenDate'] = pd.to_datetime(hl['CaseOpenDate'])

#dropping extraneous information
hl.drop(columns=['BuildingID', 'HouseNumber', 'StreetName', 'Zip', 'Block', 'Lot', 'OpenJudgement', 'Latitude', 'Longitude', 'BBL2', 'NTA','FindingOfHarassment','FindingDate','Penalty','Respondent','Community District', 'Council District', 'Census Tract', 'BIN'], inplace=True)
hl.reset_index(drop=True, inplace=True)
hl.to_csv('~/mcnulty/housing_litigations.csv')


###cleaning hmc complaints
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

hmcc = pd.read_csv('~/mcnulty/hmc_complaints.csv')
hmcc.drop_duplicates(inplace=True)
hmcc.info()

hmcc['BoroughID'].value_counts()
#creating BBL
hmcc['BoroughID'] = hmcc['BoroughID'].astype(str)
hmcc['Block'] = hmcc['Block'].astype(str)
hmcc['Lot'] = hmcc['Lot'].astype(str)

hmcc['Block'] = hmcc['Block'].str.pad(5,fillchar='0')
hmcc['Lot'] = hmcc['Lot'].str.pad(4,fillchar='0')
hmcc['BBL'] = hmcc['BoroughID']+hmcc['Block']+hmcc['Lot']
hmcc['BBL'] = hmcc['BBL'].astype(int)

hmcc.info()
#dropping unnecessary columns
hmcc = hmcc[['ComplaintID', 'BuildingID', 'BBL', 'ReceivedDate', 'Status']]

hmcc.info()

hmcc.to_csv('~/mcnulty/hmc_complaints.csv')

###cleaning pluto
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

bk = pd.read_csv('~/mcnulty/PLUTO_for_WEB/BK_18v1.csv')
bk = bk[['CD', 'CT2010','SchoolDist', 'Council', 'ZipCode', 'FireComp', 'PolicePrct', 'Address','BldgClass','LandUse','OwnerType','LotArea','BldgArea','ComArea','ResArea','OfficeArea','RetailArea','GarageArea','StrgeArea','FactryArea','OtherArea','NumFloors','UnitsRes','UnitsTotal','BsmtCode','AssessTot','YearBuilt','YearAlter1','YearAlter2','BoroCode','BBL','XCoord','YCoord','PFIRM15_FLAG']
]

#fill with negative values
bk['LandUse'].fillna(0, inplace=True)

bk['BsmtCode'].fillna(5, inplace=True)

bk.drop_duplicates(inplace=True)
bk['PFIRM15_FLAG'].fillna(0,inplace=True)
bk['OwnerType'].fillna('NA',inplace=True)
bk['FireComp'].fillna('X000',inplace=True)
bk.to_csv('~/mcnulty/pluto_bk.csv')

#import all boroughs and concatenate

pluto = pd.concat([si,bk,bx,mn,qn])
pluto.to_csv('~/mcnulty/pluto.csv')

###cleaning dob violations
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

dv = pd.read_csv('~/mcnulty/dv_new.csv')
dv.info()
#dropping unnecessary columns
dv = dv[['ISN_DOB_BIS_VIOL', 'BORO', 'BIN', 'BLOCK', 'LOT', 'ISSUE_DATE', 'VIOLATION_TYPE_CODE', 'VIOLATION_CATEGORY']]
dv.dropna(inplace=True)

#creating BBL
dv['BORO'] = dv['BORO'].apply(lambda x: str(x))
dv['BORO'] = dv['BORO'].apply(lambda x: x.strip())
dv['BORO'].isna().sum()

dv['BORO'] = dv['BORO'].replace('M',1)
dv['BORO'] = dv['BORO'].replace('Q',4)
dv['BORO'] = dv['BORO'].replace('S',5)
dv = dv[dv['BORO']!='`']
dv = dv[dv['BORO']!='B']

dv['BORO'] = pd.to_numeric(dv['BORO'], errors='coerce')

dv['BORO'] = dv['BORO'].apply(lambda x: int(x))
dv = dv[dv['BORO']!=0]

dv['BLOCK'] = pd.to_numeric(dv['BLOCK'], errors='coerce')
dv.dropna(inplace=True)
dv['BLOCK'] = dv['BLOCK'].apply(lambda x: int(x))

dv['LOT'] = pd.to_numeric(dv['LOT'], errors='coerce')
dv.dropna(inplace=True)
dv['LOT'] = dv['LOT'].apply(lambda x: int(x))

#reformatting date
dv['ISSUE_DATE'] = dv['ISSUE_DATE'].astype(str).replace(' ','')

import re
date_re = re.compile('[1-2][0-9][0-9][0-9][0-9][0-9][0-3][0-9]')
dv = dv[dv['ISSUE_DATE'].str.contains(date_re)]

dv['ISSUE_YEAR'] = dv['ISSUE_DATE'].str[0:4]
dv['ISSUE_YEAR'] = dv['ISSUE_YEAR'].astype(int, inplace=True)
mask1 = dv['ISSUE_YEAR'] > 1899
mask2 = dv['ISSUE_YEAR'] < 2019
dv = dv[mask1 & mask2]

dv['ISSUE_MONTH'] = dv['ISSUE_DATE'].astype(str).str[4:6]
dv['ISSUE_DAY'] = dv['ISSUE_DATE'].astype(str).str[6:]

dv['ISSUE_YEAR'] = dv['ISSUE_YEAR'].astype(str)

mask1 = dv['ISSUE_DAY'].astype(int) < 31
mask2 = dv['ISSUE_MONTH'].astype(int) < 12
dv = dv[mask1 & mask2]

thirtyone = [1,3,5,7,8,10,12]
thirty = [4,6,9,11]
twentynine = [2]

mask1 = dv['ISSUE_DAY'].astype(int) > 29
mask2 = dv['ISSUE_DAY'].astype(int) > 30
mask3 = dv['ISSUE_DAY'].astype(int) > 31

mask4 = dv['ISSUE_MONTH'].astype(int).isin(thirtyone)
mask5 = dv['ISSUE_MONTH'].astype(int).isin(thirty)
mask6 = dv['ISSUE_MONTH'].astype(int).isin(twentynine)

dv[dv[mask1 & mask6]]['ISSUE_DAY']=29
dv[dv[mask2 & mask5]]['ISSUE_DAY']=30
dv[dv[mask3 & mask4]]['ISSUE_DAY']=31

dv['ISSUE_DATE_NEW'] = dv['ISSUE_MONTH'].astype(str) + '/' + dv['ISSUE_DAY'].astype(str) + '/' + dv['ISSUE_YEAR'].astype(str)

dv['ISSUE_DATE'] = pd.to_datetime(dv['ISSUE_DATE_NEW'], format='%m/%d/%Y', errors='coerce')

dv.dropna(inplace=True)

#trying to get consistent values for violation category
dv['vc'] = dv['VIOLATION_CATEGORY'].str.split('-').apply(lambda x:x[-1])
dv['vc'] = dv['vc'].str.strip()
dv['vc'] = dv['vc'].str.split()
dv['vc'].value_counts()

dv['vc'] = dv['vc'].apply(lambda x: x[-1])
dv['vc'] = dv['vc'].str.upper()

violcats = ['DISMISSED', 'RESOLVED', 'ACTIVE']
mask = dv['vc'].isin(violcats)

dv = dv[mask]
dv['VIOLATION_CATEGORY'] = dv['vc']

dv.drop(columns=['ISSUE_YEAR', 'ISSUE_MONTH', 'ISSUE_DAY', 'ISSUE_DATE_NEW', 'vc'], inplace=True)

dv['bl'] = dv['BLOCK'].apply(lambda x: len(str(int(x))))
dv['ll'] = dv['LOT'].apply(lambda x: len(str(int(x))))

dv = dv[dv['ll']!=5]
#getting BBL
dv['BLOCK'] = dv['BLOCK'].apply(lambda x: str(int(x)))
dv['BORO'] = dv['BORO'].apply(lambda x: str(int(x)))
dv['LOT'] = dv['LOT'].apply(lambda x: str(int(x)))

dv['BLOCK'] = dv['BLOCK'].str.pad(5,fillchar='0')
dv['LOT'] = dv['LOT'].str.pad(4,fillchar='0')
dv['BBL'] = dv['BORO']+dv['BLOCK']+dv['LOT']
dv['BBL'] = dv['BBL'].astype(int)

dv.dropna(inplace=True)

#drop unnecessary columns
dv.drop(columns=['BORO','BLOCK','LOT','bl','ll'],inplace=True)

dv.to_csv('~/mcnulty/dob_complaints.csv')

### cleaning 311
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#have to load in chunks so creating paths for all files
paths = []
for i in range(0,188):
    path = '~/mcnulty/chunk' + str(i) + '.csv'
    paths.append(path)

#loading in chunks and cleaning by getting rid of complaints not associated with specific building
for each in paths:
    df = pd.read_csv(each, usecols=['Unique Key', 'Created Date', 'Agency', 'Complaint Type', 'Descriptor', 'Location Type', 'Status', 'BBL', 'Borough', 'X Coordinate (State Plane)', 'Y Coordinate (State Plane)', 'Latitude', 'Longitude', 'Location'])
    df = df[~df['BBL'].isna()]
    df['Created Date'] = pd.to_datetime(df['Created Date'])
    df.drop_duplicates(inplace=True)
    df.to_csv(each)
    del df

#concatenating chunks
dfs = []
for each in paths:
    df = pd.read_csv(each)
    dfs.append(df)

threeoneone = pd.concat(dfs)

threeoneone.drop_duplicates(inplace=True)

threeoneone.drop(columns='Unnamed: 0', inplace=True)
threeoneone.reset_index(drop=True)

threeoneone['Created Date'] = pd.to_datetime(threeoneone['Created Date'])

threeoneone.to_csv('~/mcnulty/311.csv')

### cleaning dob complaints
dc = pd.read_csv('~/rows.csv')
dc.drop_duplicates(inplace=True)
#dropping unnecessary columns
dc = dc[['Complaint Number', 'Status', 'Date Entered', 'House Number','House Street', 'BIN', 'Community Board']]

#getting borough
dc['Borough'] = dc['Community Board'].apply(lambda x: str(x)[0])
dc = dc[dc['Borough']!=' ']
dc['Borough'] = dc['Borough'].apply(lambda x: int(x))

dc['Date Entered']=pd.to_datetime(dc['Date Entered'])
dc.reset_index(inplace=True)
dc.to_csv('~/mcnulty/dc.csv')

### cleaning hv
hv = pd.read_csv('~/mcnulty/hmc_viol.csv')
import re
#getting violations associated with date and reformatting dates
date = re.compile('[0-1][0-9]/[0-3][0-9]/[1-2][0-9][0-9][0-9]')
hv = hv[hv['InspectionDate'].str.contains(date)]
hv = hv[hv['ApprovedDate'].str.contains(date)]

hv['InspectionDate'] = pd.to_datetime(hv['InspectionDate'], format='%m/%d/%Y')
hv['ApprovedDate'] = pd.to_datetime(hv['ApprovedDate'], format='%m/%d/%Y')
hv.drop(columns='Unnamed: 0', inplace=True)
hv.to_csv('~/mcnulty/hmc_viol.csv')

#housing lit data
hl = pd.read_csv('~/mcnulty/housing_litigations.csv')
#getting number of litigations for each building
hlbbls = dict(hl['BBL'].value_counts())
bbl['lits'] = 0
for i in bbl.index:
    if bbl.at[i,'BBL'] in hlbbls:
        bbl.at[i, 'lits'] = hlbbls[bbl.at[i,'BBL']]
    else:
        pass
bbl['has_lit'] = 0
#if building has litigation, 1
for i in bbl.index:
    if bbl.at[i,'lits'] > 0:
        bbl.at[i, 'has_lit'] = 1
    else:
        pass
del hl
del hlbbls

#311 complaints
t = pd.read_csv('~/mcnulty/311.csv')
t['BBL'] = t['BBL'].apply(lambda x: int(x))
tbbls = dict(t['BBL'].value_counts())
bbl['311'] = 0
for i in bbl.index:
    if bbl.at[i,'BBL'] in tbbls:
        bbl.at[i, '311'] = tbbls[bbl.at[i,'BBL']]
    else:
        pass
del t

#hmc violations
hv = pd.read_csv('~/mcnulty/hmc_viol.csv')
hvbbls = dict(hv['BBL'].value_counts())
bbl['hmc_v'] = 0
#getting number of violations
for i in bbl.index:
    if bbl.at[i,'BBL'] in hvbbls:
        bbl.at[i, 'hmc_v'] = hvbbls[bbl.at[i,'BBL']]
    else:
        pass
del hv

#hmc complaints
hc = pd.read_csv('~/mcnulty/hmc_complaints.csv')

hcbbls = dict(hc['BBL'].value_counts())

bbl['hmc_c'] = 0
#getting number of hmc complaints
for i in bbl.index:
    if bbl.at[i,'BBL'] in hcbbls:
        bbl.at[i, 'BBL'] = hcbbls[bbl.at[i,'BBL']]
    else:
        pass
del hc

#for mvp analysis

pluto = pd.read_csv('~/mcnulty/pluto.csv')
pluto.drop(columns='Unnamed: 0', inplace=True)
bbl.drop(columns='Unnamed: 0', inplace=True)
pluto = pluto.merge(bbl, on='BBL')

pluto.to_csv('mvpfile.csv')


#getting bbls for bins in dob complaints
hv = pd.read_csv('~/mcnulty/hv.csv')
binbbl = hv[['BIN','BBL']]
binbbl.drop_duplicates(inplace=True)
binbbl.drop_duplicates(subset='BIN',inplace=True)
binbbl.drop_duplicates(subset='BBL',inplace=True)
binbbls = dict()
for i in binbbl.index:
    binbbls[binbbl.at[i,'BIN']]=binbbl.at[i,'BBL']
dc = pd.read_csv('~/mcnulty/dc.csv')
dc['BBL']=None
for i in dc.index:
    if dc.at[i,'BIN'] in binbbls:
        dc.at[i,'BBL']=binbbls[dc.at[i,'BIN']]
dc.drop(columns=['House Number','House Street'], inplace=True)
dc.dropna(inplace=True)
dc.to_csv('~/mcnulty/dc_w_bbls.csv')
