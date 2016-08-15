# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 15:49:10 2016

@author: Iain
"""
#IMPORT PANDAS
import pandas as pd

#CREATE CROSSWALK DATAFRAME
path = '/Users/Iain/DS-SEA-3/DS-SEA-3-Project-ILM/data/HUD/'
filename = 'zip_county_062016.csv'
zipCountyCrosswalk = pd.read_csv(path + filename, converters={'ZIP':lambda x: str(x), 'COUNTY':lambda x:str(x)})

#CREATE CMS 2014 OUTPAITENT PAYMENT INFO DATA FRAME - ENSURE LEADING ZEROS PRESENT ON ZIP CODES
path = '/Users/Iain/DS-SEA-3/DS-SEA-3-Project-ILM/data/cms/'
filename = 'Medicare_Provider_Charge_Outpatient_APC32_CY2014.csv'
rawPaymentData = pd.read_csv(path + filename, converters={'Provider_Zip_Code':lambda x: str(x)})
rawPaymentData['Provider_Zip_Code'] = rawPaymentData['Provider_Zip_Code'].apply(lambda x: x.zfill(5))

#SIMPLIFY PAYMENT INFO DOWN TO SUMMED PAYMENTS PER ZIPCODE
rawPaymentData['Total'] = rawPaymentData['Outpatient_Services'] * rawPaymentData['Average_Total_Payments'] 
paymentData = rawPaymentData[['Provider_Zip_Code','Total']].groupby(by='Provider_Zip_Code', as_index=False).sum()

#CREATE CENSUSDATA DATAFRAME
path = '/Users/Iain/DS-SEA-3/DS-SEA-3-Project-ILM/data/census/'
filename = 'census-data-by-county-2016.07.31-09.48PM.csv'
censusData = pd.read_csv(path + filename, converters={'state_fips':lambda x: str(x), 'county_fips':lambda x: str(x)})

#CREATE FIPS CODE IN CENSUSDATA DATAFRAME
censusData['state_fips'] = censusData['state_fips'].apply(lambda x: x.zfill(2))
censusData['county_fips'] = censusData['county_fips'].apply(lambda x: x.zfill(3))
censusData['FIPS'] = censusData['state_fips']+censusData['county_fips']

#CHANGE COLUMS NAMES TO MERGE BY THOSE COLUMN NAMES
zipCountyCrosswalk.rename(columns={'COUNTY':'FIPS'}, inplace=True)
paymentData.rename(columns={'Provider_Zip_Code':'ZIP'}, inplace=True)

#MERGE CENSUS AND ZIP CROSSWALK DATA FRAME
censusZip = pd.merge(censusData, zipCountyCrosswalk, on='FIPS', how='left')

#MEREGE THE CENSUSZIP DATAFRAME AND THE CMS PAYMENT DATA DATAFRAME
censusZipPayment = pd.merge(censusZip, paymentData, on='ZIP', how = 'left')

print censusZipPayment.head(50)

zipCountyCrosswalk.info #52314 ZIPS

paymentData.info #2806 unique ZIPs

censusData.info #10 rows only.

censusZipPayment.info