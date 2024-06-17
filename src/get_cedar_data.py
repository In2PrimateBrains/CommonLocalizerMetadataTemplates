import requests
from urllib.parse import quote
import json
import os
from dotenv import load_dotenv

load_dotenv('.env')

class CEDARAPIHandler:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip('/') + '/'
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'apiKey {api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def get_folder_contents(self, folder_id_url, resource_types=None, version='all', publication_status='all', sort='name', limit=100):
        folder_id = quote(folder_id_url, safe='')
        url = f'{self.base_url}folders/{folder_id}/contents'
        params = {
            'resource_types': ','.join(resource_types) if resource_types else None,
            'version': version,
            'publication_status': publication_status,
            'sort': sort,
            'limit': limit
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = self.session.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def fetch_and_save_resource(self, resource_id, resource_type):
        if resource_type in ['element', 'instance', 'template']:
            endpoint_map = {
                'element': 'template-elements',
                'instance': 'template-instances',
                'template': 'templates'
            }
            url = f'{self.base_url}{endpoint_map[resource_type]}/{quote(resource_id, safe="")}'
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
        return None

    def save_to_file(self, data, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

def process_folder(cedar_api_handler, folder_id_url, path_prefix):
    folder_contents = cedar_api_handler.get_folder_contents(folder_id_url)
    for resource in folder_contents["resources"]:
        resource_type = resource["resourceType"]
        if resource_type == "folder":
            new_path_prefix = os.path.join(path_prefix, resource["schema:name"])
            process_folder(cedar_api_handler, resource["@id"], new_path_prefix)
        else:
            resource_data = cedar_api_handler.fetch_and_save_resource(resource["@id"], resource_type)
            if resource_data:
                file_path = os.path.join(path_prefix, f'{resource["schema:name"]}.json')
                cedar_api_handler.save_to_file(resource_data, file_path)

def main():
    api_key = os.getenv('CEDAR_API_KEY')
    base_url = 'https://resource.metadatacenter.org/'
    folder_id_url = os.getenv('CEDAR_FOLDER_ID_URL')
    download_directory = os.getenv('CEDAR_DOWNLOAD_DIRECTORY')
    
    cedar_api_handler = CEDARAPIHandler(base_url, api_key)
    process_folder(cedar_api_handler, folder_id_url, download_directory)

if __name__ == '__main__':
    main()
