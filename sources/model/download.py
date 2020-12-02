# -*- coding: utf-8 -*-
'''Download functions'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import threading, view.log as log, urllib, model.utils as utils

# Download file
def file( url, file ):
    ok = False
    log.console(f'Download from url: {url}', True)
    log.console(f'To file: {file}', True)

    with threading.Lock():
        try:
            f = urllib.request.urlopen(url)
            data = f.read()
            t = utils.b_ascii_to_s( data )
            with open(file, 'w') as loc:
                loc.write(t)
        except Exception as e:
            log.console(f'Download failed.\nError: {e}', True)
        else:
            log.console(f'Download succes.\n', True)
            ok = True

    return ok
