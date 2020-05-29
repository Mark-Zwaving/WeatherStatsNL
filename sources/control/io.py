# -*- coding: utf-8 -*-
'''Functions for creating, writing, deleting a file'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, math, time, os
import view.log as log
from pathlib import Path

def check(file_name):
    '''Function checks a file'''
    ok = False
    try:
        path = Path(file_name)  # Python 3.4
        if Path(path).exists():  # Check if is there file
            log.console(f'Check file {file_name} succesful')
            ok = True
        else:
            raise ValueError( f'File {file_name} does not exist' )
    except ValueError as e:
        log.console(f'Check file {file_name} failed\n{e}')

    return ok

def write(file_name='dummy.txt', content='', prefix='w', encoding='utf-8'):
    '''Function writes or makes a file'''
    ok = False
    try:
        with open( file_name, prefix, encoding=encoding ) as file_out:
            file_out.write(content)
    except Exception as e:
        log.console(f"Create/Write file: {file_name} failed\n{e}")
    else:
        log.console(f"Create/Write file: {file_name} succesful")
        ok = True

    return ok

def save(file_name='dummy.txt', content='', prefix='w', encoding='utf-8'):
    return write(file_name, content, prefix, encoding )

def create(file_name, encoding='utf-8'):
    '''Function create a file if not exists'''
    ok = False
    if check(file_name): # Check if there is a file
        ok = write(file_name, encoding=encoding)
    else:
        log.console(f"File: {file_name} already exists")

    return ok

def read(file_name):
    '''Reads data content from a file'''
    ok, txt = False, ''
    if check(file_name):
        try:
            with open(file_name, 'r') as f:
                txt = f.read()
        except Exception as e:
            log.console(f"Read file: {file_name} failed\n{e}")
        else:
            log.console(f"Read file: {file_name} succesful")
            ok = True

    return ok, txt

def delete(file_name):
    '''Function deletes a file if exists'''
    ok = False
    if check(file_name):
        try:
            Path(file_name).unlink()  # Remove file
        except Exception as e:
            log.console(f"Delete file: {file_name} failed\n{e}")
        else:
            log.console(f"Delete file: {file_name} succesful")
            ok = True

    return ok
