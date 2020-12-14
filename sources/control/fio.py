# -*- coding: utf-8 -*-
'''Functions for creating, writing, deleting, downloaden, unzipping a file'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import threading, urllib, json, os
import sources.view.console as console
import sources.view.txt as vt
from pathlib import Path
from zipfile import ZipFile

def check(fname):
    '''Function checks a file for existence'''
    ok = False
    console.log(f'Check: {fname}')

    try:
        path = Path(fname)  # Python 3.4
        if path.exists():  # Check if is there file
            ok = True
        else:
            raise ValueError(f'File does not exist')
    except ValueError as e:
        console.log(vt.error('Check', e))
    except Exception as e:
        console.log(vt.error('Check', e))
    else:
        console.log(vt.succes('Check'))

    return ok

def write(fname='dummy.txt', content='', prefix='w', encoding='utf-8'):
    '''Function writes or makes a file'''
    ok = False
    console.log(f'Write: {fname}')

    try:
        with open( fname, prefix, encoding=encoding ) as f:
            f.write(content)
    except Exception as e:
        console.log(vt.error('Write', e))
    else:
        console.log(vt.succes('Write'))
        ok = True

    return ok

def save(fname='dummy.txt', content='', prefix='w', encoding='utf-8'):
    ok = write(fname, content, prefix, encoding )
    return ok

def read(fname):
    '''Reads data content from a file'''
    ok = False
    t  = ''
    console.log(f'Read: {fname}')

    if check(fname):
        try:
            with open(fname, 'r') as f:
                t = f.read()
        except Exception as e:
            console.log(vt.error('Read', e))
        else:
            console.log(vt.succes('Read'))
            ok = True

    return ok, t

def delete(fname):
    '''Function deletes a file if exists'''
    ok = False
    console.log(f'Delete: {fname}')
    if check(fname):
        try:
            Path(fname).unlink()  # Remove file
        except Exception as e:
            console.log(vt.error('Delete', e))
        else:
            console.log(vt.succes('Delete'))
            ok = True
    else:
        console.log(f'Delete cannot. File does not exist')

    return ok

def mk_dir(path):
    '''Function makes a map if not already exists'''
    ok = False
    console.log(f'Make dir: {path}')
    try:
        if os.path.isdir(path):
            console.log('Map not made because it already exists.')
            return True
        else:
            os.mkdir(path)
    except Exception as e:
        console.log(vt.error('Make directory', e))
    else:
        console.log(vt.succes('Make directory'))
        ok = True

    return ok

def unzip( zip, txt ):
    ok = False
    console.log(f'Unzip: {zip}')
    console.log(f'To: {txt}') # TODO force to txt file

    with threading.Lock():
        try:
            dir_txt = os.path.dirname(txt)
            with ZipFile(zip, 'r') as z:
                z.extractall(dir_txt)
        except Exception as e:
            console.log(vt.error('Unzip', e))
        else:
            console.log(vt.succes('Unzip'))
            ok = True

    return ok

def download( url, file ):
    ok = False
    console.log(f'Download: {url}')
    console.log(f'To: {file}')

    with threading.Lock():
        try:
            urllib.request.urlretrieve( url, file )
        except Exception as e:
            console.log(vt.error('Download', e))
        else:
            console.log(vt.succes('Download'))
            ok = True

    return ok

def request( url, type='txt'):
    '''Function makes the request based on the url given as parameter
       The return values are: ok, True if success else False... And the text From
       the request.'''
    ok, t = False, ''
    console.log(f'Request: {url}')

    with threading.Lock():
        try:
            resp = urllib.request.urlopen( url )
            data = resp.read()
            if type == 'text':
                t = data
            elif type == 'json':
                t = json.loads(data)
        except Exception as e:
            console.log(vt.error('Request', e))
        else:
            console.log(vt.succes('Request'))
            ok = True

    return ok, t

def request_text( url ):
    return request( url, 'txt')

def request_json( url ):
    return request( url, 'json')
