import pandas as pd
from html_code.html import HTML_PROPERTIES_HEAD, HTML_PREVIEW_HEAD

from src.Revenue import Revenue

class WebApp(Revenue):
    
    def render_load(self):

      html = '''<table style="margin:0px;padding:0px;border:0px">
                    <tr>
                        <td style="padding:0px; border:none">
                            <form method="POST">
                                <table style="font-family:arial;border:none" border=1>
                                ''' + HTML_PROPERTIES_HEAD


      for i in range(len(self.df)):
                    
          html += '<tr id="tr_'+self.df['CRS ID'][i]+'" style="height:63px">'
          html += '<td><input type="hidden" name="crs_id" value="'+self.df['CRS ID'][i]+'">'+self.df['CRS ID'][i]+'</td>'
          html += '<td>'+str(self.df['Property Name'][i])+'</td>'
          html += '<td style="padding-left: 0px;padding-right: 0px;font-size: 15px;">'+str(self.df['Planned live date desc'][i])+'</td>'
          html += '<td>'+str(self.df['UF'][i])+'</td>'
          html += '<td>'+str(self.df['City'][i])+'</td>'
          
          if self.df['Cluster'][i] == 'Seasonal High Demand':
              cluster = 'Seasonal-High-Demand'
          else:
              if self.df['Cluster'][i] == 'Regular High Demand':
                  cluster = 'Regular-High-Demand'
              else:
                  if self.df['Cluster'][i] == 'Seasonal Low Demand':
                      cluster = 'Seasonal-Low-Demand'
                  else:
                      cluster = 'Regular-Low-Demand'

          html += '<td class="'+cluster+'">'+str(self.df['Cluster'][i])+'</td>'
          
          html += '<td><input onexit="values(this.id)" onkeyup="values(this.id)" type="text" size="5" id="nota_'+self.df['CRS ID'][i]+'" name="nota"></td>'
          html += '<td><input onexit="values(this.id)" onkeyup="values(this.id)" type="text" size="5" id="cncrn_'+self.df['CRS ID'][i]+'" name="concorrencia"></td>'
          html += '<td><input onexit="values(this.id)" onkeyup="values(this.id)" type="text" size="5" id="preco_'+self.df['CRS ID'][i]+'" name="preco"></td>'

          if self.df['MRC'][i] == 'PTI_Cleared':
              html += '<td class="crs-status-ok">'+str(self.df['MRC'][i])+'</td>'
          else:
              html += '<td class="crs-status-not-ok">'+str(self.df['MRC'][i])+'</td>'

          if self.df.iloc[i,2] == 'Active':
              html += '<td class="mrc-ok">'+str(self.df['CRS Status'][i])+'</td>'
          else:
              html += '<td class="mrc-not-ok">'+str(self.df['CRS Status'][i])+'</td>'
          
          if str(self.df['CRS Status'][i]) == 'Active' and str(self.df['MRC'][i]) == 'PTI_Cleared':
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
              ''' + HTML_PREVIEW_HEAD
      
      for i in range(len(self.df)):
          html +=  '''
                    <tr style="height:63px" id="pr_'''+self.df['CRS ID'][i]+'''">
                        <td style="padding:0px">
                            <button class = "p_button" id="'''+str(self.df['CRS ID'][i])+'''" onclick="fBase(this.id)">Base</button>
                            <button class = "p_button" id="'''+str(self.df['CRS ID'][i])+'''" onclick="fCeiling(this.id)">Ceiling</button>
                            <button class = "p_button" id="'''+str(self.df['CRS ID'][i])+'''" onclick="fFloor(this.id)">Floor</button>
                        </td>
                    </tr>
                    '''

      html +=  '''          </table>
                        </td>
                    </tr>
                </table>
              '''

      return html
    
    def submit_files(self, args):

        crs_id = args.getlist('crs_id')
        preco  = args.getlist('preco')
        nota   = args.getlist('nota')
        
        df_plan = pd.DataFrame(list(zip(crs_id, preco)), columns = ['CRS ID', 'Preço'])
        df_plan['nota'] = nota
        df_plan = df_plan[df_plan['Preço'] != '']
        df_plan['Preço'] = df_plan['Preço'].astype(int)
        df_plan['nota'] = df_plan['nota'].astype(float)

        self.df['CRS ID'] = self.df['CRS ID'].astype('str')
        df_plan['CRS ID'] = df_plan['CRS ID'].astype('str')

        df_plan = df_plan.merge(self.df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster', 'hub_name']])

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

            self.root_base(dt, estado, type_of_tourism)
            df_out_base    = self.base(oyo_id, nota, price, cluster)
            df_out_ceiling = self.ceiling(oyo_id, price)
            df_out_floor   = self.floor(df_out_base, oyo_id, nota, cluster)

            df_out_base.to_excel('files/Base_' + oyo_id + '.xlsx', index = False)
            df_out_ceiling.to_excel('files/Ceiling_' + oyo_id + '.xlsx', index = False)
            df_out_floor.to_excel('files/Floor_' + oyo_id + '.xlsx', index = False)

            f = [ 'Base_' + oyo_id + '.xlsx'
                , 'Ceiling_' + oyo_id + '.xlsx'
                , 'Floor_' + oyo_id + '.xlsx'
                ]

            hubs.append(submit_file(f, hub_name))

            #msg = create_message( sender       = 'me'
            #                    , to           = 'marcoantonio.bonaichi@oyorooms.com'
            #                    , subject      = 'GO LIVE - ' + oyo_id + ' - pricing update'
            #                    , message_text = "Hello team,\nplease update base, floor and ceiling prices according to attached files.\nBest regards."
            #                    , files        = f
            #                    )

            #send_message(service, "me", msg)

        df_plan['folder'] = hubs
        
        html = '''<h1 style="font-family:arial">Propriedades enviadas:</h1>
                  <table style="font-family:arial;border:none" border=0>'''
                  
        html += '''<tr>
                     <th>CRS ID</th>
                     <th>Data de envio</th>
                     <th>Google Drive</th>
                   </tr>'''

        for i in range(len(df_plan)):
            
            html += '<tr><td style="width:150px">• <b>' +df_plan.iloc[i,0] + '</b></td><td  style="width:200px">'+ datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '</td><td>' + df_plan.iloc[i,7] + '</td></tr>' 

        html += '</table>'            
        return html
    
    def render_base(self, args):
    
        oyo_id = str(args.get('id'))
        price  = float(args.getlist('preco')[0])
        nota   = float(args.getlist('nota')[0])
    
        df_plan = self.df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][self.df['CRS ID'] == oyo_id]
    
        dt              = df_plan['Planned live date'].values[0]
        estado          = df_plan['UF'].values[0]
        type_of_tourism = df_plan['Type of tourism'].values[0]
        cluster         = df_plan['Cluster'].values[0]
        
        self.root_base(dt, estado, type_of_tourism)
    
        df_out_base    = self.base(oyo_id, nota, price, cluster)
    
        return df_out_base.to_dict()

    def render_ceiling(self, args):

        oyo_id = str(args.get('id'))
        price  = float(args.getlist('preco')[0])
    
        df_plan         = self.df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][self.df['CRS ID'] == oyo_id]
        dt              = df_plan['Planned live date'].values[0]
        estado          = df_plan['UF'].values[0]
        type_of_tourism = df_plan['Type of tourism'].values[0]
        
        self.root_base(dt, estado, type_of_tourism)
    
        df_out_ceiling = self.ceiling(oyo_id, price)
    
        return df_out_ceiling.to_dict()
    
    def render_floor(self, args):
        oyo_id = str(args.get('id'))
        price  = float(args.getlist('preco')[0])
        nota   = float(args.getlist('nota')[0])
    
        df_plan = self.df[['CRS ID', 'Planned live date', 'UF', 'Type of tourism', 'Cluster']][self.df['CRS ID'] == oyo_id]
        dt              = df_plan['Planned live date'].values[0]
        estado          = df_plan['UF'].values[0]
        type_of_tourism = df_plan['Type of tourism'].values[0]
        cluster         = df_plan['Cluster'].values[0]
    
        self.root_base(dt, estado, type_of_tourism)
    
        df_out_base    = self.base(oyo_id, nota, price, cluster)
        df_out_floor   = self.floor(df_out_base, oyo_id, nota, cluster)
    
        return df_out_floor.to_dict()

        
    def __init__(self):
        super().__init__()
    
