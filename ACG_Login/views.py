from django.shortcuts import render
from django.http import HttpResponse

import hashlib
import urllib.request 
import json
from django.template.context_processors import request

def home(request, *args, **kwargs):
    return render(request, "home.html", {})

def get_hashed_vault_creds():
    url = "https://erminkreponic1c.mylabserver.com/v1/our-auth/creds"
    hdr = { 'X-Vault-Token' : 's.eKAC2vSW0rhGb8HXFwvWSjRY' }
    
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    my_json = json.loads(response.read()) #.decode('utf8')
    creds = []
    for key, value in my_json['data'].items():
        creds.append(key)
        creds.append(value)
        

    # return hashlib.sha256((creds[0] + creds[1]).encode()).hexdigest()
    return creds 
    

def acg_login_view(request, *args, **kwargs):
    
    credsHash = hashlib.sha256((request.POST['InputEmail'] + request.POST['InputPassword']).encode()).hexdigest()
    print("credsHash: ", credsHash)
    print("vaultHash: ", get_hashed_vault_creds()[1])
    
    if get_hashed_vault_creds()[1] == credsHash:
        return HttpResponse('Authorized', status=200)
    else:
        return HttpResponse('Unauthorized', status=401)
    
    
def get_token():
    url = "https://erminkreponic1c.mylabserver.com/v1/api-keys/api-01"
    hdr = { 'X-Vault-Token' : 's.svodbkb0WV3GyIEHqIXez6AG' }
    
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    my_json = json.loads(response.read()) #.decode('utf8')
    creds = []
    for key, value in my_json['data'].items():
        creds.append(key)
        creds.append(value)

    return value 

def api_auth_test(request, *args, **kwargs):
    print("REQUEST: ", request.headers['Auth-Token'])
    print("GET_TOKEN: ", get_token())
    
    if request.headers['Auth-Token'] == get_token():
        return HttpResponse("IT WORKS")
    else:
        return HttpResponse('Unauthorized', status=401)
