from datetime import datetime, timedelta
import decimal
import pytz
import numpy as np
import pandas as pd
from src.Utils import Utils
from src.Data import Data

class Revenue:
    
    ################################################################################
    ## Creates the df DataFrame                                                   ##
    ## Merge: Lve log, Properties Tracker, Bases PMO , Clusters & Type of tourism ##
    ################################################################################
    def f_df(self):
    
        # Merge: Live Log & Properties Tracker
        df = self.data.Live_Log.merge(self.data.Properties_Tracker)
        
        # ... & Bases PMO
        df = df.merge(self.data.Bases_PMO)

        # Converts "City" to Str
        df['City'] = df['City'].astype(str)

        # Saves the original city name
        cities = df['City'].copy()
        
        # Removes the Properties Tracker City punctuaton
        df['City'] = self.utils.punctuation(df['City'])

        # Merge the Clusters...
        df = df.merge( self.data.clusters
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
        df = df[df['Planned live date'] >= self.today]
        
        # Sort by "Planned live date"
        df = df.sort_values('Planned live date')
        
        # Set the non-defined cities as "Regular Low Demand"
        df['Cluster'][df['Cluster'] == ''] = 'Regular Low Demand'
        
        df = df.merge(self.data.type_of_tourism[['City', 'UF', 'Type of tourism']], left_on = ['UF', 'City'], right_on = ['UF', 'City'], how = 'left')
        df['Type of tourism'] = df['Type of tourism'].fillna('Regular')

        df = df.drop_duplicates(keep = 'last', subset = 'CRS ID')
        df.reset_index(inplace = True) 

        self.df = df
        
        return df
    ##############################################################

    #########################################################
    ## Function: Root base                                 ##
    #########################################################
    ## • Creates the basic data frame, used for all others ##
    #########################################################
    def root_base(self, dt, estado, type_of_tourism):
        
        # Creates the DataFrame with 365 days
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
            df_base = df_base.merge(self.data.month_regular[estado], left_on='month', right_index=True);
        else:
            if type_of_tourism ==  'Beach':
                    df_base = df_base.merge(self.data.month_beach[estado], left_on='month', right_index=True);
            else:
                    df_base = df_base.merge(self.data.month_another[estado], left_on='month', right_index=True);
        df_base = df_base.rename(columns = {estado:'Month Factor'})
        
        # Merge: df_base & weekday
        if type_of_tourism == 'Regular':
            df_base = df_base.merge(self.data.weekday_regular[estado], left_on = 'dayofweek', right_index=True);
        else:
            if type_of_tourism ==  'Beach':
                    df_base = df_base.merge(self.data.weekday_beach[estado], left_on = 'dayofweek', right_index=True);
            else:
                    df_base = df_base.merge(self.data.weekday_another[estado], left_on = 'dayofweek', right_index=True);
        df_base = df_base.rename(columns = {estado:'Weekday Factor'})
    
        # Merge: df_base & peak dates
        df_base = df_base.merge(self.data.peak_dates[['Date', 'Factor']], left_on = 'date', right_on = 'Date', how = 'left')
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
            
            if (df_base.iloc[i, 0] - pd.to_datetime(self.today)).days < self.data.base_price['1'][10]:
                df_base.iloc[i, 6] = 1
            else:
                before = before * (1 + self.data.base_price['1'][12])
                if before > self.data.base_price['1'][11]:
                    before = self.data.base_price['1'][11]
                df_base.iloc[i, 6] = before
    
        df_base['Stagger'] = df_base['Stagger'].astype(float)
    
        # Creates the Factor column
        df_base['Factor'] = df_base['Month Factor'] * df_base['Weekday Factor'] * df_base['Peak Factor'] * df_base['Stagger']
        df_base['Factor'][df_base['Factor'] > self.data.base_price['1'][9]] = self.data.base_price['1'][9]
        df_base['Factor'] = df_base['Factor'].astype(float)

        self.df_root_base = df_base
    #########################################################

    ##############################
    ## Function: Base           ##
    ##############################
    ## • Creates the Base sheet ##
    ##############################
    def base(self, oyo_id, nota, price, cluster):
    
        price = self.getPrice(cluster, nota, price)
        
        columns = ['price_1', 'price_2', 'price_3', 'price_4', 'price_5']
        
        df_base = self.df_root_base.copy()

        for i, price_column in enumerate(columns):
    
            # Creates the "price" columns
            df_base[price_column] = ((price * self.data.base_price['1'][i + 1]) * self.df_root_base['Factor']) / self.data.base_price['1'][0]

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
    def ceiling(self, oyo_id, price):
    
        df_base = self.df_root_base
        
        columns = ['ceiling_so', 'ceiling_do', 'ceiling_to', 'ceiling_4', 'ceiling_5']
        for i, price_column in enumerate(columns):
    
            # Creates the "ceiling_so" column
            df_base[price_column] = price * self.data.base_price['1'][i + 1] * self.df_root_base['Factor'] * self.data.pricing_matrix['Top 30 days'][0]
    
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
    def floor(self, df_base, oyo_id, nota, cluster):
    
       df_r = self.df_root_base.copy()
        
       # Creates the "Peak Date Factor" column
       df_r['Peak Date Factor'] = 6
       df_r['Peak Date Factor'][df_r['Peak Factor'] == 2]  = 0
    
       # Merge: df_base & floor_price
       df_r = df_r.merge( self.data.floor_price[['Importance', '1', '2', '3', '4', '5']]
                        , left_on  = 'Peak Date Factor'
                        , right_on = 'Importance'
                        , how      = 'left'
                        )

       # Creates the "df_out_floor" DataFrame
       df_out_floor = df_base.copy()
    
       for i in range(1, 6):
           c1 = i

           df_out_floor[str(c1)] = np.where( self.getPrice(cluster, nota, df_base['price_' + str(c1)], 'Floor') <= df_r[str(c1)]
                                           , self.getPrice(cluster, nota, df_base['price_' + str(c1)], 'Floor')
                                           , df_r[str(c1)]
                                           ) / self.data.floor_factor['Floor Factor'][0]
    
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
       df_out_floor['start_date'] = pd.to_datetime(df_out_floor['start_date']).dt.strftime('%d/%m/%Y')
       df_out_floor['end_date']   = pd.to_datetime(df_out_floor['end_date']).dt.strftime('%d/%m/%Y')
       
       return df_out_floor
    ###############################

    #####################################
    ## Function: Get price             ##
    #####################################
    ## • Set price on Cluster and Nota ##
    #####################################
    def getPrice(self, cluster, nota, pre_price, plan = 'Base'):
            
        if plan == 'Base':
            
            # Get Cluster multiplier
            aux = self.data.cluster_multiplier[self.data.cluster_multiplier['Cluster'].str.lower() == cluster.lower()][['High', 'Mid', 'Low']].reset_index()
            price = aux['Mid'][0] * pre_price
            
            # Get multiplier on Nota
            if nota < 6.5:
                price = aux['Low'][0] * pre_price
            if nota > 8:
                price = aux['High'][0] * pre_price
    
        else:
           price = pre_price * self.data.cluster_floor[self.data.cluster_floor['Cluster'].str.lower() == cluster.lower()]['Factor'].values[0]
    
        return price
    #####################################


    def __init__(self):
        
        #####################
        ## Get current day ##
        #####################
        source_date               = datetime.now()
        source_time_zone          = pytz.timezone('US/Eastern')
        source_date_with_timezone = source_time_zone.localize(source_date)
        target_time_zone          = pytz.timezone('US/Eastern')
        target_date_with_timezone = source_date_with_timezone.astimezone(target_time_zone)
        self.today = pd.to_datetime(target_date_with_timezone.today() - timedelta(days = 1))
        #####################
        
        self.utils = Utils()
        self.data = Data()
        
