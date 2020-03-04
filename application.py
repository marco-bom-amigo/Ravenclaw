############################
## Importing dependencies ##
############################
from __future__ import print_function
import pickle
import re
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from apiclient.http import MediaFileUpload
import mimetypes
import base64
import pandas as pd
import numpy as np
from datetime import date, datetime
import decimal
from flask import Flask, request, jsonify
import pytz
############################

##################################
## Set Decimal as ROUND_HALF_UP ##
##################################
context          = decimal.getcontext()
context.rounding = decimal.ROUND_HALF_UP

source_date = datetime.datetime.now()
source_time_zone = pytz.timezone('US/Eastern')
source_date_with_timezone = source_time_zone.localize(source_date)
target_time_zone = pytz.timezone('US/Eastern')
target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
today            = target_date_with_timezone.today()
##################################

##########################################
## Connecting to the google spreadsheet ##
##########################################
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly'
         ,'https://mail.google.com/'
         ,'https://www.googleapis.com/auth/drive']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
sheet   = build('sheets', 'v4', credentials = creds).spreadsheets()
gdrive  = build('drive', 'v3', credentials = creds)
service = build('gmail', 'v1', credentials = creds)
##########################################

##########################
## Function: Read sheet ##
##########################
def read_sheet(SPREADSHEET_ID, RANGE, COLUMN_INDEXES, COLUMN_NAMES):

    # Get the spreadsheet values
    values = sheet.values().get( spreadsheetId = SPREADSHEET_ID
                               , range         = RANGE
                               ).execute().get('values', [])
    
    # Converts to DataFrame
    values = pd.DataFrame(values)[COLUMN_INDEXES]
    
    # Rename the columns
    values.columns = COLUMN_NAMES
    
    return values
##########################

#####################################
## Read: Bases PMO > hotel_details ##
#####################################
## • MRC                           ##
#####################################
Bases_PMO = read_sheet( SPREADSHEET_ID = '1DON-emTbfEUnvlO1RpPzUKz5IhSD_swRAKX65OcPBCA'
                      , RANGE          = 'hotel_details!A2:R5000'
                      , COLUMN_INDEXES = [0, 3, 17]
                      , COLUMN_NAMES   = ['CRS ID', 'hub_name', 'MRC']
                      )
#####################################

######################################
## Read: Go-live tracker > Live Log ##
######################################
## • Planned live date              ##
######################################
Live_Log = read_sheet( SPREADSHEET_ID = '1few_jNvQ6DnsDXHBmypPoi3tds13_nrFLnUnjaqslm8'
                     , RANGE          = 'Live Log!B2:X5000'
                     , COLUMN_INDEXES = [0, 12, 22]
                     , COLUMN_NAMES   = ['CRS ID', 'Planned live date', 'CRS Status']
                     )
######################################

######################################################
## Read: All_new_clustered_RBP > [output]base_price ##
######################################################
## • Price ranges                                   ##
######################################################
base_price = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                       , RANGE          = '[output]base_price!S2:T14'
                       , COLUMN_INDEXES = [0, 1]
                       , COLUMN_NAMES   = ['0', '1']
                       )
# Subset rows
base_price = base_price.iloc[[0, 1, 2, 3, 4, 5, 9, 10, 11, 12], :]

# Converts "base price" to Decimal
base_price['1'] = base_price['1'].str.replace('x', '').apply(lambda x: float(decimal.Decimal(x)))
######################################################

################################################
## Read: All_new_clustered_RBP > [aux]weekday ##
################################################
## • Weekday                                  ##
################################################
UFs = ['SP', 'RJ', 'ES', 'MG', 'RS', 'SC', 'PR', 'MS', 'MT', 'DF', 'GO', 'TO', 'BA', 'SE', 'AL', 'CE', 'RN', 'PE', 'PB', 'MA', 'PI', 'AM', 'PA', 'AC', 'AP', 'RO', 'RR']

# Regular
weekday_regular = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                            , RANGE          = '[aux]weekday!C5:ACS11'
                            , COLUMN_INDEXES = list(range(27))
                            , COLUMN_NAMES   = UFs
                            )
weekday_regular.index = list(range(1, 8))

# Beach
weekday_beach   = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                            , RANGE          = '[aux]weekday!C15:ACS21'
                            , COLUMN_INDEXES = list(range(23))
                            , COLUMN_NAMES   = UFs[0:23]
                            )
weekday_beach.index = list(range(1, 8))

# Another
weekday_another = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                            , RANGE          = '[aux]weekday!C25:ACS31'
                            , COLUMN_INDEXES = list(range(27))
                            , COLUMN_NAMES   = UFs
                            )
weekday_another.index = list(range(1, 8))

# Converts to Float
weekday_regular = weekday_regular.replace('x', '', regex = True).astype(float)
weekday_beach[weekday_beach == ''] = 0
weekday_beach   = weekday_beach.replace('x', '', regex = True).astype(float)
weekday_another = weekday_another.replace('x', '', regex = True).astype(float)

del UFs
################################################

##############################################
## Read: All_new_clustered_RBP > [aux]month ##
##############################################
## • Month                                  ##
##############################################
UFs = ['SP', 'RJ', 'ES', 'MG', 'RS', 'SC', 'PR', 'MS', 'MT', 'DF', 'GO', 'TO', 'BA', 'SE', 'AL', 'CE', 'RN', 'PE', 'PB', 'MA', 'PI', 'AM', 'PA', 'AC', 'AP', 'RO', 'RR']

# Regular
month_regular = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                          , RANGE          = '[aux]month!C5:AC16'
                          , COLUMN_INDEXES = list(range(27))
                          , COLUMN_NAMES   = UFs
                          )
month_regular.index = list(range(1, 13))

# Beach
month_beach   = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                          , RANGE          = '[aux]month!C20:AC31'
                          , COLUMN_INDEXES = list(range(25))
                          , COLUMN_NAMES   = UFs[0:25]
                          )
month_beach.index = list(range(1, 13))

# Another
month_another = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                          , RANGE          = '[aux]month!C35:AC46'
                          , COLUMN_INDEXES = list(range(27))
                          , COLUMN_NAMES   = UFs
                          )
