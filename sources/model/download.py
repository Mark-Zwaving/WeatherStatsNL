# -*- coding: utf-8 -*-
'''Download functions'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import threading, view.log as log, urllib, model.utils as utils
import requests, json

# Download file
def file( url, file ):
    ok = False
    log.console(f'Download from url: {url}', True)
    log.console(f'To file: {file}', True)

    with threading.Lock():
        try:
            f = urllib.request.urlopen(url)
            data = f.read()
            t = utils.b_utf8_to_s( data )
            with open(file, 'w') as loc:
                loc.write(t)
        except Exception as e:
            log.console(f'Download failed.\nError: {e}', True)
        else:
            log.console(f'Download succes.', True)
            ok = True

    return ok

def request( url, type='txt'):
    '''Function makes the request based on the url given as parameter
       The return values are: ok, True if succes else False... And the text From
       the request.'''
    ok, t = False, ''

    with threading.Lock():
        try:
            resp = urllib.request.urlopen( url )
            data = resp.read()
            if type == 'text':
                t = data
            elif type == 'json':
                t = json.loads(data)
        except Exception as e:
            log.console(f'Failed request from {url}.\nError: {e}', True)
        else:
            log.console(f'Succesfull request from {url}', True)
            ok = True

    return ok, t

def request_text( url ):
    return request( url, 'txt')

def request_json( url ):
    return request( url, 'json')
