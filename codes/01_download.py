from io import BytesIO
import os
import zipfile

import requests

downloads = [{"url": "https://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2019.zip", "dest_folder": "2019"},
             {"url": "https://download.inep.gov.br/microdados/Enade_Microdados/microdados_enade_2018.zip", "dest_folder": ""},
             {"url": "https://download.inep.gov.br/microdados/Enade_Microdados/microdados_Enade_2017_portal_2018.10.09.zip", "dest_folder": "2017"}]

def download_file(url, dest_folder):
    dest_path = "../microdados/" + dest_folder
    os.makedirs(dest_path, exist_ok=True)

    r = requests.get(url)
    z = zipfile.ZipFile(BytesIO(r.content))
    z.extractall(dest_path)

for download in downloads:
    download_file(download["url"], download["dest_folder"])