from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import time

# Scopes and credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
creds_file = 'drive_credentials.json'

# Authentication
flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
creds = flow.run_local_server(port=0)

# Build the Drive service
service = build('drive', 'v3', credentials=creds)

def count_files_in_folder(drive_id, key_text=None, retry=0):
    """ Recursively counts PDF and JPG files within folders containing specific text in the shared drive """
    total_files = 0
    page_token = None
    try:
        while True:
            query = f"name contains '{key_text}' and mimeType='application/vnd.google-apps.folder'" if key_text else None
            results = service.files().list(
                q=query,
                spaces='drive',
                corpora='drive',
                driveId=drive_id,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
                fields='nextPageToken, files(id, mimeType, name)',
                pageToken=page_token
            ).execute()
            items = results.get('files', [])

            for item in items:
                if item['mimeType'] == 'application/vnd.google-apps.folder':
                    # Recurse into the folder
                    total_files += count_files_in_folder(item['id'], key_text)
                elif item['mimeType'] == 'application/pdf' or item['mimeType'] == 'image/jpeg':
                    total_files += 1
                    print(f"Found file: {item['name']}")

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

    except Exception as e:
        if retry < 3:
            time.sleep(5)  # wait before retrying
            return count_files_in_folder(drive_id, key_text, retry+1)
        else:
            raise

    return total_files

drive_id = ''
key_text = '2024'  # Set to '2024' to filter by folders containing '2024' in their name
file_count = count_files_in_folder(drive_id, key_text)  # Start at the root of the shared drive
print(f"Total PDF and JPG files in folders containing '{key_text}': {file_count}")
