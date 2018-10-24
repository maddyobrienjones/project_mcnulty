###cleaning dob_ecb_viol.csv

import pandas as pd

df = pd.read_csv('~/mcnulty/dob_ecb_viol.csv', usecols=['ISN_DOB_BIS_EXTRACT', 'ECB_VIOLATION_STATUS', 'BIN', 'BORO', 'BLOCK', 'LOT', 'ISSUE_DATE', 'SEVERITY', 'VIOLATION_TYPE', 'AGGRAVATED_LEVEL', 'CERTIFICATION_STATUS'])
pd.set_option('display.float_format', lambda x: '%.2f' % x)

df['AGGRAVATED_LEVEL'].fillna('NO', inplace=True)
df['CERTIFICATION_STATUS'].fillna('NO COMPLIANCE RECORDED', inplace=True)

df.drop_duplicates(inplace=True)

dev['ISSUE_DATE'] = dev['ISSUE_DATE'].astype(str).replace(' ','')

import re
date_re = re.compile('[1-2][0-9][0-9][0-9][0-9][0-9][0-3][0-9]')
dev = dev[dev['ISSUE_DATE'].str.contains(date_re)]

dev['ISSUE_YEAR'] = dev['ISSUE_DATE'].str[0:4]
dev['ISSUE_YEAR'] = dev['ISSUE_YEAR'].astype(int, inplace=True)
mask1 = dev['ISSUE_YEAR'] > 1899
mask2 = dev['ISSUE_YEAR'] < 2019
dev = dev[mask1 & mask2]

dev['ISSUE_MONTH'] = dev['ISSUE_DATE'].astype(str).str[4:6]
dev['ISSUE_DAY'] = dev['ISSUE_DATE'].astype(str).str[6:]

dev['ISSUE_YEAR'] = dev['ISSUE_YEAR'].astype(str)

mask1 = dev['ISSUE_DAY'].astype(int) < 31
mask2 = dev['ISSUE_MONTH'].astype(int) < 12
dev = dev[mask1 & mask2]

thirtyone = [1,3,5,7,8,10,12]
thirty = [4,6,9,11]
twentynine = [2]

mask1 = dev['ISSUE_DAY'].astype(int) > 29
mask2 = dev['ISSUE_DAY'].astype(int) > 30
mask3 = dev['ISSUE_DAY'].astype(int) > 31

mask4 = dev['ISSUE_MONTH'].astype(int).isin(thirtyone)
mask5 = dev['ISSUE_MONTH'].astype(int).isin(thirty)
mask6 = dev['ISSUE_MONTH'].astype(int).isin(twentynine)

dev[dev[mask1 & mask6]]['ISSUE_DAY']=29
dev[dev[mask2 & mask5]]['ISSUE_DAY']=30
dev[dev[mask3 & mask4]]['ISSUE_DAY']=31

dev['ISSUE_DATE_NEW'] = dev['ISSUE_MONTH'].astype(str) + '/' + dev['ISSUE_DAY'].astype(str) + '/' + dev['ISSUE_YEAR'].astype(str)

dev['ISSUE_DATE'] = pd.to_datetime(dev['ISSUE_DATE_NEW'], format='%m/%d/%Y', errors='coerce')

dev.head()

dev.drop(columns=['ISSUE_YEAR', 'ISSUE_MONTH', 'ISSUE_DAY', 'ISSUE_DATE_NEW'], inplace=True)
dev = dev[dev['BORO']!=6]
dev.drop(columns=['BORO', 'BLOCK', 'LOT'], inplace=True)

df = df.reset_index(drop=True)

df.to_csv(‘~/mcnulty/dob_ecb_viol.csv’)

del df

###cleaning housing lits

import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

hl = pd.read_csv('~/mcnulty/housing_litigations.csv')
hl['Boro'] = hl['Boro'].astype(str)
hl['Block'] = hl['Block'].astype(str)
hl['Lot'] = hl['Lot'].astype(str)