month_another.index = list(range(1, 13))

# Converts to Floar
month_regular = month_regular.replace('x', '', regex = True).astype(float)
month_beach[month_beach == ''] = 0
month_beach   = month_beach.replace('x', '', regex = True).astype(float)
month_another = month_another.replace('x', '', regex = True).astype(float)

del UFs
##############################################

##################################################################
## Read: All_new_clustered_RBP > [ACTION_REQUIRED] import_range ##
##################################################################
## • Type of tourism                                            ##
##################################################################
type_of_tourism = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                            , RANGE          = '[ACTION_REQUIRED] import_range!AC2:AG5000'
                            , COLUMN_INDEXES = list(range(5))
                            , COLUMN_NAMES   = ['City', 'State', 'UF', 'HUBs', 'Type of tourism']
                            )
##################################################################

###################################################
## Read: All_new_clustered_RBP > [aux]peak_dates ##
###################################################
## • Peak dates                                  ##
###################################################
peak_dates = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                       , RANGE          = '[aux]peak_dates!C7:F5000'
                       , COLUMN_INDEXES = list(range(4))
                       , COLUMN_NAMES   = ['Date', 'Event', 'Importance', 'Factor']
                       )

# Converts "Date" to DateTime
peak_dates['Date'] = pd.to_datetime(peak_dates['Date'])

# Converts "Factor" to Float
peak_dates['Factor'] = peak_dates['Factor'].astype(float)
###################################################

################################################
## Read: Go-live tracker > Properties Tracker ##
################################################
## • City & UF                                ##
################################################
Properties_Tracker = read_sheet( SPREADSHEET_ID = '1few_jNvQ6DnsDXHBmypPoi3tds13_nrFLnUnjaqslm8'
                               , RANGE          = 'Properties Tracker!D4:J5000'
                               , COLUMN_INDEXES = [0, 5, 6]
                               , COLUMN_NAMES   = ['CRS ID', 'UF', 'City']
                               )
################################################

##########################################################
## Read: All_new_clustered_RBP > [output]pricing_matrix ##
##########################################################
## • Pricing matrix                                     ##
##########################################################
pricing_matrix = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                           , RANGE          = '[output]pricing_matrix!C2:C5'
                           , COLUMN_INDEXES = [0]
                           , COLUMN_NAMES   = ['0']
                           )

# Transpose the DataFrame
pricing_matrix = pricing_matrix.T

# Rename the columns
pricing_matrix.columns = ['Top 30 days', 'Top D-DAY', 'Bottom 30 Days', 'Bottom D-DAY']

# Converts all columns to Float
pricing_matrix = pricing_matrix.astype(float)
##########################################################

#######################################################
## Read: All_new_clustered_RBP > [output]floor_price ##
#######################################################
## • Floor price by importance                       ##
#######################################################
floor_price = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                        , RANGE          = '[output]floor_price!O2:U9'
                        , COLUMN_INDEXES = list(range(7))
                        , COLUMN_NAMES   = list(range(7))
                        )

# Use the first row as columns names
floor_price.columns = floor_price.iloc[0,:]

# Remove the first row
floor_price = floor_price.iloc[1:7,:]

# Remove the "Factor" "x" character
floor_price['Factor'] = floor_price['Factor'].str.replace('x', '')

# Replace the empty values to "0"
floor_price['Factor'][floor_price['Factor'] == ''] = 0

# Converts "Factor" to Float
floor_price['Factor'] = floor_price['Factor'].astype(float)

# Converts "Importance" to Int
floor_price['Importance'] = floor_price['Importance'].astype(int)

## Remove the "R$" characters and converts to Float
floor_price['1'] = floor_price['1'].str.replace("R[$]", '').astype(float)
floor_price['2'] = floor_price['2'].str.replace('R[$]', '').astype(float)
floor_price['3'] = floor_price['3'].str.replace('R[$]', '').astype(float)
floor_price['4'] = floor_price['4'].str.replace('R[$]', '').astype(float)
floor_price['5'] = floor_price['5'].str.replace('R[$]', '').astype(float)
#######################################################

#######################################################
## Read: All_new_clustered_RBP > [output]floor_price ##
#######################################################
## • Floor factor                                    ##
#######################################################
floor_factor = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                         , RANGE          = '[output]floor_price!P11'
                         , COLUMN_INDEXES = [0]
                         , COLUMN_NAMES   = ['Floor Factor']
                         )

# Converts "Floor Factor" to Float
floor_factor['Floor Factor'] = floor_factor['Floor Factor'].astype(float)
#######################################################

##############################
## Clusters > Clusters BRA  ##
##############################
## • Clusters by UF & City  ##
##############################
clusters = read_sheet( SPREADSHEET_ID = '12E00hjlTlBllMP8q4qlq3Xkjc_mjmgIaEpDatam20b4'
                     , RANGE          = 'Clusters BRA!A2:I5000'
                     , COLUMN_INDEXES = list(range(9))
                     , COLUMN_NAMES   = ['City', 'State', 'UF', 'Seasonal/Touristic', '# inhabitants > 500k', 'Access', 'Group 1', 'Group 2', 'Cluster']
                     )
#############################
    
#################################################
## Read: All_new_clustered_RBP > Clusterização ##
#################################################
## • Clusters multipliers, Base & Floor        ##
#################################################

# Base
cluster_multiplier = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                               , RANGE          = 'Clusterização!L4:O7'
                               , COLUMN_INDEXES = [0,1,2,3]
                               , COLUMN_NAMES   = ['Cluster', 'High', 'Mid', 'Low']
                               )
cluster_multiplier = cluster_multiplier.dropna()
cluster_multiplier[['High', 'Mid', 'Low']] = cluster_multiplier[['High', 'Mid', 'Low']].astype(float)

# Floor
cluster_floor = read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                          , RANGE          = 'Clusterização!L13:M16'
                          , COLUMN_INDEXES = [0,1]
                          , COLUMN_NAMES   = ['Cluster', 'Factor']
                          )
cluster_floor['Factor'] = cluster_floor['Factor'].astype(float)
#################################################

