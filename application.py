############################
## Importing dependencies ##
############################
from __future__ import print_function
import mimetypes
import pandas as pd
import numpy as np
import decimal
from flask import Flask, request, jsonify

from src.Revenue import Revenue
############################

##################################
## Set Decimal as ROUND_HALF_UP ##
##################################
context          = decimal.getcontext()
context.rounding = decimal.ROUND_HALF_UP
##################################

revenue = Revenue()

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

    df_plan = revenue.df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][revenue.df['CRS ID'] == oyo_id]

    dt              = df_plan['Planned live date'].values[0]
    estado          = df_plan['UF'].values[0]
    type_of_tourism = df_plan['Type of tourism'].values[0]
    cluster         = df_plan['Cluster'].values[0]
    
    revenue.root_base(dt, estado, type_of_tourism)

    df_out_base    = revenue.base(oyo_id, nota, price, cluster)

    return jsonify(df_out_base.to_dict())

@app.route("/ceiling/")
def p_ceiling():
    args = request.args

    oyo_id = str(args.get('id'))
    price  = float(args.getlist('preco')[0])

    df_plan         = revenue.df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][revenue.df['CRS ID'] == oyo_id]
    dt              = df_plan['Planned live date'].values[0]
    estado          = df_plan['UF'].values[0]
    type_of_tourism = df_plan['Type of tourism'].values[0]
    
    revenue.root_base(dt, estado, type_of_tourism)

    df_out_ceiling = revenue.ceiling(oyo_id, price)

    return jsonify(df_out_ceiling.to_dict())

@app.route("/floor/")
def p_floor():
    args = request.args

    oyo_id = str(args.get('id'))
    price  = float(args.getlist('preco')[0])
    nota   = float(args.getlist('nota')[0])

    df_plan = revenue.df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][revenue.df['CRS ID'] == oyo_id]
    dt              = df_plan['Planned live date'].values[0]
    estado          = df_plan['UF'].values[0]
    type_of_tourism = df_plan['Type of tourism'].values[0]
    cluster         = df_plan['Cluster'].values[0]

    revenue.root_base(dt, estado, type_of_tourism)

    df_out_base    = revenue.base(oyo_id, nota, price, cluster)

    df_out_floor   = revenue.floor(df_out_base, oyo_id, nota, cluster)

    return jsonify(df_out_floor.to_dict())

@app.route('/BasesPMO/', methods=['GET'])
def Bases_PMO():
    revenue.data.f_Bases_PMO()
    return 'Ok'

@app.route('/LiveLog/', methods=['GET'])
def Live_Log():
    revenue.data.f_Live_Log()
    return 'Ok'

@app.route('/baseprice/', methods=['GET'])
def base_price():
    revenue.data.f_base_price()
    return 'Ok'

@app.route('/weekday/', methods=['GET'])
def weekday():
    revenue.data.f_weekday()
    return 'Ok'

@app.route('/month/', methods=['GET'])
def month():
    revenue.data.f_month()
    return 'Ok'

@app.route('/typeoftourism/', methods=['GET'])
def type_of_tourism():
    revenue.data.f_type_of_tourism()
    return 'Ok'

@app.route('/PropertiesTracker/', methods=['GET'])
def Properties_Tracker():
    revenue.data.f_Properties_Tracker()
    return 'Ok'

@app.route('/peakdates/', methods=['GET'])
def peak_dates():
    revenue.data.f_peak_dates()
    return 'Ok'

@app.route('/pricingmatrix/', methods=['GET'])
def pricing_matrix():
    revenue.data.f_pricing_matrix()
    return 'Ok'

@app.route('/floorprice/', methods=['GET'])
def floor_price():
    revenue.data.f_floor_price()
    return 'Ok'

@app.route('/floorfactor/', methods=['GET'])
def floor_factor():
    revenue.data.f_floor_factor()
    return 'Ok'