hl['Block'] = hl['Block'].str.pad(5,fillchar='0')
hl['Lot'] = hl['Lot'].str.pad(4,fillchar='0')
hl['BBL2'] = hl['Boro']+hl['Block']+hl['Lot']
hl['BBL'] = hl['BBL2'].astype(int)

hl['CaseOpenDate'] = pd.to_datetime(hl['CaseOpenDate'])

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

hmcc['BoroughID'] = hmcc['BoroughID'].astype(str)
hmcc['Block'] = hmcc['Block'].astype(str)
hmcc['Lot'] = hmcc['Lot'].astype(str)

hmcc['Block'] = hmcc['Block'].str.pad(5,fillchar='0')
hmcc['Lot'] = hmcc['Lot'].str.pad(4,fillchar='0')
hmcc['BBL'] = hmcc['BoroughID']+hmcc['Block']+hmcc['Lot']
hmcc['BBL'] = hmcc['BBL'].astype(int)

hmcc.info()

hmcc = hmcc[['ComplaintID', 'BuildingID', 'BBL', 'ReceivedDate', 'Status']]

hmcc.info()

hmcc.to_csv('~/mcnulty/hmc_complaints.csv')

###cleaning pluto
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

bk = pd.read_csv('~/mcnulty/PLUTO_for_WEB/BK_18v1.csv')
bk = bk[['FireComp', 'PolicePrct', 'LandUse', 'OwnerType', 'LotArea', 'BldgArea', 'ComArea', 'ResArea', 'OfficeArea', 'RetailArea', 'GarageArea', 'StrgeArea', 'FactryArea', 'OtherArea', 'NumFloors', 'UnitsRes', 'UnitsTotal', 'LotType', 'BsmtCode', 'AssessTot', 'YearBuilt', 'YearAlter1', 'BoroCode', 'BBL', 'XCoord', 'YCoord']]
bk.drop(columns=['XCoord', 'YCoord'], inplace=True)
bk.drop(columns=['FireComp', 'PolicePrct', 'OwnerType'], inplace=True)

#using 0 as unspecified value
bk['LandUse'].fillna(0, inplace=True)

#filling nulls with value for 'unknown'
bk['LotType'].fillna(0, inplace=True)

#filling nulls with value for unknown
bk['BsmtCode'].fillna(5, inplace=True)

bk.drop_duplicates(inplace=True)
bk.to_csv('~/mcnulty/pluto_bk.csv')


bx = pd.read_csv('~/mcnulty/PLUTO_for_WEB/BX_18v1.csv')
bx = bx[['FireComp', 'PolicePrct', 'LandUse', 'OwnerType', 'LotArea', 'BldgArea', 'ComArea', 'ResArea', 'OfficeArea', 'RetailArea', 'GarageArea', 'StrgeArea', 'FactryArea', 'OtherArea', 'NumFloors', 'UnitsRes', 'UnitsTotal', 'LotType', 'BsmtCode', 'AssessTot', 'YearBuilt', 'YearAlter1', 'BoroCode', 'BBL', 'XCoord', 'YCoord']]
bx.drop(columns=['XCoord', 'YCoord'], inplace=True)
bx.drop(columns=['FireComp', 'PolicePrct', 'OwnerType'], inplace=True)

#using 0 as unspecified value
bx['LandUse'].fillna(0, inplace=True)

#filling nulls with value for 'unknown'
bx['LotType'].fillna(0, inplace=True)

#filling nulls with value for unknown
bx['BsmtCode'].fillna(5, inplace=True)

bx.drop_duplicates(inplace=True)

bx.to_csv('~/mcnulty/pluto_bx.csv')


mn = pd.read_csv('~/mcnulty/PLUTO_for_WEB/MN_18v1.csv')

mn = mn[['FireComp', 'PolicePrct', 'LandUse', 'OwnerType', 'LotArea', 'BldgArea', 'ComArea', 'ResArea', 'OfficeArea', 'RetailArea', 'GarageArea', 'StrgeArea', 'FactryArea', 'OtherArea', 'NumFloors', 'UnitsRes', 'UnitsTotal', 'LotType', 'BsmtCode', 'AssessTot', 'YearBuilt', 'YearAlter1', 'BoroCode', 'BBL', 'XCoord', 'YCoord']]
mn.drop(columns=['XCoord', 'YCoord'], inplace=True)
mn.drop(columns=['FireComp', 'PolicePrct', 'OwnerType'], inplace=True)

