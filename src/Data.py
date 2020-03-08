import decimal
import pandas as pd
from src.Google import Google
from src.Utils import Utils

class Data(Google):

    #####################################
    ## Read: Bases PMO > hotel_details ##
    #####################################
    ## • MRC                           ##
    #####################################
    def f_Bases_PMO(self):

        r = 'Ok'
        try:
            self.Bases_PMO = self._read_sheet( SPREADSHEET_ID = '1DON-emTbfEUnvlO1RpPzUKz5IhSD_swRAKX65OcPBCA'
                                             , RANGE          = 'hotel_details!A2:R5000'
                                             , COLUMN_INDEXES = [0, 3, 17]
                                             , COLUMN_NAMES   = ['CRS ID', 'hub_name', 'MRC']
                                             )

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    #####################################

    ######################################
    ## Read: Go-live tracker > Live Log ##
    ######################################
    ## • Planned live date              ##
    ######################################
    def f_Live_Log(self):
        r = 'Ok'
        try:
            self.Live_Log = self._read_sheet( SPREADSHEET_ID = '1few_jNvQ6DnsDXHBmypPoi3tds13_nrFLnUnjaqslm8'
                                       , RANGE          = 'Live Log!B3:X5000'
                                       , COLUMN_INDEXES = [0, 1, 12, 22]
                                       , COLUMN_NAMES   = ['CRS ID', 'Property Name', 'Planned live date', 'CRS Status']
                                       )
            
            self.Live_Log = self.Live_Log[self.Live_Log['CRS ID'] != 'Signed']
            self.Live_Log = self.Live_Log[~self.Live_Log['Planned live date'].isin(['Churn', 'Sem Visibilidade', 'LIVE'])]
            self.Live_Log = self.Live_Log[self.Live_Log['Planned live date'] != '']
            
            

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    ######################################
    
    ######################################################
    ## Read: All_new_clustered_RBP > [output]base_price ##
    ######################################################
    ## • Price ranges                                   ##
    ######################################################
    def f_base_price(self):
        r = 'Ok'
        try:
            base_price = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                              , RANGE          = '[output]base_price!S2:T14'
                                              , COLUMN_INDEXES = [0, 1]
                                              , COLUMN_NAMES   = ['0', '1']
                                              )
            # Subset rows
            self.base_price = base_price.iloc[[0, 1, 2, 3, 4, 5, 9, 10, 11, 12], :]
            
            # Converts "base price" to Decimal
            self.base_price['1'] = self.base_price['1'].str.replace('x', '').apply(lambda x: float(decimal.Decimal(x)))
    
        except Exception as e:
            r = "Error: {}".format(e)

        return r
    ######################################################

    ################################################
    ## Read: All_new_clustered_RBP > [aux]weekday ##
    ################################################
    ## • Weekday                                  ##
    ################################################
    def f_weekday(self):
        r = 'Ok'
        try:
            UFs = ['SP', 'RJ', 'ES', 'MG', 'RS', 'SC', 'PR', 'MS', 'MT', 'DF', 'GO', 'TO', 'BA', 'SE', 'AL', 'CE', 'RN', 'PE', 'PB', 'MA', 'PI', 'AM', 'PA', 'AC', 'AP', 'RO', 'RR']
            
            # Regular
            weekday_regular = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                              , RANGE          = '[aux]weekday!C5:ACS11'
                                              , COLUMN_INDEXES = list(range(27))
                                              , COLUMN_NAMES   = UFs
                                              )
            weekday_regular.index = list(range(1, 8))
            
            # Beach
            weekday_beach   = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                              , RANGE          = '[aux]weekday!C15:ACS21'
                                              , COLUMN_INDEXES = list(range(23))
                                              , COLUMN_NAMES   = UFs[0:23]
                                              )
            weekday_beach.index = list(range(1, 8))
            
            # Another
            weekday_another = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                              , RANGE          = '[aux]weekday!C25:ACS31'
                                              , COLUMN_INDEXES = list(range(27))
                                              , COLUMN_NAMES   = UFs
                                              )
            weekday_another.index = list(range(1, 8))
            
            # Converts to Float
            self.weekday_regular = weekday_regular.replace('x', '', regex = True).astype(float)
            weekday_beach[weekday_beach == ''] = 0
            self.weekday_beach   = weekday_beach.replace('x', '', regex = True).astype(float)
            self.weekday_another = weekday_another.replace('x', '', regex = True).astype(float)

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    ################################################
    
    ##############################################
    ## Read: All_new_clustered_RBP > [aux]month ##
    ##############################################
    ## • Month                                  ##
    ##############################################
    def f_month(self):
        r = 'Ok'
        try:
            UFs = ['SP', 'RJ', 'ES', 'MG', 'RS', 'SC', 'PR', 'MS', 'MT', 'DF', 'GO', 'TO', 'BA', 'SE', 'AL', 'CE', 'RN', 'PE', 'PB', 'MA', 'PI', 'AM', 'PA', 'AC', 'AP', 'RO', 'RR']
            
            # Regular
            month_regular = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                            , RANGE          = '[aux]month!C5:AC16'
                                            , COLUMN_INDEXES = list(range(27))
                                            , COLUMN_NAMES   = UFs
                                            )
            month_regular.index = list(range(1, 13))
            
            # Beach
            month_beach   = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                            , RANGE          = '[aux]month!C20:AC31'
                                            , COLUMN_INDEXES = list(range(25))
                                            , COLUMN_NAMES   = UFs[0:25]
                                            )
            month_beach.index = list(range(1, 13))
            
            # Another
            month_another = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                            , RANGE          = '[aux]month!C35:AC46'
                                            , COLUMN_INDEXES = list(range(27))
                                            , COLUMN_NAMES   = UFs
                                            )
            month_another.index = list(range(1, 13))
            
            # Converts to Float
            self.month_regular = month_regular.replace('x', '', regex = True).astype(float)
            month_beach[month_beach == ''] = 0
            self.month_beach   = month_beach.replace('x', '', regex = True).astype(float)
            self.month_another = month_another.replace('x', '', regex = True).astype(float)

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    ##############################################

    ##################################################################
    ## Read: All_new_clustered_RBP > [ACTION_REQUIRED] import_range ##
    ##################################################################
    ## • Type of tourism                                            ##
    ##################################################################
    def f_type_of_tourism(self):
        r = 'Ok'
        try:
            self.type_of_tourism = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                                   , RANGE          = '[ACTION_REQUIRED] import_range!AC2:AG5000'
                                                   , COLUMN_INDEXES = list(range(5))
                                                   , COLUMN_NAMES   = ['City', 'State', 'UF', 'HUBs', 'Type of tourism']
                                                   )
    
        except Exception as e:
            r = "Error: {}".format(e)

        return r
    ##################################################################

    ################################################
    ## Read: Go-live tracker > Properties Tracker ##
    ################################################
    ## • City & UF                                ##
    ################################################
    def f_Properties_Tracker(self):
        r = 'Ok'
        try:
            self.Properties_Tracker = self._read_sheet( SPREADSHEET_ID = '1few_jNvQ6DnsDXHBmypPoi3tds13_nrFLnUnjaqslm8'
                                                      , RANGE          = 'Properties Tracker!D4:J5000'
                                                      , COLUMN_INDEXES = [0, 5, 6]
                                                      , COLUMN_NAMES   = ['CRS ID', 'UF', 'City']
                                                      )

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    ################################################

    ###################################################
    ## Read: All_new_clustered_RBP > [aux]peak_dates ##
    ###################################################
    ## • Peak dates                                  ##
    ###################################################
    def f_peak_dates(self):
        r = 'Ok'
        try:
            self.peak_dates = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                              , RANGE          = '[aux]peak_dates!C7:F5000'
                                              , COLUMN_INDEXES = list(range(4))
                                              , COLUMN_NAMES   = ['Date', 'Event', 'Importance', 'Factor']
                                              )
            
            # Converts "Date" to DateTime
            self.peak_dates['Date'] = pd.to_datetime(self.peak_dates['Date'])
            
            # Converts "Factor" to Float
            self.peak_dates['Factor'] = self.peak_dates['Factor'].astype(float)

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    ###################################################

    ##########################################################
    ## Read: All_new_clustered_RBP > [output]pricing_matrix ##
    ##########################################################
    ## • Pricing matrix                                     ##
    ##########################################################
    def f_pricing_matrix(self):
        r = 'Ok'
        try:
            pricing_matrix = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                             , RANGE          = '[output]pricing_matrix!C2:C5'
                                             , COLUMN_INDEXES = [0]
                                             , COLUMN_NAMES   = ['0']
                                             )
            
            # Transpose the DataFrame
            pricing_matrix = pricing_matrix.T
            
            # Rename the columns
            pricing_matrix.columns = ['Top 30 days', 'Top D-DAY', 'Bottom 30 Days', 'Bottom D-DAY']
            
            # Converts all columns to Float
            self.pricing_matrix = pricing_matrix.astype(float)

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    ##########################################################

    #######################################################
    ## Read: All_new_clustered_RBP > [output]floor_price ##
    #######################################################
    ## • Floor price by importance                       ##
    #######################################################
    def f_floor_price(self):
        r = 'Ok'
        try:
            floor_price = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
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
            
            self.floor_price = floor_price
    
        except Exception as e:
            r = "Error: {}".format(e)

        return r
    #######################################################

    #######################################################
    ## Read: All_new_clustered_RBP > [output]floor_price ##
    #######################################################
    ## • Floor factor                                    ##
    #######################################################
    def f_floor_factor(self):
        r = 'Ok'
        try:
            floor_factor = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                           , RANGE          = '[output]floor_price!P11'
                                           , COLUMN_INDEXES = [0]
                                           , COLUMN_NAMES   = ['Floor Factor']
                                           )
            
            # Converts "Floor Factor" to Float
            floor_factor['Floor Factor'] = floor_factor['Floor Factor'].astype(float)
    
            self.floor_factor = floor_factor

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    #######################################################

    ##############################
    ## Clusters > Clusters BRA  ##
    ##############################
    ## • Clusters by UF & City  ##
    ##############################
    def f_clusters(self):
        r = 'Ok'
        try:
            clusters = self._read_sheet( SPREADSHEET_ID = '12E00hjlTlBllMP8q4qlq3Xkjc_mjmgIaEpDatam20b4'
                                       , RANGE          = 'Clusters BRA!A2:I5000'
                                       , COLUMN_INDEXES = list(range(9))
                                       , COLUMN_NAMES   = ['City', 'State', 'UF', 'Seasonal/Touristic', '# inhabitants > 500k', 'Access', 'Group 1', 'Group 2', 'Cluster']
                                       )
        
            # Creats a City column to be modified
            clusters['CityMod'] = clusters['City'].copy()
            
            # Removes the Cluster City punctuation
            clusters['CityMod'] = self.utils.punctuation(clusters['CityMod'])
            
            self.clusters = clusters

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    #############################

    #################################################
    ## Read: All_new_clustered_RBP > Clusterização ##
    #################################################
    ## • Cluster multiplier base                   ##
    #################################################
    def f_cluster_multiplier(self):
        r = 'Ok'
        try:
            cluster_multiplier = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                                 , RANGE          = 'Clusterização!L4:O7'
                                                 , COLUMN_INDEXES = [0,1,2,3]
                                                 , COLUMN_NAMES   = ['Cluster', 'High', 'Mid', 'Low']
                                                 )
            cluster_multiplier = cluster_multiplier.dropna()
            cluster_multiplier[['High', 'Mid', 'Low']] = cluster_multiplier[['High', 'Mid', 'Low']].astype(float)
    
            self.cluster_multiplier = cluster_multiplier

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    #################################################

    #################################################
    ## Read: All_new_clustered_RBP > Clusterização ##
    #################################################
    ## • Cluster multiplier floor                  ##
    #################################################
    def f_cluster_floor(self):
        r = 'Ok'
        try:
            cluster_floor = self._read_sheet( SPREADSHEET_ID = '1iP52JQqWkABOvs_P6eSAGbYpbGSy1k4OSL_xEkZZMII'
                                      , RANGE          = 'Clusterização!L13:M16'
                                      , COLUMN_INDEXES = [0,1]
                                      , COLUMN_NAMES   = ['Cluster', 'Factor']
                                      )
            cluster_floor['Factor'] = cluster_floor['Factor'].astype(float)
    
            self.cluster_floor = cluster_floor

        except Exception as e:
            r = "Error: {}".format(e)

        return r
    #################################################

    def __init__(self):
        super().__init__()
        self.utils = Utils()

