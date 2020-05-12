# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 10:55:49 2020

@author: Bruger
"""
import sys

def ToServer(message):
    print(message, file=sys.stdout, flush=True)
    
def HardCodedForDefault():
    while True:
        ToServer('Move(W);Move(E)')
        server_messages=sys.stdin
        response=server_messages.readline().rstrip()
        ToServer('#'+str(response))
        if(response[0]!='t'):
            break
                       
    ToServer('NoOp;Move(N)')
    server_messages=sys.stdin
    response=server_messages.readline().rstrip()
    ToServer('#'+str(response))   
    ToServer('NoOp;Move(N)')
    server_messages=sys.stdin
    response=server_messages.readline().rstrip()
    ToServer('#'+str(response))     
                   
    while True:
        ToServer('NoOp;Move(W)')
        server_messages=sys.stdin
        response=server_messages.readline().rstrip()
        ToServer('#'+str(response)) 
        if(response[5]!='t'):
            break    
            
    ToServer('NoOp;Push(S,S)')
    server_messages=sys.stdin
    response=server_messages.readline().rstrip()
    ToServer('#'+str(response)) 
               
    while True:
        ToServer('Move(S);NoOp')
        server_messages=sys.stdin
        response=server_messages.readline().rstrip()
        ToServer('#'+str(response)) 
        if(response[0]!='t'):
            break
        
    while True:
        ToServer('Move(E);NoOp')
        server_messages=sys.stdin
        response=server_messages.readline().rstrip()
        ToServer('#'+str(response)) 
        if(response[0]!='t'):
            break
            
    ToServer('Push(N,N);NoOp')
    server_messages=sys.stdin
    response=server_messages.readline().rstrip()
    ToServer('#'+str(response)) 