# -*- coding: utf-8 -*-
"""
Created on Tue May 12 19:55:58 2020

@author: Bruger
"""
import sys

import globals

def HandleError(message):
    if globals.server :
        print(message, file=sys.stderr, flush=True)
    else :
        print('ERROR : '+message)
    sys.exit(1)

def ToServer(message):
    if globals.server :
        print(message, file=sys.stdout, flush=True)
    else :
        print(message)