#####################################################
## Subset: Live log                                ##
#####################################################
## • Remove Signed, Churn, Sem visibilidade & LIVE ##
#####################################################
Live_Log = Live_Log[Live_Log['CRS ID'] != 'Signed']
Live_Log = Live_Log[~Live_Log['Planned live date'].isin(['Churn', 'Sem Visibilidade', 'LIVE'])]
Live_Log = Live_Log[Live_Log['Planned live date'] != '']
#####################################################

##########################
## Fuction: Punctuation ##
##########################
## • Remove punctuation ##
##########################
def punctuation(var):
    
    if type(var) == str:
        var = pd.Series(var)
    
    var = var.apply(lambda x: re.sub('[ÁÂÀÃ]', 'A', x.upper()))
    var = var.apply(lambda x: re.sub('[ÉÊ]'  , 'E', x.upper()))
    var = var.apply(lambda x: re.sub('[Í]'   , 'I', x.upper()))
    var = var.apply(lambda x: re.sub('[ÓOO]' , 'O', x.upper()))
    var = var.apply(lambda x: re.sub('[ÚÜ]'  , 'U', x.upper()))
    var = var.apply(lambda x: re.sub('[Ç]'   , 'C', x.upper()))
    var = var.apply(lambda x: re.sub('[Ñ]'   , 'N', x.upper()))
    return var
##########################

################################################################################
## Merge: Lve log, Properties Tracker, Bases PMO , Clusters & Type of tourism ##
################################################################################
    
# Merge: Live Log & Properties Tracker
df = Live_Log.merge(Properties_Tracker)

# ... & Bases PMO
df = df.merge(Bases_PMO)

# Converts "City" to Str
df['City'] = df['City'].astype(str)

# Creats a City column to be modified
clusters['CityMod'] = clusters['City'].copy()

# Removes the Cluster City punctuation
clusters['CityMod'] = punctuation(clusters['CityMod'])

# Saves the original city name
cities = df['City'].copy()

# Removes the Properties Tracker City punctuaton
df['City'] = punctuation(df['City'])

# Merge the Clusters...
df = df.merge( clusters
             , left_on  = ['UF', 'City']
             , right_on = ['UF', 'CityMod']
             , how      = 'left'
             )

# Set the Cities not defined
df['City_y'][df['City_y'].isna()] = cities[df['City_y'].isna()]

# Drop the useless columns
df = df.drop('City_x', axis = 1)
df = df.drop('CityMod', axis = 1)

# Renames the correct City column name
df = df.rename(columns = {'City_y':'City'})

# Fill the empties wuth a space
df = df.fillna('')

# Creates the Planned live date description column
df['Planned live date desc'] = df['Planned live date']

# Converts "Planned live date" to Str
df['Planned live date'] = df['Planned live date'].astype(str)

# Converts "Planned live date" to DateTime
df['Planned live date'] = pd.to_datetime(df['Planned live date'], errors = 'coerce')

# Subset
df = df[df['Planned live date'] >= pd.to_datetime(today)]

# Sort by "Planned live date"
df = df.sort_values('Planned live date')

# Set the non-defined cities as "Regular Low Demand"
df['Cluster'][df['Cluster'] == ''] = 'Regular Low Demand'

df = df.merge(type_of_tourism[['City', 'UF', 'Type of tourism']], left_on = ['UF', 'City'], right_on = ['UF', 'City'], how = 'left')
df['Type of tourism'] = df['Type of tourism'].fillna('Regular')

del Live_Log, Properties_Tracker, Bases_PMO, clusters, cities, type_of_tourism
##############################################################

####################
## Validation...! ##
####################
# c = df['CRS ID'].value_counts()
###################

#########################################################
## Function: Root base                                 ##
#########################################################
## • Creates the basic data frame, used for all others ##
#########################################################
def root_base(dt, estado, type_of_tourism):
    
    # Creates the DataFrane with 365 days
    df_base = pd.DataFrame( pd.date_range( start   = dt
                                         , periods = 365
                                         )
                          , columns = ['date']
                          )

    # Creates the Month column
    df_base['month'] = df_base['date'].dt.month
    
    # Creates the dayofweek column
    df_base['dayofweek'] = df_base['date'].dt.dayofweek + 2
    df_base['dayofweek'][df_base['dayofweek'] == 8] = 1

    # Merge: df_base & month
    if type_of_tourism == 'Regular':
        df_base = df_base.merge(month_regular[estado], left_on='month', right_index=True);
    else:
        if type_of_tourism ==  'Beach':
                df_base = df_base.merge(month_beach[estado], left_on='month', right_index=True);
        else:
                df_base = df_base.merge(month_another[estado], left_on='month', right_index=True);
    df_base = df_base.rename(columns = {estado:'Month Factor'})
    
    # Merge: df_base & weekday
    if type_of_tourism == 'Regular':
        df_base = df_base.merge(weekday_regular[estado], left_on = 'dayofweek', right_index=True);
    else:
        if type_of_tourism ==  'Beach':
                df_base = df_base.merge(weekday_beach[estado], left_on = 'dayofweek', right_index=True);
        else:
                df_base = df_base.merge(weekday_another[estado], left_on = 'dayofweek', right_index=True);
    df_base = df_base.rename(columns = {estado:'Weekday Factor'})

    # Merge: df_base & peak dates
    df_base = df_base.merge(peak_dates[['Date', 'Factor']], left_on = 'date', right_on = 'Date', how = 'left')
    df_base = df_base.drop('Date', axis = 1)
    df_base = df_base.rename(columns = {'Factor':'Peak Factor'})
    df_base['Peak Factor'][df_base['Peak Factor'].isna()] = 1

    # Creates the Stagger column
    df_base['Stagger'] = 1
    df_base = df_base.sort_values('date')
    df_base = df_base.reset_index().drop('index', axis = 1)
    aux = list(df_base['Stagger'])[:-1]
    aux.insert(0, 0)
    before = 1
    for i, n in enumerate(aux):
        
        if (df_base.iloc[i, 0] - pd.to_datetime(today)).days < base_price['1'][10]:
            df_base.iloc[i, 6] = 1
        else:
            before = before * (1 + base_price['1'][12])
            if before > base_price['1'][11]:
                before = base_price['1'][11]
            df_base.iloc[i, 6] = before

    df_base['Stagger'] = df_base['Stagger'].astype(float)

    # Creates the Factor column
    df_base['Factor'] = df_base['Month Factor'] * df_base['Weekday Factor'] * df_base['Peak Factor'] * df_base['Stagger']
    df_base['Factor'][df_base['Factor'] > base_price['1'][9]] = base_price['1'][9]
    df_base['Factor'] = df_base['Factor'].astype(float)

    return df_base    
