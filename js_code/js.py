JS_F_BASE = '''     fBase = function(id) {

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

                    }; '''
                                
JS_F_CEILING = '''  fCeiling = function(id) {
                    
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
                      
                    }; '''
                                
JS_F_FLOOR = '''    fFloor = function(id) {
                    
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

                    }; '''
                                
JS_F_LOAD = '''             function load() {

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
                                                                                                                                                         , success: function(result){document.getElementById('content').innerHTML = result;}});
                                                                                                                                                 
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
                          }; '''
                                                                                                                                                         
JS_F_VALUES = '''       function values(id) {
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
                        };  '''

JS_BOTTOM = '''       var span = document.getElementsByClassName("close")[0];
                        span.onclick = function() {
                          document.getElementById("myModal").style.display = "none";
                          var table = document.getElementById("t");
                          $("#t tr").remove(); 
                        };
                        
                        window.onclick = function(event) {
                          if (event.target == modal) {
                            document.getElementById("myModal").style.display = "none";
                            var table = document.getElementById("t");
                            $("#t tr").remove(); 
                          }
                        }; '''