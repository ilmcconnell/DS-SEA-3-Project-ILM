# coding: utf-8
import pandas as pd
#import numpy as np

#Checkotu the crosswlk data strcutre
# https://www.huduser.gov/portal/datasets/usps_crosswalk.html

#ZIP	5 digit USPS ZIP code
#TRACT	11 digit unique 2000 Census tract code consisting of state + county + tract code. The decimal is implied and leading and trailing zeros have been preserved.
#COUNTY	5 digit unique 2000 Census county code consisting of state + county.
#CBSA	5 digit CBSA code for Micropolitan and Metropolitan Areas as defined by OMB in February of 2013. ZIP codes with a CBSA code of ‘99999’ are not located within a CBSA.
#RES_RATIO	The ratio of residential addresses in the ZIP – Tract, County, or CBSA part to the total number of residential addresses in the entire ZIP.
#BUS_RATIO	The ratio of business addresses in the ZIP – Tract, County, or CBSA part to the total number of business addresses in the entire ZIP.
#OTH_RATIO	The ratio of other addresses in the ZIP – Tract, County, or CBSA part to the total number of other addresses in the entire ZIP.
#TOTAL_RATIO	The ratio of all addresses in the ZIP – Tract, County, or CBSA part to the total number of all types of addresses in the entire ZIP.

path = '/Users/Iain/DS-SEA-3/DS-SEA-3-Project-ILM/data/HUD/'
filename = 'zip_county_062016.csv'

zipCountyCrosswalk = pd.read_csv(path + filename, converters={'ZIP':lambda x: str(x), 'COUNTY':lambda x:str(x)})


print zipCountyCrosswalk.head()

zipCountyCrosswalk.COUNTY.dtype

print zipCountyCrosswalk.columns

print len(zipCountyCrosswalk)




#check out FIPS to statand county name corsswalk strucutre
#https://www.census.gov/geo/reference/codes/cou.html

#These text files contain comma-delimited records for each county. The records are of the format:
#
#Field Name	Field Description	Example
#STATE	State Postal Code	FL
#STATEFP	State FIPS Code	12
#COUNTYFP	County FIPS Code	011
#COUNTYNAME	County Name and Legal/Statistical Area Description	Broward County
#CLASSFP	FIPS Class Code	H1
#
#FIPS Class Codes
#H1:  identifies an active county or statistically equivalent entity that does not qualify under subclass C7 or H6.
#H4:  identifies a legally defined inactive or nonfunctioning county or statistically equivalent entity that does not qualify under subclass H6.
#H5:  identifies census areas in Alaska, a statistical county equivalent entity.
#H6:  identifies a county or statistically equivalent entity that is areally coextensive or governmentally consolidated with an incorporated place, part of an incorporated place, or a consolidated city. 
#C7:  identifies an incorporated place that is an independent city; that is, it also serves as a county equivalent because it is not part of any county, and a minor civil division (MCD) equivalent because it is not part of any MCD.

#path = '/Users/Iain/DS-SEA-3/DS-SEA-3-Project-ILM/data/CensusCountyFIPS/'
#filename = 'StateCountyFIPSCrossWalk.csv'
#StateCountyFIPSCrosswalk = pd.read_csv(path + filename, converters={'StateFP':lambda x: str(x), 'CountyFP':lambda x: str(x)})
#print StateCountyFIPSCrosswalk.head()
#StateCountyFIPSCrosswalk.StateFP.dtype
#StateCountyFIPSCrosswalk['FIPS'] = StateCountyFIPSCrosswalk['StateFP']+StateCountyFIPSCrosswalk['CountyFP']
#print StateCountyFIPSCrosswalk.head()
#print len(StateCountyFIPSCrosswalk)


#chek out CMS data structures
path = '/Users/Iain/DS-SEA-3/DS-SEA-3-Project-ILM/data/cms/'

# Medicare_Provider_Charge_Outpatient_APC32_CY2014.csv
# Medicare_Provider_Charge_Outpatient_APC30_CY2013_v2.csv
# Medicare_Provider_Charge_Outpatient_APC30_CY2012.csv
# Medicare_Provider_Charge_Outpatient_APC30_CY2011_v2.csv



filename = 'Medicare_Provider_Charge_Outpatient_APC32_CY2014.csv'


paymentdata = pd.read_csv(path + filename, converters={'Provider_Zip_Code':lambda x: str(x)})

print paymentdata.columns

print len(paymentdata)

print paymentdata.head()

#pd.scatter_matrix(paymentdata)

#pd.scatter_matrix(paymentdata[[u'Provider_Zip_Code',u'Hospital_Referral_Region', u'Outpatient_Services', u'Average_Estimated_Submitted_Charges', u'Average_Total_Payments']])
       
       
#checktou the cencsus data structures
path = '/Users/Iain/DS-SEA-3/DS-SEA-3-Project-ILM/data/census/'

filename = 'census-data-by-county-2016.07.31-09.48PM.csv'

censusData = pd.read_csv(path + filename, converters={'state_fips':lambda x: str(x), 'county_fips':lambda x: str(x)})

censusData.head()

#censusData['state_fips'] = [ str(str('0') + str(row)) if len(row) == 1  else str(row) for row in censusData['state_fips']]
#df['ID'] = df['ID'].apply(lambda x: x.zfill(15))

censusData['state_fips'] = censusData['state_fips'].apply(lambda x: x.zfill(2))
censusData['county_fips'] = censusData['county_fips'].apply(lambda x: x.zfill(3))

censusData['FIPS'] = censusData['state_fips']+censusData['county_fips']

print censusData.head()


censusData['FIPS'].dtype

#zipCountyCrosswalk.head()
zipCountyCrosswalk.rename(columns={'COUNTY':'FIPS'}, inplace=True)
#zipCountyCrosswalk.head()


#censusData['FIPS'].dtype
#zipCountyCrosswalk['FIPS'].dtype

#zipCountyCrosswalk.to_string(columns=['FIPS'])

# zipCountyCrosswalk.head() #looks lie county is FIPS here

#StateCountyFIPSCrosswalk.head() #don't need this one

joined = pd.merge(censusData, zipCountyCrosswalk, on='FIPS', how='left')
joined.head()

paymentdata.rename(columns={'Provider_Zip_Code':'ZIP'}, inplace=True)
doublejoined = pd.merge(joined, paymentdata, on='ZIP', how = 'left')

print paymentdata.ZIP.dtype
print joined.ZIP.dtype

doublejoined.head(20)