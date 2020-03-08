from googleapiclient.discovery import build
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from apiclient.http import MediaFileUpload
import base64
from src.Utils import Utils

class Google:
    
    #######################################
    ## Connecting to the google services ##
    #######################################
    def _auth(self):
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
        self.sheet   = build('sheets', 'v4', credentials = creds).spreadsheets()
        self.gdrive  = build( 'drive', 'v3', credentials = creds)
        self.service = build( 'gmail', 'v1', credentials = creds)
        #######################################

    ##########################
    ## Function: Read sheet ##
    ##########################
    def _read_sheet(self, SPREADSHEET_ID, RANGE, COLUMN_INDEXES, COLUMN_NAMES):
    
        # Get the spreadsheet values
        values = self.sheet.values().get( spreadsheetId = SPREADSHEET_ID
                                        , range         = RANGE
                                        ).execute().get('values', [])

        # Converts to DataFrame
        values = pd.DataFrame(values)[COLUMN_INDEXES]

        # Rename the columns
        values.columns = COLUMN_NAMES
        
        return values
    ##########################
    
    ##############################
    ## Function: create message ##
    ##############################
    ## • Creates the e-mail     ##
    ##############################
    def create_message(self, sender, to, subject, message_text, files):
        
      # Creates the e-mail body
      message = MIMEMultipart()
      #message['to'] = ", ".join(['vinicius.alves@oyorooms.com', 'ana.passos@oyorooms.com'])
      message['to'] = ", ".join(['marcoantonio.bonamichi@oyorooms.com', 'marco.bom.amigo@gmail.com'])
      
      message['from'] = sender
      message['subject'] = subject
      msg = MIMEText(message_text)
      message.attach(msg)
    
      for file in files:
    
          # Get the file path
          file = 'files/' + file
          
          # Get the file type
          #content_type, encoding = mimetypes.guess_type(file)
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
    def send_message(self, service, user_id, message):
        message = (service.users().messages().send(userId = user_id, body = message).execute())
        return message
    ############################

    #######################################
    ## Function: Submit file             ##
    #######################################
    ## • Sends the files to Google Drive ##
    #######################################
    def submit_file(self, files, hub):
    
        # Folder to send the files    
        folder_id = '1ZXcZ7WSTdS8R2XHVACutibn5zWtGJnz5'
    
        folders = self.gdrive.files().list( q        = "mimeType='application/vnd.google-apps.folder' and parents in '"+folder_id+"' and trashed = false"
                                          , fields   = "nextPageToken, files(id, name)"
                                          , pageSize = 400).execute()
        folders = pd.DataFrame(folders['files'])
        
        folder_id   = folders['id'][folders['name'].str.lower().str.startswith(self.utils.punctuation(hub).str.lower().str.replace(' ', '_').values[0])]
        folder_name = folders['name'][folders['name'].str.lower().str.startswith(self.utils.punctuation(hub).str.lower().str.replace(' ', '_').values[0])]
        
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
            self.gdrive.files().create( body       = file_metadata
                                 , media_body = media
                                 , fields     = 'id').execute()
        
        return folder_name
    #######################################

    def __init__(self):
        self._auth()
        self.utils = Utils()
