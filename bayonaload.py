import requests
import re
import os
import sys
import urllib
from urllib.request import urlopen
import zipfile

path = os.getcwd()

all_zips = [item for sublist in [x[2] for x in os.walk(path)][1:] for item in sublist]
valid_zips = []
# De todos los zips que hay, solo nos quedamos con los validos (que se puedan abrir con zipfile.ZipFile)
for file in all_zips:
    folder = file.replace('-','_').split('_part_')[0]
    try:
        zipfile.ZipFile(os.path.join(path, folder, file))
        valid_zips.append(file)
    except:
        pass

url_pagina = 'https://www.3dbuzz.com'
req = requests.get(url_pagina)
# Obtenemos todos los zips
files = re.findall('href="(.*zip)"', req.text)
print('Already exists', len(valid_zips), 'files')
print('Downloading', len(files) - len(valid_zips), 'files, be patient...')
for idx, file in enumerate(files):
    name = file.split('/')[-1]
    # Comprobamos que no exista ya
    if name in valid_zips:
        print('Skipping', name + '.', 'Already exists.')
        continue

    # Creamos la carpeta si no existe ya
    try:
        folder = name.replace('-', '_').split('_part_')[0]
        os.mkdir(os.path.join(path, folder))
        print('Folder', folder, 'created')
    except:
        pass

    print('Downloading file', str(idx+1) + ':', name + '...')
    downloaded = True
    with open(os.path.join(path, folder, name), 'wb') as f:
        try:
            # Bajamos el contenido de la url y lo guardamos en el fichero
            # correspondiente
            f.write(urlopen(file).read())
        except Exception as err:
            print(str(err).replace(':',''))
            downloaded = False
        finally:
            print("File", str(idx+1) + ':', name, end=' ')
            if not downloaded: print('not', end=' ')
            print('downloaded')

        if not downloaded:
            sys.exit(1)