#########################################################

#####################################
## Function: Get price             ##
#####################################
## • Set price on Cluster and Nota ##
#####################################
def getPrice(cluster, nota, pre_price, plan = 'Base'):
        
    if plan == 'Base':
        
        # Get Cluster multiplier
        aux = cluster_multiplier[cluster_multiplier['Cluster'].str.lower() == cluster.lower()][['High', 'Mid', 'Low']].reset_index()
        price = aux['Mid'][0] * pre_price
        
        # Get multiplier on Nota
        if nota < 6.5:
            price = aux['Low'][0] * pre_price
        if nota > 8:
            price = aux['High'][0] * pre_price

    else:
       price = pre_price * cluster_floor[cluster_floor['Cluster'].str.lower() == cluster.lower()]['Factor'].values[0]

    return price
#####################################
    
##############################
## Function: Base           ##
##############################
## • Creates the Base sheet ##
##############################
def base(df_base, oyo_id, nota, price, cluster):

    price = getPrice(cluster, nota, price)
    
    columns = ['price_1', 'price_2', 'price_3', 'price_4', 'price_5']
    for i, price_column in enumerate(columns):

        # Creates the "price" columns
        df_base[price_column] = ((price * base_price['1'][i + 1]) * df_base['Factor']) / base_price['1'][0]
        
        # Rounds the value and converts to Int
        df_base[price_column] = df_base[price_column].apply(lambda x: round(decimal.Decimal(x), 0)).astype(int)
        
    # Creates the "df_out_base" DataFrame
    df_out_base = df_base[['price_1', 'price_2', 'price_3', 'price_4','price_5']]

    # Creates the "oyo_id" column
    df_out_base['oyo_id'] = oyo_id

    # Formats the dates
    df_out_base['date']     = df_base['date'].dt.strftime('%d/%m/%Y')
    df_out_base['end_date'] = df_base['date'].dt.strftime('%d/%m/%Y')
    
    # Order by "date"
    df_out_base['order'] = df_base['date']
    df_out_base          = df_out_base.sort_values('order')
    
    # Subset the columns
    df_out_base = df_out_base[['oyo_id', 'date', 'end_date', 'price_1', 'price_2', 'price_3', 'price_4', 'price_5']]
    
    return df_out_base
##############################

#################################
## Function: Ceiling           ##
#################################
## • Creates the Ceiling sheet ##
#################################
def ceiling(df_base, oyo_id, price):

    columns = ['ceiling_so', 'ceiling_do', 'ceiling_to', 'ceiling_4', 'ceiling_5']
    for i, price_column in enumerate(columns):

        # Creates the "ceiling_so" column
        df_base[price_column] = price * base_price['1'][i + 1] * df_base['Factor'] * pricing_matrix['Top 30 days'][0]

        # Rounds the value and converts to Int
        df_base[price_column] = df_base[price_column].apply(lambda x: round(decimal.Decimal(x), 0)).astype(int)

    # Subsets the columns
    df_out_ceiling = df_base[['ceiling_so', 'ceiling_do', 'ceiling_to', 'ceiling_4', 'ceiling_5']]

    # Creates the "oyo_id" column
    df_out_ceiling['oyo_id'] = oyo_id
    
    # Formats the dates
    df_out_ceiling['start_date'] = df_base['date'].dt.strftime('%d/%m/%Y')
    df_out_ceiling['end_date']   = df_base['date'].dt.strftime('%d/%m/%Y')

    # Order by "date"
    df_out_ceiling['order'] = df_base['date']
    df_out_ceiling          = df_out_ceiling.sort_values('order')

    # Subset the columns
    df_out_ceiling = df_out_ceiling[['oyo_id', 'start_date', 'end_date', 'ceiling_so', 'ceiling_do', 'ceiling_to', 'ceiling_4', 'ceiling_5']]
    
    return df_out_ceiling
#################################

###############################
## Function: Floor           ##
###############################
## • Creates the Floor sheet ##
###############################
def floor(df_base, oyo_id, nota, cluster):

   # Creates the "Peak Date Factor" column
   df_base['Peak Date Factor'] = 6
   df_base['Peak Date Factor'][df_base['Peak Factor'] == 2]  = 0

   # Merge: df_base & floor_price
   df_base = df_base.merge( floor_price[['Importance', '1', '2', '3', '4', '5']]
                          , left_on  = 'Peak Date Factor'
                          , right_on = 'Importance'
                          , how      = 'left'
                          )
   
   # Creates the "df_out_floor" DataFrame
   df_out_floor = df_base.copy()

   for i in range(1, 6):
       c1 = i

       df_out_floor[str(c1)] = np.where( getPrice(cluster, nota, df_base['price_' + str(c1)], 'Floor') <= df_base[str(c1)]
                                       , getPrice(cluster, nota, df_base['price_' + str(c1)], 'Floor')
                                       , df_base[str(c1)]
                                       ) / floor_factor['Floor Factor'][0]

       # Rounds the value and converts to Int
       df_out_floor[str(c1)] = df_out_floor[str(c1)].apply(lambda x: round(decimal.Decimal(x), 0)).astype(int)

   # Creates the "oyo_id" column
   df_out_floor['oyo_id'] = oyo_id
   
   # Creates the "reason" column
   df_out_floor['reason'] = 'rule_based_brazil'
   
   # Creates the "room_category_id" column
   df_out_floor['room_category_id'] = 1
   
   # Creates the "category" column
   df_out_floor['category'] = 'smart_bulk'

   # Sort by "date"
   df_out_floor = df_out_floor.sort_values('date')
    
   # Subset the columns
   df_out_floor = df_out_floor[['oyo_id', 'category', 'date', 'date', '1', '2', '3', '4', '5', 'reason', 'room_category_id']]

   # Rename the columns
   df_out_floor.columns = ['oyo_id', 'category', 'start_date', 'end_date', '1', '2', '3', '4', '5', 'reason', 'room_category_id']

   # Formats the dates
   df_out_floor['start_date'] = df_out_floor['start_date'].dt.strftime('%d/%m/%Y')
   df_out_floor['end_date']   = df_out_floor['end_date'].dt.strftime('%d/%m/%Y')
   
   return df_out_floor
