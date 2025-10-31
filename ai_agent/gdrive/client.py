import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

class GDriveClient:
    def __init__(self, credentials_file='credentials.json', token_pickle='token.pickle'):
        self.credentials_file = credentials_file
        self.token_pickle = token_pickle
        self.service = self._get_gdrive_service()

    def _get_gdrive_service(self):
        creds = None
        if os.path.exists(self.token_pickle):
            with open(self.token_pickle, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, ['https://www.googleapis.com/auth/drive.readonly']
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_pickle, 'wb') as token:
                pickle.dump(creds, token)

        return build('drive', 'v3', credentials=creds)

    def list_files(self, page_size=10):
        results = self.service.files().list(
            pageSize=page_size, fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        items = results.get('files', [])
        return items

    def download_file(self, file_id, file_path, mime_type):
        if "google-apps" in mime_type:
            if mime_type == 'application/vnd.google-apps.document':
                request = self.service.files().export_media(fileId=file_id, mimeType='application/pdf')
                file_path += ".pdf"
            elif mime_type == 'application/vnd.google-apps.spreadsheet':
                request = self.service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                file_path += ".xlsx"
            elif mime_type == 'application/vnd.google-apps.presentation':
                request = self.service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                file_path += ".pptx"
            else:
                return None # Unsupported Google Doc type
        else:
            request = self.service.files().get_media(fileId=file_id)

        with open(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
        return file_path
