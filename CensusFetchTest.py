# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 17:36:11 2016

@author: Iain
"""

import pandas as pd
import requests

year = '2010'
census_api_key = '6840b3dd45356442d47f59230b9ac7434ec21a87'

r = requests.get('http://api.census.gov/data/2010/sf1?key=6840b3dd45356442d47f59230b9ac7434ec21a87&get=H0130002&for=state:01')


r.text
