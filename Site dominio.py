import os
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

# Escopos necessários para acessar a API do Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

# Imprimir o diretório de trabalho atual
print("Diretório de trabalho atual:", os.getcwd())

# Carregar as credenciais do arquivo credentials.json
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Imprimir o caminho absoluto do arquivo credentials.json
        print(os.path.abspath('credentials.json'))
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Criar o serviço da API do Google Drive
drive_service = build('drive', 'v3', credentials=creds)

# IDs das pastas e arquivos no Google Drive (igual ao anterior)

# Nome da pasta de saída no Google Drive
output_folder_name = 'catalogo_olympikus'

# Procurar a pasta de saída no Google Drive
results = drive_service.files().list(
    q=f"name = '{output_folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
    fields="nextPageToken, files(id)").execute()
items = results.get('files', [])

if not items:
    # Criar a pasta de saída se ela não existir
    file_metadata = {
        'name': output_folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    output_folder_id = file.get('id')
    print(f'Pasta de saída criada no Google Drive com ID: {output_folder_id}')
else:
    # Usar o ID da pasta existente
    output_folder_id = items[0]['id']
    print(f'Pasta de saída encontrada no Google Drive com ID: {output_folder_id}')

# ... (restante do código - igual ao anterior, mas usando output_folder_id
# para salvar os arquivos HTML na pasta correta) ...