###############################

##############################
## Function: create message ##
##############################
## • Creates the e-mail     ##
##############################
def create_message(sender, to, subject, message_text, files):
    
  # Creates the e-mail body
  message = MIMEMultipart()
  message['to'] = ", ".join(['vinicius.alves@oyorooms.com', 'ana.passos@oyorooms.com'])
  #message['to'] = ", ".join(['marcoantonio.bonamichi@oyorooms.com', 'marco.bom.amigo@gmail.com'])
  
  message['from'] = sender
  message['subject'] = subject
  msg = MIMEText(message_text)
  message.attach(msg)

  for file in files:

      # Get the file path
      file = 'files/' + file
      
      # Get the file type
      content_type, encoding = mimetypes.guess_type(file)
      #main_type, sub_type = str(content_type).split('/', 1)

      # Open the file      
      fp = open(file, 'rb')
      msg = MIMEBase(None, None)
      msg.set_payload(fp.read())
      fp.close()
    
      # Attach the file
      filename = os.path.basename(file)
      msg.add_header('Content-Disposition', 'attachment', filename = filename)
      message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
##############################

############################
## Function: Send message ##
############################
## • Sends the e-mail     ##
############################
def send_message(service, user_id, message):
    message = (service.users().messages().send(userId = user_id, body = message).execute())
    return message
############################

#######################################
## Function: Submit file             ##
#######################################
## • Sends the files to Google Drive ##
#######################################
def submit_file(files, hub):

    # Folder to send the files    
    folder_id = '1ZXcZ7WSTdS8R2XHVACutibn5zWtGJnz5'

    folders = gdrive.files().list( q        = "mimeType='application/vnd.google-apps.folder' and parents in '"+folder_id+"' and trashed = false"
                                 , fields   = "nextPageToken, files(id, name)"
                                 , pageSize = 400).execute()
    folders = pd.DataFrame(folders['files'])
    
    folder_id   = folders['id'][folders['name'].str.lower().str.startswith(punctuation(hub).str.lower().str.replace(' ', '_').values[0])]
    folder_name = folders['name'][folders['name'].str.lower().str.startswith(punctuation(hub).str.lower().str.replace(' ', '_').values[0])]
    
    if len(folder_id) ==  0:
        folder_id   = '1ZXcZ7WSTdS8R2XHVACutibn5zWtGJnz5'
        folder_name = 'Automatic'
    else:
        folder_id = folder_id.values[0]
    
    for f in files:
        file_metadata = { 'name': f
                        , 'parents': [folder_id]
                        }
        media = MediaFileUpload( 'files/' + f
                               , mimetype  = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                               , resumable = True
                               )
        gdrive.files().create( body       = file_metadata
                             , media_body = media
                             , fields     = 'id').execute()
    
    return folder_name
#######################################

###############
## Front-End ##
###############
app = Flask(__name__)

@app.route("/base/")
def p_base():
    
    args = request.args

    oyo_id = str(args.get('id'))
    price  = float(args.getlist('preco')[0])
    nota   = float(args.getlist('nota')[0])

    df_plan = df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][df['CRS ID'] == oyo_id]

    dt              = df_plan['Planned live date'].values[0]
    estado          = df_plan['UF'].values[0]
    type_of_tourism = df_plan['Type of tourism'].values[0]
    cluster         = df_plan['Cluster'].values[0]
    
    df_base        = root_base(dt, estado, type_of_tourism)
    df_out_base    = base(df_base, oyo_id, nota, price, cluster)

    return jsonify(df_out_base.to_dict())

@app.route("/ceiling/")
def p_ceiling():
    args = request.args

    oyo_id = str(args.get('id'))
    price  = float(args.getlist('preco')[0])

    df_plan = df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][df['CRS ID'] == oyo_id]
    dt              = df_plan['Planned live date'].values[0]
    estado          = df_plan['UF'].values[0]
    type_of_tourism = df_plan['Type of tourism'].values[0]
    
    df_base        = root_base(dt, estado, type_of_tourism)
    df_out_ceiling = ceiling(df_base, oyo_id, price)

    return jsonify(df_out_ceiling.to_dict())
    
@app.route("/floor/")
def p_floor():
    args = request.args

    oyo_id = str(args.get('id'))
    price  = float(args.getlist('preco')[0])
    nota   = float(args.getlist('nota')[0])

    df_plan = df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][df['CRS ID'] == oyo_id]
    dt              = df_plan['Planned live date'].values[0]
    estado          = df_plan['UF'].values[0]
    type_of_tourism = df_plan['Type of tourism'].values[0]
    cluster         = df_plan['Cluster'].values[0]

    df_base        = root_base(dt, estado, type_of_tourism)
    df_out_base    = base(df_base, oyo_id, nota, price, cluster)
    df_out_floor   = floor(df_base, oyo_id, nota, cluster)

    return jsonify(df_out_floor.to_dict())

