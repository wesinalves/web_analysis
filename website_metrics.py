'''
Script to collect website metrics
'''
import json
import requests
import pandas as pd
import urllib
import time
#from google.colab import files
import io

# Define URL
# url = 'https://www.iec.gov.br'

# # API request url
# result = urllib.request.urlopen('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}/&strategy=mobile'\
# .format(url)).read().decode('UTF-8')

# # Convert to json format
# result_json = json.loads(result)

# with open('result.json', 'w') as outfile:
#   json.dump(result_json, outfile)

column_header = 'url'
df = pd.read_csv('sites.csv')

response_object = {}

print('loading websites')
# Iterate through the df
for x in range(0, len(df)):

    # Define request parameter
    url = df.iloc[x][column_header]
    print(f'processing url: {url}')

    # Make request
    pagespeed_results = urllib.request.urlopen('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={}&strategy=mobile&key=AIzaSyBF1tbpB0rsMnOVDxdlhjZ5Dch67wFy89E'.format(url)).read().decode('UTF-8')

    # Convert to json format
    pagespeed_results_json = json.loads(pagespeed_results)

    # Insert returned json response into response_object
    response_object[url] = pagespeed_results_json
    time.sleep(10)



# Create dataframe to store responses
df_pagespeed_results = pd.DataFrame(columns=
          ['url',
          'Overall_Category',
          'Largest_Contentful_Paint',
          'First_Input_Delay',
          'Cumulative_Layout_Shift',
          'First_Contentful_Paint',
          'Time_to_Interactive',
          'Total_Blocking_Time',
          'Speed_Index'])

print('retriving metrics from json')
for (url, x) in zip(response_object.keys(), range(0, len(response_object))):

        # URLs
        df_pagespeed_results.loc[x, 'url'] =\
            response_object[url]['lighthouseResult']['finalUrl']

        # Overall Category
        df_pagespeed_results.loc[x, 'Overall_Category'] =\
            response_object[url]['loadingExperience']['overall_category']

        # Core Web Vitals

        # Largest Contentful Paint
        df_pagespeed_results.loc[x, 'Largest_Contentful_Paint'] =\
        response_object[url]['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']

        # First Input Delay
        fid = response_object[url]['loadingExperience']['metrics']['FIRST_INPUT_DELAY_MS']
        df_pagespeed_results.loc[x, 'First_Input_Delay'] = fid['percentile']

        # Cumulative Layout Shift
        df_pagespeed_results.loc[x, 'Cumulative_Layout_Shift'] =\
        response_object[url]['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']

        # Additional Loading Metrics

        # First Contentful Paint
        df_pagespeed_results.loc[x, 'First_Contentful_Paint'] =\
        response_object[url]['lighthouseResult']['audits']['first-contentful-paint']['displayValue']

        # Additional Interactivity Metrics

        # Time to Interactive
        df_pagespeed_results.loc[x, 'Time_to_Interactive'] =\
        response_object[url]['lighthouseResult']['audits']['interactive']['displayValue']

        # Total Blocking Time
        df_pagespeed_results.loc[x, 'Total_Blocking_Time'] =\
        response_object[url]['lighthouseResult']['audits']['total-blocking-time']['displayValue']

        # Speed Index
        df_pagespeed_results.loc[x, 'Speed_Index'] =\
        response_object[url]['lighthouseResult']['audits']['speed-index']['displayValue']

print('results save to file')
df_pagespeed_results.to_csv('pagespeed_results.csv')
