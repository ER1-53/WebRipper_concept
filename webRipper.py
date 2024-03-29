#!/usr/bin/python3

import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

arg = sys.argv[1]

def download_jpg(url, chemin_sauvegarde, depth=1, pathcount=0):

    if pathcount == 0:
        base_name = os.path.basename(url) 
        pathname, ext = os.path.splitext(base_name)
        shortName = pathname
        print(os.path)
        print(base_name)
        print(len(pathname))
        if len(pathname) > 3:
            shortName = pathname[-3:]
        elif len(pathname) < 3:
            path = os.path.dirname(url) 
            newPath = os.path.basename(path)
            shortName = f'{newPath[:1]}/{newPath[-3:]}'
            print(shortName)
        chemin_sauvegarde = chemin_sauvegarde + pathname 
        pathcount = pathcount + 1

    

    if depth < 0:
        return
    if not os.path.exists(chemin_sauvegarde):
        os.makedirs(chemin_sauvegarde)

    response = requests.get(url)
    page = BeautifulSoup(response.text, 'lxml')
    body = page.body
    if body is None:
        return
    img_tags = body.find_all('img')
    
    for img in img_tags:
        img_url = img.attrs.get('src')
        print(f'IMPRIME URL IMG : {img_url}')
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
    
        if '.jpg' in img_url and shortName in img_url:
            file_name = os.path.join(chemin_sauvegarde, os.path.basename(img_url))
            if os.path.exists(file_name):
                continue
            with open(file_name, 'wb') as f:
                f.write(requests.get(img_url).content)
                print("j'ai imprimer avec src")

    for img in img_tags:
        img_url = img.attrs.get('data-src')
        print(f'IMPRIME URL IMG : {img_url}')
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
    
        if '.jpg' in img_url and shortName in img_url:
            file_name = os.path.join(chemin_sauvegarde, os.path.basename(img_url))
            if os.path.exists(file_name):
                continue
            with open(file_name, 'wb') as f:
                f.write(requests.get(img_url).content)
                print("j'ai imprimer avec data-src")

    print(not any('.jpg' in (img.attrs.get('data-src') if img.attrs.get('data-src') else img.attrs.get('src')) for img in img_tags))
    if depth > 0 and not any('.jpg' in (img.attrs.get('data-src') if img.attrs.get('data-src') else img.attrs.get('src')) for img in img_tags):
        link_tags = body.find_all('a')
        if link_tags:
            print(f'IMPRIME LINK TAG : {link_tags} END')
            count = 0
            for link_tag in link_tags:
                link_url = link_tag.attrs.get('href')
                if link_url:
                    print(f'je suis pathname {type(pathname)}')
                    if len(pathname) < 3 or isinstance(int(pathname), int) :
                        return
                    print(f'IMPRIME LINK URL 1 : {link_url} END')
                    link_url = urljoin(url, link_url)
                    if count > 1:
                        if name:
                            pass
                        else:
                            base_name = os.path.basename(url) 
                            name, ext = os.path.splitext(base_name)
                            if len(name) > 3:
                                name = name[-3:]
                            elif len(name) < 3:
                                path = os.path.dirname(url) 
                                name = os.path.basename(path)
                                
                    else :
                        base_name = os.path.basename(url) 
                        name, ext = os.path.splitext(base_name)
                        count = count + 1
                        if len(name) > 3:
                            name = name[-3:]
                        elif len(name) < 3:
                                path = os.path.dirname(url) 
                                name = os.path.basename(path)
                                

                    print(f'IMPRIME LINK URL 2 : {link_url} END')
                    print(f'IMPRIME NAME : {name} END')
                    if name in link_url and link_url != url:
                        print(f'IMPRIME NAME : {name} END')
                        print(f'IMPRIME LINK URL 3 : {link_url} END')
                        print(f'IMPRIME URL : {url} END')
                        download_jpg(link_url, chemin_sauvegarde, depth-1, pathcount)
                    

                    

# Utilisation de la fonction
url = arg  # Remplacez par l'URL de votre choix
chemin_sauvegarde = './images/'
profondeur = 100  # Remplacez par la profondeur de votre choix
download_jpg(url, chemin_sauvegarde, profondeur)

"""import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_short_name(url):
    base_name = os.path.basename(url) 
    pathname, ext = os.path.splitext(base_name)
    if len(pathname) > 3:
        return pathname[-3:]
    elif len(pathname) < 3:
        path = os.path.dirname(url) 
        newPath = os.path.basename(path)
        return f'{newPath[:1]}/{newPath[-3:]}'
    return pathname

def download_image(img_url, chemin_sauvegarde):
    file_name = os.path.join(chemin_sauvegarde, os.path.basename(img_url))
    if os.path.exists(file_name):
        return
    with open(file_name, 'wb') as f:
        f.write(requests.get(img_url).content)

def download_jpg(url, chemin_sauvegarde, depth=1):
    if depth < 0:
        return
    if not os.path.exists(chemin_sauvegarde):
        os.makedirs(chemin_sauvegarde)

    response = requests.get(url)
    page = BeautifulSoup(response.text, 'lxml')
    body = page.body
    if body is None:
        return
    img_tags = body.find_all('img')
    shortName = get_short_name(url)
    
    for img in img_tags:
        img_url = img.attrs.get('src') or img.attrs.get('data-src')
        if img_url and '.jpg' in img_url:
            img_url = urljoin(url, img_url)
            if shortName in img_url:
                download_image(img_url, chemin_sauvegarde)

    if depth > 0 and not any('.jpg' in (img.attrs.get('src') or img.attrs.get('data-src')) for img in img_tags):
        for link_tag in body.find_all('a'):
            link_url = link_tag.attrs.get('href')
            if link_url:
                link_url = urljoin(url, link_url)
                download_jpg(link_url, chemin_sauvegarde, depth-1)

# Utilisation de la fonction
url = sys.argv[1]
chemin_sauvegarde = './images/'
profondeur = 100
download_jpg(url, chemin_sauvegarde, profondeur)"""