@app.route('/', methods=['GET', 'POST'])
def form():

    if request.method == 'POST':

        args   = request.form
        crs_id = args.getlist('crs_id')
        preco  = args.getlist('preco')
        nota   = args.getlist('nota')
        
        df_plan = pd.DataFrame(list(zip(crs_id, preco)), columns = ['CRS ID', 'Preço'])
        df_plan['nota'] = nota
        df_plan = df_plan[df_plan['Preço'] != '']
        df_plan['Preço'] = df_plan['Preço'].astype(int)
        df_plan['nota'] = df_plan['nota'].astype(float)

        df_plan = df_plan.merge(df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster', 'hub_name']])

        hubs = []

        for i in range(len(df_plan)):
            oyo_id          = df_plan['CRS ID'][i]
            price           = df_plan['Preço'][i]
            dt              = df_plan['Planned live date'][i]
            estado          = df_plan['UF'][i]
            type_of_tourism = df_plan['Type of tourism'][i]
            nota            = df_plan['nota'][i]
            cluster         = df_plan['Cluster'][i]
            hub_name        = df_plan['hub_name']

            df_base        = root_base(dt, estado, type_of_tourism)
            df_out_base    = base(df_base, oyo_id, nota, price, cluster)
            df_out_ceiling = ceiling(df_base, oyo_id, price)
            df_out_floor   = floor(df_base, oyo_id, nota, cluster)

            df_out_base.to_excel('files/Base_' + oyo_id + '.xlsx', index = False)
            df_out_ceiling.to_excel('files/Ceiling_' + oyo_id + '.xlsx', index = False)
            df_out_floor.to_excel('files/Floor_' + oyo_id + '.xlsx', index = False)
       
            f = [ 'Base_' + oyo_id + '.xlsx'
                , 'Ceiling_' + oyo_id + '.xlsx'
                , 'Floor_' + oyo_id + '.xlsx'
                ]

            hubs.append(submit_file(f, hub_name))

            msg = create_message( sender       = 'me'
                                , to           = 'marcoantonio.bonaichi@oyorooms.com'
                                , subject      = 'GO LIVE - ' + oyo_id + ' - pricing update'
                                , message_text = "Hello team,\nplease update base, floor and ceiling prices according to attached files.\nBest regards."
                                , files        = f
                                )
            send_message(service, "me", msg)

        html = '''
                  <h1 style="font-family:arial">Propriedades enviadas:</h1>
                  <table style="font-family:arial;border:none" border=0>
               '''

        df_plan['folder'] = hubs
        
        html += '''<tr>
                     <th>CRS ID</th>
                     <th>Data de envio</th>
                     <th>Google Drive</th>
                   </tr>'''
        
        for i in range(len(df_plan)):
            
            html += '<tr><td style="width:150px">• <b>' +df_plan.iloc[i,0] + '</b></td><td  style="width:200px">'+ datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '</td><td>' + df_plan.iloc[i,7] + '</td></tr>' 

        html += '</table>'            
        return html

    else:
      html = '''<style>
                    
                    table {border-collapse: collapse;}
                    td, th {border: 1px solid black}
                    td {padding: 10px; height:55px}
                    .button, .bt-okay, .bt-not-okay {
                      color: white;
                      text-align: center;
                      text-decoration: none;
                      font-size: 16px;
                      margin: 0px;
                    }
                    .button {
                      padding: 15px 32px;
                      background-color: #4CAF50;
                    }
                    .bt-okay, .bt-not-okay {
                      padding: 5px 16px;
                      font-weight: bold;
                      font-size: 20px;
                    }
                    .bt-okay {background-color: #4CAF50;}
                    .bt-not-okay {background-color: #AF4C50;}
                    .mrc-ok, .crs-status-ok {background-color: #DDFFDD;}
                    .mrc-not-ok, .crs-status-not-ok {background-color: #FFDDDD;}
                   .Seasonal-High-Demand, .Regular-High-Demand, .Seasonal-Low-Demand, .Regular-Low-Demand {
                      font-weight: bold;
                      font-size: 18px;
                   }
                   .Seasonal-High-Demand {background-color: #cc4125;}
                   .Regular-High-Demand {background-color: #ea9999;}
                   .Seasonal-Low-Demand {background-color: #6aa84f;}
                   .Regular-Low-Demand {background-color: #b6d7a8;}

                    /* The Modal (background) */
                    .modal {
                      display: none;
                      position: fixed;
                      z-index: 1;
                      padding-top: 50px;
                      left: 0;
                      top: 0;
                      width: 100%;
                      height: 100%;
                      overflow: auto;
                      background-color: rgb(0,0,0);
                      background-color: rgba(0,0,0,0.5);
                    }
                    
                    /* Modal Content */
                    .modal-content {
                      background-color: #fefefe;
                      margin: auto;
                      padding: 20px;
                      border: 1px solid #888;
                      width: 80%;
                    }
                    
                    /* The Close Button */
                    .close {
                      color: #aaaaaa;
                      float: right;
                      font-size: 28px;
                      font-weight: bold;
                    }
                    
                    .close:hover,
                    .close:focus {
                      color: #000;
                      text-decoration: none;
                      cursor: pointer;
                    }
                        
                    .p_button {
                      background-color: #999999;
                      color: white;
                      text-align: center;
                      text-decoration: none;
                      display: inline-block;
                      font-size: 14px;
                      padding: 6px;
                      cursor: pointer;
                      border-radius: 25px;
                      border: none;
                    }
                    input[type="text"] {
                        font-size:16px;
                    }
                </style>

                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

                <div id="myModal" class="modal" style="font-family:arial">
                  <div class="modal-content" style="text-align:center">
                    <span class="close">&times;</span>
                    <h1 id="title"></h1>
                    <p><table id="t" style="display:inline-block;font-size:18px;"></table></p>
                    <p id="a"></p>
                  </div>
                </div>

                <table style="margin:0px;padding:0px;border:0px">
                    <tr>
                        <td style="padding:0px; border:none">

                <form method="POST">
                <table style="font-family:arial;border:none" border=1>
                   <tr style="font-weight: bold;height:60px">
                    <td>CRS ID</td>
                    <td>Planned live date</td>
                    <td>UF</td>
                    <td>Cidade</td>
                    <td>Cluster</td>
                    <td>Nota</td>
                    <td>Preço da concorrência</td>
                    <td>Preço</td>
                    <td>MRC</td>
                    <td>CRS Status</td>
                    <td>Status</td>
                  </tr>'''

      for i in range(len(df)):
                    
          html += '<tr id="tr_'+df.iloc[i,0]+'" style="height:63px">'
          html += '<td><input type="hidden" name="crs_id" value="'+df.iloc[i,0]+'">'+df.iloc[i,0]+'</td>'
          html += '<td style="padding-left: 5px;padding-right: 0px;">'+str(df.iloc[i,14])+'</td>'
          html += '<td>'+str(df.iloc[i,3])+'</td>'
          html += '<td>'+str(df.iloc[i,6])+'</td>'
          
          if df.iloc[i,13] == 'Seasonal High Demand':
              cluster = 'Seasonal-High-Demand'
          else:
              if df.iloc[i,13] == 'Regular High Demand':
                  cluster = 'Regular-High-Demand'
              else:
                  if df.iloc[i,13] == 'Seasonal Low Demand':
                      cluster = 'Seasonal-Low-Demand'
                  else:
                      cluster = 'Regular-Low-Demand'
          
          html += '<td class="'+cluster+'">'+str(df.iloc[i,13])+'</td>'
          
          html += '<td><input onkeyup="values(this.id)" type="text" size="5" id="nota_'+df.iloc[i,0]+'" name="nota"></td>'
          html += '<td><input onkeyup="values(this.id)" type="text" size="5" id="cncrn_'+df.iloc[i,0]+'" name="concorrencia"></td>'
          html += '<td><input onkeyup="values(this.id)" type="text" size="5" id="preco_'+df.iloc[i,0]+'" name="preco"></td>'

          if df.iloc[i,5] == 'PTI_Cleared':
              html += '<td class="crs-status-ok">'+str(df.iloc[i,5])+'</td>'
          else:
              html += '<td class="crs-status-not-ok">'+str(df.iloc[i,5])+'</td>'

          if df.iloc[i,2] == 'Active':
              html += '<td class="mrc-ok">'+str(df.iloc[i,2])+'</td>'
          else:
              html += '<td class="mrc-not-ok">'+str(df.iloc[i,2])+'</td>'
          
          if str(df.iloc[i,2]) == 'Active' and str(df.iloc[i,5]) == 'PTI_Cleared':
              html += '<td class="bt-okay"><div>Okay</div></td>'
          else:
              html += '<td class="bt-not-okay"><div>Not okay</div></td>'

          html += '</tr>'

      html += '''   </table>
                    <br>
                    <input class="button" type="submit" value="Okay">
                    </form>
                 </td>

                 <td style="padding:0px;border:none" valign="top">
                    <table style="font-family:arial">
                         <tr style="font-weight: bold;height:60px">
                             <td style ="width:200px">Preview</td>
                        </tr>'''
              
      for i in range(len(df)):
          html +=  '''
                    <tr style="height:63px">
                        <td>
                            <button class = "p_button" id="'''+str(df.iloc[i,0])+'''" onclick="fBase(this.id)">Base</button>
                            <button class = "p_button" id="'''+str(df.iloc[i,0])+'''" onclick="fCeiling(this.id)">Ceiling</button>
                            <button class = "p_button" id="'''+str(df.iloc[i,0])+'''" onclick="fFloor(this.id)">Floor</button>
                        </td>
                    </tr>
                    '''

      html +=  '''
                            </table>
                        
                        </td>
                    </tr>
                </table>
                      
                <script>

                    function values(id) {
                      var x = document.getElementById(id);
                      if (!isNaN(parseFloat(x.value))) {
                        x.value = parseFloat(x.value);
                      } else {
                        x.value = ''
                      }
                    }
                    
                    var modal = document.getElementById("myModal");
                    var span = document.getElementsByClassName("close")[0];

                    fBase = function(id) {
                    
                      modal.style.display = "block";

                      var title = document.getElementById("title")
                      title.innerHTML = 'Base: '.concat(id);

                      preco = document.getElementById("preco_".concat(id.toString())).value
                      nota  = document.getElementById("nota_".concat(id).toString()).value
                      cncrn = document.getElementById("cncrn_".concat(id).toString()).value

                      $.ajax({ url: "/base/"
                             , success: function(result){

                                var table = document.getElementById("t");
                                $("#t tr").remove(); 
            
                                var row = table.insertRow(-1);

                                var oyo_id = row.insertCell(0);
                                oyo_id.innerHTML = 'oyo id';
                                  
                                var date = row.insertCell(1);
                                date.innerHTML = 'date';
                                  
                                var end_date = row.insertCell(2);
                                end_date.innerHTML = 'end date';
                                  
                                var price_1 = row.insertCell(3);
                                price_1.innerHTML = 'price 1';
                                  
                                var price_2 = row.insertCell(4);
                                price_2.innerHTML = 'price 2';
                                  
                                var price_3 = row.insertCell(5);
                                price_3.innerHTML = 'price 3';

                                var price_4 = row.insertCell(6);
                                price_4.innerHTML = 'price 4';
                                  
                                var price_5 = row.insertCell(7);
                                price_5.innerHTML = 'price 5';

                                $.each(result['date'], function(k, v) {

                                      var row = table.insertRow(-1);

                                      var oyo_id = row.insertCell(0);
                                      oyo_id.innerHTML = result['oyo_id'][k];
                                      
                                      var date = row.insertCell(1);
                                      date.innerHTML = result['date'][k];
                                      
                                      var end_date = row.insertCell(2);
                                      end_date.innerHTML = result['end_date'][k];
                                      
                                      var price_1 = row.insertCell(3);
                                      price_1.innerHTML = result['price_1'][k];
                                      
                                      var price_2 = row.insertCell(4);
                                      price_2.innerHTML = result['price_2'][k];
                                      
                                      var price_3 = row.insertCell(5);
                                      price_3.innerHTML = result['price_3'][k];

                                      var price_4 = row.insertCell(6);
                                      price_4.innerHTML = result['price_4'][k];
                                      
                                      var price_5 = row.insertCell(7);
                                      price_5.innerHTML = result['price_5'][k];
                                });
                               }
                             , dataType: "json"
                             , data: { preco: preco
                                     , nota:  nota
                                     , cncrn: cncrn
                                     , id:    id
                                     }
                             });

                    }
                    fCeiling = function(id) {
                      modal.style.display = "block";
                      
                      var title = document.getElementById("title")
                      title.innerHTML = 'Ceiling: '.concat(id);
                      
                      preco = document.getElementById("preco_".concat(id.toString())).value
                      nota  = document.getElementById("nota_".concat(id).toString()).value
                      cncrn = document.getElementById("cncrn_".concat(id).toString()).value

                      $.ajax({ url: "/ceiling/"
                             , success: function(result){

                                var table = document.getElementById("t");
                                $("#t tr").remove(); 
            
                                var row = table.insertRow(-1);

                                var oyo_id = row.insertCell(0);
                                oyo_id.innerHTML = 'oyo id';
                                
                                var start_date = row.insertCell(1);
                                start_date.innerHTML = 'start date';
                                
                                var end_date = row.insertCell(2);
                                end_date.innerHTML = 'end date';
                                
                                var ceiling_so = row.insertCell(3);
                                ceiling_so.innerHTML = 'ceiling so';
                                
                                var ceiling_do = row.insertCell(4);
                                ceiling_do.innerHTML = 'ceiling do';
                                
                                var ceiling_to = row.insertCell(5);
                                ceiling_to.innerHTML = 'ceiling to';
                                
                                var ceiling_4 = row.insertCell(6);
                                ceiling_4.innerHTML = 'ceiling 4';
                                
                                var ceiling_5 = row.insertCell(7);
                                ceiling_5.innerHTML = 'ceiling 5';

                                $.each(result['start_date'], function(k, v) {

                                    var row = table.insertRow(-1);
                                    
                                    var oyo_id = row.insertCell(0);
                                    oyo_id.innerHTML = result['oyo_id'][k];

                                    var start_date = row.insertCell(1);
                                    start_date.innerHTML = result['start_date'][k];
                                    
                                    var end_date = row.insertCell(2);
                                    end_date.innerHTML = result['end_date'][k];
                                    
                                    var ceiling_so = row.insertCell(3);
                                    ceiling_so.innerHTML = result['ceiling_so'][k];
                                    
                                    var ceiling_do = row.insertCell(4);
                                    ceiling_do.innerHTML = result['ceiling_do'][k];
                                    
                                    var ceiling_to = row.insertCell(5);
                                    ceiling_to.innerHTML = result['ceiling_to'][k];
                                    
                                    var ceiling_4 = row.insertCell(6);
                                    ceiling_4.innerHTML = result['ceiling_4'][k];
                                    
                                    var ceiling_5 = row.insertCell(7);
                                    ceiling_5.innerHTML = result['ceiling_5'][k];                                      
                                });
                               }
                             , dataType: "json"
                             , data: { preco: preco
                                     , nota:  nota
                                     , cncrn: cncrn
                                     , id:    id
                                     }
                             });
                      
                    }

                    fFloor = function(id) {
                      modal.style.display = "block";
                      
                      var title = document.getElementById("title")
                      title.innerHTML = 'Floor: '.concat(id);
                      
                      preco = document.getElementById("preco_".concat(id.toString())).value
                      nota  = document.getElementById("nota_".concat(id).toString()).value
                      cncrn = document.getElementById("cncrn_".concat(id).toString()).value

                      $.ajax({ url: "/floor/"
                             , success: function(result){

                                var table = document.getElementById("t");
                                $("#t tr").remove(); 

                                var row = table.insertRow(-1);

                                var oyo_id = row.insertCell(0);
                                oyo_id.innerHTML = 'oyo id';
                                
                                var category = row.insertCell(1);
                                category.innerHTML = 'category';

                                var start_date = row.insertCell(2);
                                start_date.innerHTML = 'start date';

                                var end_date = row.insertCell(3);
                                end_date.innerHTML = 'end date';

                                var c1 = row.insertCell(4);
                                c1.innerHTML = '1';

                                var c2 = row.insertCell(5);
                                c2.innerHTML = '2';

                                var c3 = row.insertCell(6);
                                c3.innerHTML = '3';

                                var c4 = row.insertCell(7);
                                c4.innerHTML = '4';

                                var c5 = row.insertCell(8);
                                c5.innerHTML = '5';

                                var reason = row.insertCell(9);
                                reason.innerHTML = 'reason';

                                var room_category_id = row.insertCell(10);
                                room_category_id.innerHTML = 'room category id';

                                $.each(result['start_date'], function(k, v) {

                                    var row = table.insertRow(-1);
                                    
                                    var oyo_id = row.insertCell(0);
                                    oyo_id.innerHTML = result['oyo_id'][k];

                                    var category = row.insertCell(1);
                                    category.innerHTML = result['category'][k];

                                    var start_date = row.insertCell(2);
                                    start_date.innerHTML = result['start_date'][k];
                                    
                                    var end_date = row.insertCell(3);
                                    end_date.innerHTML = result['end_date'][k];
                                              
                                    var c1 = row.insertCell(4);
                                    c1.innerHTML = result['1'][k];
    
                                    var c2 = row.insertCell(5);
                                    c2.innerHTML = result['2'][k];
    
                                    var c3 = row.insertCell(6);
                                    c3.innerHTML = result['3'][k];
    
                                    var c4 = row.insertCell(7);
                                    c4.innerHTML = result['4'][k];
    
                                    var c5 = row.insertCell(8);
                                    c5.innerHTML = result['5'][k];
    
                                    var reason = row.insertCell(9);
                                    reason.innerHTML = result['reason'][k];
    
                                    var room_category_id = row.insertCell(10);
                                    room_category_id.innerHTML = result['room_category_id'][k];
                                });

                             }
                             , dataType: "json"
                             , data: { preco: preco
                                     , nota:  nota
                                     , cncrn: cncrn
                                     , id:    id
                                     }
                             });

                    }

                    span.onclick = function() {
                      modal.style.display = "none";
                      var table = document.getElementById("t");
                      $("#t tr").remove(); 
                      
                    }
                    
                    window.onclick = function(event) {
                      if (event.target == modal) {
                        modal.style.display = "none";
                        var table = document.getElementById("t");
                        $("#t tr").remove(); 
                      }
                    }
                </script>
       
              '''
      
      return html

app.run( threaded = True
       , host     = '0.0.0.0'
       , port     = 8080
       )
##############