@app.route('/clusters/', methods=['GET'])
def clusters():
    revenue.data.f_clusters()
    return 'Ok'

@app.route('/clustermultiplier/', methods=['GET'])
def cluster_multiplier():
    revenue.data.f_cluster_multiplier()
    return 'Ok'

@app.route('/clusterfloor/', methods=['GET'])
def cluster_floor():
    revenue.data.f_cluster_floor()
    return 'Ok'

@app.route('/df/', methods=['GET'])
def df():
    revenue.r_df()
    return 'Ok'


@app.route('/', methods=['GET'])
def hello():

    return '''<html>
                  <head>
                  
                      <title>Revenue OYO</title>

                      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

<style>

                    table {border-collapse: collapse;}
                    td, th {border: 1px solid black}
                    td {padding: 5px; height:55px}
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
                      padding:0px;
                      padding-left:2px;
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
                      background-color: #666;
                      color: white;
                      text-align: center;
                      text-decoration: none;
                      display: inline-block;
                      font-size: 14px;
                      padding: 6px;
                      cursor: pointer;
                      border-radius: 25px;
                      border: none;
                      float:left;
                      margin-left:2px;
                    }
                    input[type="text"] {
                        font-size:16px;
                    }
                </style>

                <script>

                    fBase = function(id) {

                      document.getElementById("myModal").style.display = "block";

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
                    
                      document.getElementById("myModal").style.display = "block";
                      
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
                    
                      document.getElementById("myModal").style.display = "block";
                      
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


                </script>


                      <script>

                          function load() {

                              var value = 'BasesPMO';
                              $.ajax({ url: '/'.concat(value).concat('/')
                                     , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                     , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                     , complete: function(result) {
                                     
                                          value = 'LiveLog';
                                          $.ajax({ url: '/'.concat(value).concat('/')
                                                 , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                 , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                 , complete: function(result) {
                                                 
                                                  value = 'baseprice';
                                                  $.ajax({ url: '/'.concat(value).concat('/')
                                                         , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                         , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                         , complete: function(result) {
                                                         
                                                          value = 'weekday';
                                                          $.ajax({ url: '/'.concat(value).concat('/')
                                                                 , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                 , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                 , complete: function(result) {
                                                                 
                                                                  value = 'month';
                                                                  $.ajax({ url: '/'.concat(value).concat('/')
                                                                         , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                         , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                         , complete: function(result) {
                                                                         
                                                                          value = 'typeoftourism';
                                                                          $.ajax({ url: '/'.concat(value).concat('/')
                                                                                 , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                 , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                 , complete: function(result) {
                                                                                 
                                                                                  value = 'PropertiesTracker';
                                                                                  $.ajax({ url: '/'.concat(value).concat('/')
                                                                                         , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                         , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                         , complete: function(result) {
                                                                                         
                                                                                          value = 'peakdates';
                                                                                          $.ajax({ url: '/'.concat(value).concat('/')
                                                                                                 , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                                 , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                                 , complete: function(result) {
                                                                                                 
                                                                                                  value = 'pricingmatrix';
                                                                                                  $.ajax({ url: '/'.concat(value).concat('/')
                                                                                                         , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                                         , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                                         , complete: function(result) {
                                                                                                         
                                                                                                          value = 'floorprice';
                                                                                                          $.ajax({ url: '/'.concat(value).concat('/')
                                                                                                                 , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                                                 , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                                                 , complete: function(result) {
                                                                                                                 
                                                                                                                  value = 'floorfactor';
                                                                                                                  $.ajax({ url: '/'.concat(value).concat('/')
                                                                                                                         , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                                                         , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                                                         , complete: function(result) {
                                                                                                                         
                                                                                                                          value = 'clusters';
                                                                                                                          $.ajax({ url: '/'.concat(value).concat('/')
                                                                                                                                 , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                                                                 , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                                                                 , complete: function(result) {
                                                                                                                                 
                                                                                                                                  value = 'clustermultiplier';
                                                                                                                                  $.ajax({ url: '/'.concat(value).concat('/')
                                                                                                                                         , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                                                                         , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                                                                         , complete: function(result) {
                                                                                                                                         
                                                                                                                                          value = 'clusterfloor';
                                                                                                                                          $.ajax({ url: '/'.concat(value).concat('/')
                                                                                                                                                 , success: function(result){document.getElementById(value).innerHTML = 'Ok';document.getElementById(value).classList.add("bt-okay");}
                                                                                                                                                 , error: function(result) {document.getElementById(value).innerHTML = 'Error';document.getElementById(value).classList.add("bt-not-okay");}
                                                                                                                                                 , complete: function(result) {
                                                                                                                                                         $.ajax({url: "/load/"
                                                                                                                                                         , success: function(result){document.getElementById('content').innerHTML = result;}
                                                                                                                                                                });
                                                                                                                                                 
                                                                                                                                          }})
                                                                                                                                  }})
                                                                                                                          }})
                                                                                                                  }})
                                                                                                          }})
                                                                                                  }})
                                                                                          }})
                                                                                  }})
                                                                          }})
                                                                  }})
                                                          }})
                                                  }})
                                          }})
                              }})
                          }

                          function onLoad() {
                              load();
                          }

                      </script>

                    <script>
                        function values(id) {
                          var x = document.getElementById(id);
                          if (!isNaN(parseFloat(x.value))) {
                            x.value = parseFloat(x.value);
                            var j_ID = "BR_".concat(id.split("_")[2])
                            var i_nota  = document.getElementById("nota_".concat(j_ID))
                            var i_cncrn = document.getElementById("cncrn_".concat(j_ID))
                            var i_preco = document.getElementById("preco_".concat(j_ID))
                            
                            if (i_nota.value != '' && i_cncrn.value != '' && i_preco.value != '') {
                              document.getElementById("tr_".concat(j_ID)).style.backgroundColor = "#DDFFDD";
                              document.getElementById("pr_".concat(j_ID)).style.backgroundColor = "#4CAF50";
                            } else {
                              document.getElementById("tr_".concat(j_ID)).style.backgroundColor = "#FFFFFF";
                              document.getElementById("pr_".concat(j_ID)).style.backgroundColor = "#FFFFFF";
                            }
                    
                          } else {
                            x.value = ''
                          }
                        }
                    
                    </script>
                      
                  </head>
                  
                  <body onload="onLoad()" style="font-family:arial">

                <div id="myModal" class="modal" style="font-family:arial">
                  <div class="modal-content" style="text-align:center">
                    <span class="close">&times;</span>
                    <h1 id="title"></h1>
                    <p><table id="t" style="display:inline-block;font-size:18px;"></table></p>
                    <p id="a"></p>
                  </div>
                </div>

                  
                      <div id="content">
                          <table style="">
                              <tr>
                                  <td style="padding-left:20px; border:none">
                                      <h1 style="margin:0px">Carregando <i>(Lendo Google Sheets)</i>...</h1>
                                  </td>
                                  <td style="padding-left:20px; border:none">
                                      <img height="30" src="https://gifimage.net/wp-content/uploads/2017/09/ajax-loading-gif-transparent-background-2.gif">
                                  </td>
                              </tr>
                          </table>

                          <style>
                            #ld tr td {height:0px;padding: 8px;font-size: 16px;}
                          </style>
                          <table id="ld" style="margin-left:20px">
                              <tr style="font-weight: bold">
                                  <td style="; border:none"></td>
                                  <td>Dados</td>
                                  <td>Planilha</td>
                                  <td>Aba</td>
                                  <td>Status</td>
                              </tr>
                              
                              <tr>
                                  <td>( 1/14)</td>
                                  <td>Bases_PMO</td>
                                  <td>Bases PMO</td>
                                  <td>hotel_details</td>
                                  <td id="BasesPMO"></td>
                              </tr>

                              <tr>
                                  <td>( 2/14)</td>
                                  <td>Live_Log</td>
                                  <td>Go-live tracker</td>
                                  <td>Live Log</td>
                                  <td id="LiveLog"></td>
                              </tr>

                              <tr>
                                  <td>( 3/14)</td>
                                  <td>base_price</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>[output]base_price</td>
                                  <td id="baseprice"></td>
                              </tr>

                              <tr>
                                  <td>( 4/14)</td>
                                  <td>weekday</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>[aux]weekday</td>
                                  <td id="weekday"></td>
                              </tr>

                              <tr>
                                  <td>( 5/14)</td>
                                  <td>month</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>[aux]month</td>
                                  <td id="month"></td>
                              </tr>

                              <tr>
                                  <td>( 6/14)</td>
                                  <td>type_of_tourism</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>[ACTION_REQUIRED] import_range</td>
                                  <td id="typeoftourism"></td>
                              </tr>

                              <tr>
                                  <td>( 7/14)</td>
                                  <td>Properties_Tracker</td>
                                  <td>Go-live tracker</td>
                                  <td>Properties Tracker</td>
                                  <td id="PropertiesTracker"></td>
                              </tr>

                              <tr>
                                  <td>( 8/14)</td>
                                  <td>peak_dates</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>[aux]peak_dates</td>
                                  <td id="peakdates"></td>
                              </tr>

                              <tr>
                                  <td>( 9/14)</td>
                                  <td>pricing_matrix</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>[output]pricing_matrix</td>
                                  <td id="pricingmatrix"></td>
                              </tr>

                              <tr>
                                  <td>(10/14)</td>
                                  <td>floor_price</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>[output]floor_price</td>
                                  <td id="floorprice"></td>
                              </tr>

                              <tr>
                                  <td>(11/14)</td>
                                  <td>floor_factor</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>[output]floor_price</td>
                                  <td id="floorfactor"></td>
                              </tr>

                              <tr>
                                  <td>(12/14)</td>
                                  <td>clusters</td>
                                  <td>Clusters</td>
                                  <td>Clusters BRA</td>
                                  <td id="clusters"></td>
                              </tr>

                              <tr>
                                  <td>(13/14)</td>
                                  <td>cluster_multiplier</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>Clusterização</td>
                                  <td id="clustermultiplier"></td>
                              </tr>

                              <tr>
                                  <td>(14/14)</td>
                                  <td>cluster_floor</td>
                                  <td>All_new_clustered_RBP</td>
                                  <td>Clusterização</td>
                                  <td id="clusterfloor"></td>
                              </tr>

                          </table>
                      </div>
                          <script>
                        var span = document.getElementsByClassName("close")[0];
                        span.onclick = function() {
                          document.getElementById("myModal").style.display = "none";
                          var table = document.getElementById("t");
                          $("#t tr").remove(); 
                        }
                        
                        window.onclick = function(event) {
                          if (event.target == modal) {
                            document.getElementById("myModal").style.display = "none";
                            var table = document.getElementById("t");
                            $("#t tr").remove(); 
                          }
                        }
                      </script>
    
                  </body>
              </html>
           '''