#using 0 as unspecified value
mn['LandUse'].fillna(0, inplace=True)

#filling nulls with value for 'unknown'
mn['LotType'].fillna(0, inplace=True)

#filling nulls with value for unknown
mn['BsmtCode'].fillna(5, inplace=True)

mn.drop_duplicates(inplace=True)
mn.to_csv('~/mcnulty/pluto_mn.csv')

qn = pd.read_csv('~/mcnulty/PLUTO_for_WEB/QN_18v1.csv')
qn = qn[['FireComp', 'PolicePrct', 'LandUse', 'OwnerType', 'LotArea', 'BldgArea', 'ComArea', 'ResArea', 'OfficeArea', 'RetailArea', 'GarageArea', 'StrgeArea', 'FactryArea', 'OtherArea', 'NumFloors', 'UnitsRes', 'UnitsTotal', 'LotType', 'BsmtCode', 'AssessTot', 'YearBuilt', 'YearAlter1', 'BoroCode', 'BBL', 'XCoord', 'YCoord']]
qn.drop(columns=['XCoord', 'YCoord'], inplace=True)
qn.drop(columns=['FireComp', 'PolicePrct', 'OwnerType'], inplace=True)

#using 0 as unspecified value
qn['LandUse'].fillna(0, inplace=True)

#filling nulls with value for 'unknown'
qn['LotType'].fillna(0, inplace=True)

#filling nulls with value for unknown
qn['BsmtCode'].fillna(5, inplace=True)

qn.drop_duplicates(inplace=True)
qn.to_csv('~/mcnulty/pluto_qn.csv')


si = pd.read_csv('~/mcnulty/PLUTO_for_WEB/SI_18v1.csv')
si = si[['FireComp', 'PolicePrct', 'LandUse', 'OwnerType', 'LotArea', 'BldgArea', 'ComArea', 'ResArea', 'OfficeArea', 'RetailArea', 'GarageArea', 'StrgeArea', 'FactryArea', 'OtherArea', 'NumFloors', 'UnitsRes', 'UnitsTotal', 'LotType', 'BsmtCode', 'AssessTot', 'YearBuilt', 'YearAlter1', 'BoroCode', 'BBL', 'XCoord', 'YCoord']]
si.drop(columns=['XCoord', 'YCoord'], inplace=True)
si.drop(columns=['FireComp', 'PolicePrct', 'OwnerType'], inplace=True)

#using 0 as unspecified value
si['LandUse'].fillna(0, inplace=True)

#filling nulls with value for 'unknown'
si['LotType'].fillna(0, inplace=True)

#filling nulls with value for unknown
si['BsmtCode'].fillna(5, inplace=True)

si.drop_duplicates(inplace=True)
si.to_csv('~/mcnulty/pluto_si.csv')

pluto = pd.concat([si,bk,bx,mn,qn])
pluto.drop(columns=['Unnamed: 0'], inplace=True)
pluto.to_csv('~/mcnulty/pluto.csv')

###cleaning dob violations
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)

dv = pd.read_csv('~/mcnulty/dob_viol.csv')
dv.info()

dv = dv[['ISN_DOB_BIS_VIOL', 'BORO', 'BIN', 'BLOCK', 'LOT', 'ISSUE_DATE', 'VIOLATION_TYPE_CODE', 'VIOLATION_CATEGORY']]
dv = dv.dropna(axis=0)

dv['ISSUE_DATE'].value_counts()

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

dv.dropna(inplace=True)
dv.reset_index(drop=True, inplace=True)

dv = dv[dv['BORO']!='`']
dv['BORO'] = dv['BORO'].apply(lambda x: int(x))
dv = dv.dropna()
dv = dv[dv['BORO']!=0]

dv = dv.dropna()

numbers = re.compile('\d+')
#? dv['blockre'] = dv['BLOCK'].str.findall(numbers)
