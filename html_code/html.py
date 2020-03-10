HTML_MODAL = '''<div id="myModal" class="modal" style="font-family:arial">
                  <div class="modal-content" style="text-align:center">
                    <span class="close">&times;</span>
                    <h1 id="title"></h1>
                    <p><table id="t" style="display:inline-block;font-size:18px;"></table></p>
                    <p id="a"></p>
                  </div>
                </div>'''
                
HTML_CONTENT = '''    <div id="content">
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
                          
                          <table id="ld" style="margin-left:20px">
                              <tr class="head_row">
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
                      </div>'''
                      
HTML_PROPERTIES_HEAD = '''<tr class="head_row">
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

HTML_PREVIEW_HEAD = '''<tr style="font-weight: bold;height:60px;color: white;background: black;">
                             <td style ="width:200px">Preview</td>
                       </tr>'''