@app.route("/load/", methods=['GET', 'POST'])
def load():

    revenue.df = revenue.f_df()

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

        df_plan = df_plan.merge(revenue.df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster', 'hub_name']])

        hubs = []

        for i in range(len(df_plan)):
            oyo_id          = df_plan['CRS ID'][i]
            price           = df_plan['Preço'][i]
            dt              = df_plan['Planned live date'][i]
            estado          = df_plan['UF'][i]
            type_of_tourism = df_plan['Type of tourism'][i]
            nota            = df_plan['nota'][i]
            cluster         = df_plan['Cluster'][i]
            hub_name        = df_plan['hub_name'][i]

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

      html = '''


                <table style="margin:0px;padding:0px;border:0px">
                    <tr>
                        <td style="padding:0px; border:none">

                <form method="POST">
                <table style="font-family:arial;border:none" border=1>
                   <tr style="font-weight: bold;height:60px; color: white;background: black;">
                    <td>CRS ID</td>
                    <td>Nome</td>
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

      for i in range(len(revenue.df)):
                    
          html += '<tr id="tr_'+revenue.df['CRS ID'][i]+'" style="height:63px">'
          html += '<td><input type="hidden" name="crs_id" value="'+revenue.df['CRS ID'][i]+'">'+revenue.df['CRS ID'][i]+'</td>'
          html += '<td>'+str(revenue.df['Property Name'][i])+'</td>'
          html += '<td style="padding-left: 0px;padding-right: 0px;font-size: 15px;">'+str(revenue.df['Planned live date desc'][i])+'</td>'
          html += '<td>'+str(revenue.df['UF'][i])+'</td>'
          html += '<td>'+str(revenue.df['City'][i])+'</td>'
          
          if revenue.df['Cluster'][i] == 'Seasonal High Demand':
              cluster = 'Seasonal-High-Demand'
          else:
              if revenue.df['Cluster'][i] == 'Regular High Demand':
                  cluster = 'Regular-High-Demand'
              else:
                  if revenue.df['Cluster'][i] == 'Seasonal Low Demand':
                      cluster = 'Seasonal-Low-Demand'
                  else:
                      cluster = 'Regular-Low-Demand'

          html += '<td class="'+cluster+'">'+str(revenue.df['Cluster'][i])+'</td>'
          
          html += '<td><input onexit="values(this.id)" onkeyup="values(this.id)" type="text" size="5" id="nota_'+revenue.df['CRS ID'][i]+'" name="nota"></td>'
          html += '<td><input onexit="values(this.id)" onkeyup="values(this.id)" type="text" size="5" id="cncrn_'+revenue.df['CRS ID'][i]+'" name="concorrencia"></td>'
          html += '<td><input onexit="values(this.id)" onkeyup="values(this.id)" type="text" size="5" id="preco_'+revenue.df['CRS ID'][i]+'" name="preco"></td>'

          if revenue.df['MRC'][i] == 'PTI_Cleared':
              html += '<td class="crs-status-ok">'+str(revenue.df['MRC'][i])+'</td>'
          else:
              html += '<td class="crs-status-not-ok">'+str(revenue.df['MRC'][i])+'</td>'

          if revenue.df.iloc[i,2] == 'Active':
              html += '<td class="mrc-ok">'+str(revenue.df['CRS Status'][i])+'</td>'
          else:
              html += '<td class="mrc-not-ok">'+str(revenue.df['CRS Status'][i])+'</td>'
          
          if str(revenue.df['CRS Status'][i]) == 'Active' and str(revenue.df['MRC'][i]) == 'PTI_Cleared':
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
                         <tr style="font-weight: bold;height:60px;color: white;background: black;">
                             <td style ="width:200px">Preview</td>
                        </tr>'''
              
      for i in range(len(revenue.df)):
          html +=  '''
                    <tr style="height:63px" id="pr_'''+revenue.df['CRS ID'][i]+'''">
                        <td style="padding:0px">
                            <button class = "p_button" id="'''+str(revenue.df['CRS ID'][i])+'''" onclick="fBase(this.id)">Base</button>
                            <button class = "p_button" id="'''+str(revenue.df['CRS ID'][i])+'''" onclick="fCeiling(this.id)">Ceiling</button>
                            <button class = "p_button" id="'''+str(revenue.df['CRS ID'][i])+'''" onclick="fFloor(this.id)">Floor</button>
                        </td>
                    </tr>
                    '''

      html +=  '''
                            </table>
                        
                        </td>
                    </tr>
                </table>
              '''

      return html

app.run( threaded = True
       , host     = '0.0.0.0'
       , port     = 8080
       )
##############

