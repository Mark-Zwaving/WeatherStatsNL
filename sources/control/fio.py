# -*- coding: utf-8 -*-
'''Functions for creating, writing, deleting, downloaden, unzipping a file'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.7"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import threading, urllib, requests, json, math, time, os, threading
import sources.view.log as log
import sources.model.utils as utils
import sources.view.translate as tr
from pathlib import Path
from zipfile import ZipFile

def check(fname):
    '''Function checks a file for existence'''
    ok = False
    log.console(f'Check: {fname}')

    try:
        path = Path(fname)  # Python 3.4
        if Path(path).exists():  # Check if is there file
            ok = True
        else:
            raise ValueError( f'File does not exist' )
    except ValueError as e:
        log.console(f'Check failed.\nError {e}')
    except Exception as e:
        log.console(f'Check failed.\nError {e}')
    else:
        log.console(f'Check success.')

    return ok

def write(fname='dummy.txt', content='', prefix='w', encoding='utf-8'):
    '''Function writes or makes a file'''
    ok = False
    log.console(f'Write: {fname}')

    try:
        with open( fname, prefix, encoding=encoding ) as f:
            f.write(content)
    except Exception as e:
        log.console(f'Write failed.\nError {e}')
    else:
        log.console(f'Write success.')
        ok = True

    return ok

def save(fname='dummy.txt', content='', prefix='w', encoding='utf-8'):
    ok = write(fname, content, prefix, encoding )
    return ok

def read(fname):
    '''Reads data content from a file'''
    ok = False
    t  = ''
    log.console(f'Read: {fname}')

    if check(fname):
        try:
            with open(fname, 'r') as f:
                t = f.read()
        except Exception as e:
            log.console(f'Read failed.\nError {e}')
        else:
            log.console(f'Read success.')
            ok = True

    return ok, t

def delete(fname):
    '''Function deletes a file if exists'''
    ok = False
    log.console(f'Delete: {fname}')
    if check(fname):
        try:
            Path(fname).unlink()  # Remove file
        except Exception as e:
            log.console(f'Delete failed.\nError {e}')
        else:
            log.console(f'Delete succes.')
            ok = True
    else:
        log.console(f'Delete failed. File does not exist')


    return ok

def unzip( zip, txt ):
    ok = False
    log.console(f'Unzip: {zip}')
    log.console(f'To: {txt}') # TODO force to txt file

    with threading.Lock():
        try:
            dir = os.path.dirname(txt)
            with ZipFile(zip, 'r') as z:
                z.extractall(dir)
        except Exception as e:
            log.console(tr.txt('Unzip failed.') + f'\nError {e}')
        else:
            log.console(f'Unzip success.')
            ok = True

    return ok

def download( url, file ):
    ok = False
    log.console(f'Download: {url}')
    log.console(f'To: {file}')

    with threading.Lock():
        try:
            urllib.request.urlretrieve( url, file )
        except Exception as e:
            log.console(f'Download failed.\nError: {e}')
        else:
            log.console(f'Download success.')
            ok = True

    return ok

def request( url, type='txt'):
    '''Function makes the request based on the url given as parameter
       The return values are: ok, True if success else False... And the text From
       the request.'''
    ok, t = False, ''
    log.console(f'Request: {url}')

    with threading.Lock():
        try:
            resp = urllib.request.urlopen( url )
            data = resp.read()
            if type == 'text':
                t = data
            elif type == 'json':
                t = json.loads(data)
        except Exception as e:
            log.console(f'Request failed.\nError: {e}')
        else:
            log.console(f'Request success.')
            ok = True

    return ok, t

def request_text( url ):
    return request( url, 'txt')

def request_json( url ):
    return request( url, 'json')
