# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 15:49:10 2016

@author: Iain
"""
#IMPORT PANDAS NUMPY MATPLOTLIB AND SEABORN
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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
filename = 'census-data-by-county-2016.08.15-03.48AM.csv'
censusData = pd.read_csv(path + filename,   converters={'state_fips':lambda x: str(x), 'county_fips':lambda x: str(x)})

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

print zipCountyCrosswalk.shape #52314 ZIPS

print paymentData.shape #2806 unique ZIPs

print censusData.shape #3143 rows

print censusZipPayment.shape #52033 rows

#ELIMINATE COLUMNS THAT ARE JUST NaN
del censusZipPayment['Unnamed: 4']
del censusZipPayment['Urban:_2010']
del censusZipPayment['Urban: !! Inside urbanized areas_2010']
del censusZipPayment['Urban: !! Inside urban clusters_2010']
del censusZipPayment['Rural !! Inside urban clusters_2010'] 

#DROP ALL ROWS CONTAINING NaN
censusZipPaymentNoNan = pd.DataFrame(censusZipPayment.dropna())

censusZipPaymentNoNan.shape #3877 rwos left.

#still need to multiple though county/zip splits
censusZipPaymentNoNan.columns.values
censusZipPaymentNoNan.head()
collist = ['2-person household H13. Household Size [8]_2010',
'3-person household H13. Household Size [8]_2010',
'4-person household H13. Household Size [8]_2010',
'5-person household H13. Household Size [8]_2010',
'6-person household H13. Household Size [8]_2010',
'7-or-more-person household H13. Household Size [8]_2010',
'Total population_2010', 'White alone_2010',
'Black or African American alone_2010',
'American Indian and Alaska Native alone_2010', 'Asian alone_2010',
'Native Hawaiian and Other Pacific Islander alone_2010',
'Some Other Race alone_2010', 'Two or More Races_2010',
'Not Hispanic or Latino_2010', 'Hispanic or Latino_2010',
'Total Population_2010', 'Male:_2010', 'Male: !! Under 5 years_2010',
'Male: !! 5 to 9 years_2010', 'Male: !! 10 to 14 years_2010',
'Male: !! 15 to 17 years_2010', 'Male: !! 18 and 19 years_2010',
'Male: !! 20 years_2010', 'Male: !! 21 years_2010',
'Male: !! 22 to 24 years_2010', 'Male: !! 25 to 29 years_2010',
'Male: !! 30 to 34 years_2010', 'Male: !! 35 to 39 years_2010',
'Male: !! 40 to 44 years_2010', 'Male: !! 45 to 49 years_2010',
'Male: !! 50 to 54 years_2010', 'Male: !! 55 to 59 years_2010',
'Male: !! 60 and 61 years_2010', 'Male: !! 62 to 64 years_2010',
'Male: !! 65 and 66 years_2010', 'Male: !! 67 to 69 years_2010',
'Male: !! 70 to 74 years_2010', 'Male: !! 75 to 79 years_2010',
'Male: !! 80 to 84 years_2010', 'Male: !! 85 years and over_2010',
'Female: !! 85 years and over_2010', 'Female: !! Under 5 years_2010',
'Female: !! 5 to 9 years_2010', 'Female: !! 10 to 14 years_2010',
'Female: !! 15 to 17 years_2010', 'Female: !! 18 and 19 years_2010',
'Female: !! 20 years_2010', 'Female: !! 21 years_2010',
'Female: !! 22 to 24 years_2010', 'Female: !! 25 to 29 years_2010',
'Female: !! 30 to 34 years_2010', 'Female: !! 35 to 39 years_2010',
'Female: !! 40 to 44 years_2010', 'Female: !! 45 to 49 years_2010',
'Female: !! 50 to 54 years_2010', 'Female: !! 55 to 59 years_2010',
'Female: !! 60 and 61 years_2010', 'Female: !! 62 to 64 years_2010',
'Female: !! 65 and 66 years_2010', 'Female: !! 67 to 69 years_2010',
'Female: !! 70 to 74 years_2010', 'Female: !! 75 to 79 years_2010',
'Female: !! 80 to 84 years_2010','Total']

nonNumericColList = ['state', 'county', 'state_fips', 'county_fips','FIPS', 'ZIP', 'RES_RATIO', 'BUS_RATIO', 'OTH_RATIO', 'TOT_RATIO']
 
#censusZipPaymentNoNan[collist] = censusZipPaymentNoNan[collist].apply(pd.to_numeric)
numericChunk = censusZipPaymentNoNan[collist].apply(lambda x: pd.to_numeric(x, errors='coerce'))
nonNumericChunk = censusZipPaymentNoNan[nonNumericColList]

#join the chuncks back to gether on their indexes
frames  = [nonNumericChunk,numericChunk]
numericCensusZipPaymentNoNan = pd.concat(frames, axis=1, join = 'inner')

#res_ratio is the ratio of how much of the country is in that particualr zip code
numericCensusZipPaymentNoNan[numericCensusZipPaymentNoNan['RES_RATIO'] != 1 ].head(5)

#CREATED ADDITIONAL COLUMN TO REPRESENT PAYMENT CONTRIBUTION FROM COUNTY CENSUS DEMOGRPAHICS TAKING INTO ACCOUNT CENSUS AND COUNTY  OVERLAP
numericCensusZipPaymentNoNan['adjTotal'] = numericCensusZipPaymentNoNan['Total'] * numericCensusZipPaymentNoNan['RES_RATIO']


#look at distribution of payment information per zip before and after adjustment for zip code county over lap
#it's clear the adjustment pushes the distribution left and minimizes the tail.
from scipy import stats, integrate
sns.set(color_codes=True)

totalByZIP = numericCensusZipPaymentNoNan.groupby('ZIP').Total.sum()
adjTotalByZIP = numericCensusZipPaymentNoNan.groupby('ZIP').adjTotal.sum()

print list(adjTotalByZIP.columns)
adjTotalByZIP.rename(columns={'','adjTotal'}, inplace=True)
adjTotalByZIP.head(5)

sns.set(rc={"figure.figsize": (12, 4)})
sns.distplot(numericCensusZipPaymentNoNan['adjTotal'], bins=200, kde=False, rug=False)


lidAdjTotalByZIP = adjTotalByZIP[ adjTotalByZIP < 250001 ]
#sns.distplot(lidAdjTotalByZIP, bins=200, kde=False, rug=False) #ont' bother plotting with largest bar near zero

#plot summed by ZIP codes data 
heelLidAdjTotalByZIP = lidAdjTotalByZIP[ lidAdjTotalByZIP > 100 ]
sns.distplot(heelLidAdjTotalByZIP, bins=200, kde=False, rug=False)


#sns.distplot(totalByZIP)
#sns.distplot(adjTotalByZIP)

correlationcheckcollist=['2-person household H13. Household Size [8]_2010',
'3-person household H13. Household Size [8]_2010',
'4-person household H13. Household Size [8]_2010',
'5-person household H13. Household Size [8]_2010',
'6-person household H13. Household Size [8]_2010',
'7-or-more-person household H13. Household Size [8]_2010',
'Total population_2010', 'White alone_2010',
'Black or African American alone_2010',
'American Indian and Alaska Native alone_2010', 'Asian alone_2010',
'Native Hawaiian and Other Pacific Islander alone_2010',
'Some Other Race alone_2010', 'Two or More Races_2010',
'Not Hispanic or Latino_2010', 'Hispanic or Latino_2010',
'Total Population_2010', 'Male:_2010', 'Male: !! Under 5 years_2010',
'Male: !! 5 to 9 years_2010', 'Male: !! 10 to 14 years_2010',
'Male: !! 15 to 17 years_2010', 'Male: !! 18 and 19 years_2010',
'Male: !! 20 years_2010', 'Male: !! 21 years_2010',
'Male: !! 22 to 24 years_2010', 'Male: !! 25 to 29 years_2010',
'Male: !! 30 to 34 years_2010', 'Male: !! 35 to 39 years_2010',
'Male: !! 40 to 44 years_2010', 'Male: !! 45 to 49 years_2010',
'Male: !! 50 to 54 years_2010', 'Male: !! 55 to 59 years_2010',
'Male: !! 60 and 61 years_2010', 'Male: !! 62 to 64 years_2010',
'Male: !! 65 and 66 years_2010', 'Male: !! 67 to 69 years_2010',
'Male: !! 70 to 74 years_2010', 'Male: !! 75 to 79 years_2010',
'Male: !! 80 to 84 years_2010', 'Male: !! 85 years and over_2010',
'Female: !! 85 years and over_2010', 'Female: !! Under 5 years_2010',
'Female: !! 5 to 9 years_2010', 'Female: !! 10 to 14 years_2010',
'Female: !! 15 to 17 years_2010', 'Female: !! 18 and 19 years_2010',
'Female: !! 20 years_2010', 'Female: !! 21 years_2010',
'Female: !! 22 to 24 years_2010', 'Female: !! 25 to 29 years_2010',
'Female: !! 30 to 34 years_2010', 'Female: !! 35 to 39 years_2010',
'Female: !! 40 to 44 years_2010', 'Female: !! 45 to 49 years_2010',
'Female: !! 50 to 54 years_2010', 'Female: !! 55 to 59 years_2010',
'Female: !! 60 and 61 years_2010', 'Female: !! 62 to 64 years_2010',
'Female: !! 65 and 66 years_2010', 'Female: !! 67 to 69 years_2010',
'Female: !! 70 to 74 years_2010', 'Female: !! 75 to 79 years_2010',
'Female: !! 80 to 84 years_2010','adjTotal']

smalllist = ['adjTotal', 'Total Population_2010']

pd.scatter_matrix(numericCensusZipPaymentNoNan[smalllist])

pd.scatter_matrix(numericCensusZipPaymentNoNan[correlationcheckcollist])

sns.set(style="white")

# Compute the correlation matrix
#corr = numericChunk[correlationcheckcollist].corr()

corr = numericCensusZipPaymentNoNan[correlationcheckcollist].corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)
#cmap = sns.cubehelix_palette(8, start=.5, rot=-.75, as_cmap=True)
# Draw the heatmap with the mask and correct aspect ratio
sns_plot = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3,
           square=True, xticklabels=5, yticklabels=5,#
          linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
fig = sns_plot.get_figure()
fig.savefig('/Users/Iain/DS-SEA-3/DS-SEA-3-Project-ILM/viz/correlationHeatMap.png')

         
#PLOT WITH DEFAULT COLOUR MAP (BLEUGH!)       
#sns.heatmap(corr, mask=mask, vmax=.3,
#            square=True, xticklabels=5, yticklabels=5,
#            linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)

#it seems like all the census data is not strongly correclated iwth the total payments by Zip code.
#let's test it.


#what is the rmse we'd expect by random quessing?
from sklearn import metrics
numericCensusZipPaymentNoNan['nullPrediction']=numericCensusZipPaymentNoNan.adjTotal.mean()
nullPredictionRMSE = np.sqrt(metrics.mean_squared_error(numericCensusZipPaymentNoNan.adjTotal, numericCensusZipPaymentNoNan.nullPrediction))
#print 'nullPredictionRMSE: ', nullPredictionRMSE


featurelist = ['Total Population_2010','White alone_2010',
'Black or African American alone_2010',
'American Indian and Alaska Native alone_2010', 'Asian alone_2010',
'Native Hawaiian and Other Pacific Islander alone_2010',
'Some Other Race alone_2010', 'Two or More Races_2010',
'Not Hispanic or Latino_2010', 'Hispanic or Latino_2010', 'Male:_2010']

rowsWithNulls = pd.isnull(numericCensusZipPaymentNoNan)

rowsWithNulls.head(5)

np.any(np.isnan(numericCensusZipPaymentNoNan[featurelist]))

np.all(np.isfinite(numericCensusZipPaymentNoNan[featurelist]))

from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import LinearRegression
y = numericCensusZipPaymentNoNan['adjTotal']
X = numericCensusZipPaymentNoNan[featurelist]


linreg = LinearRegression()
msescores = cross_val_score(linreg,X,y,cv=10,scoring='mean_squared_error')
rmsescores = np.mean(np.sqrt(-msescores))

print 'linreg rmsescores: ', rmsescores
print 'nullPredictionRMSE: ', nullPredictionRMSE
