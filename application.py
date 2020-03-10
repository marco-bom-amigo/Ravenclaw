############################
## Importing dependencies ##
############################
from __future__ import print_function
import mimetypes
import pandas as pd
import numpy as np
import decimal
from flask import Flask, request, jsonify

from src.WebApp import WebApp
from src.Revenue import Revenue

from css_code.css import *
from js_code.js import *
from html_code.html import *
############################

##################################
## Set Decimal as ROUND_HALF_UP ##
##################################
context          = decimal.getcontext()
context.rounding = decimal.ROUND_HALF_UP
##################################

web_app = WebApp()
revenue = Revenue()

###############
## Front-End ##
###############
app = Flask(__name__)

@app.route("/base/")
def p_base():
    return jsonify(web_app.render_base(request.args))

@app.route("/ceiling/")
def p_ceiling():
    return jsonify(web_app.render_ceiling(request.args))

@app.route("/floor/")
def p_floor():
    return jsonify(web_app.render_floor(request.args))

@app.route('/BasesPMO/', methods=['GET'])
def Bases_PMO():
    web_app.data.f_Bases_PMO()
    return 'Ok'

@app.route('/LiveLog/', methods=['GET'])
def Live_Log():
    web_app.data.f_Live_Log()
    return 'Ok'

@app.route('/baseprice/', methods=['GET'])
def base_price():
    web_app.data.f_base_price()
    return 'Ok'

@app.route('/weekday/', methods=['GET'])
def weekday():
    web_app.data.f_weekday()
    return 'Ok'

@app.route('/month/', methods=['GET'])
def month():
    web_app.data.f_month()
    return 'Ok'

@app.route('/typeoftourism/', methods=['GET'])
def type_of_tourism():
    web_app.data.f_type_of_tourism()
    return 'Ok'

@app.route('/PropertiesTracker/', methods=['GET'])
def Properties_Tracker():
    web_app.data.f_Properties_Tracker()
    return 'Ok'

@app.route('/peakdates/', methods=['GET'])
def peak_dates():
    web_app.data.f_peak_dates()
    return 'Ok'

@app.route('/pricingmatrix/', methods=['GET'])
def pricing_matrix():
    web_app.data.f_pricing_matrix()
    return 'Ok'

@app.route('/floorprice/', methods=['GET'])
def floor_price():
    web_app.data.f_floor_price()
    return 'Ok'

@app.route('/floorfactor/', methods=['GET'])
def floor_factor():
    web_app.data.f_floor_factor()
    return 'Ok'

@app.route('/clusters/', methods=['GET'])
def clusters():
    web_app.data.f_clusters()
    return 'Ok'

@app.route('/clustermultiplier/', methods=['GET'])
def cluster_multiplier():
    web_app.data.f_cluster_multiplier()
    return 'Ok'

@app.route('/clusterfloor/', methods=['GET'])
def cluster_floor():
    web_app.data.f_cluster_floor()
    return 'Ok'

@app.route('/df/', methods=['GET'])
def df():
    web_app.r_df()
    return 'Ok'

@app.route('/', methods = ['GET', 'POST'])
def hello():

    args = request.args

    if request.method == 'GET':    
        html = '''<html>

                      <head>
                          <title>Revenue OYO</title>
                          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
                          <style>
                            ''' + CSS_MAIN + '''
                          </style>
                          <script>
                            ''' + JS_F_BASE + JS_F_CEILING + JS_F_FLOOR + JS_F_LOAD + JS_F_VALUES + '''
                          </script>
                      </head>
                      
                      <body onload="load()" style="font-family:arial">
                          ''' + HTML_MODAL + HTML_CONTENT + '''
                          <script>
                              ''' + JS_BOTTOM + '''
                          </script>
                      </body>

                  </html>'''
    else:
        #html = web_app.submit_files(args)
        html = jsonify(args)

    return html

@app.route("/load/", methods=['GET', 'POST'])
def load():
    web_app.df = web_app.f_df()
    return web_app.render_load()


app.run( threaded = True
       , host     = '0.0.0.0'
       , port     = 8080
       )
##############

