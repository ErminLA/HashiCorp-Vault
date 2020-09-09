from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

import hashlib
import urllib.request 
import json

def home(request, *args, **kwargs):
    #return HttpResponse("<h1>DOES IT WORK</h1>")
    return render(request, "home.html", {})

def get_hashed_vault_creds():
    url = "https://erminkreponic1c.mylabserver.com/v1/kv-test/test03-kv"
    hdr = { 'X-Vault-Token' : 's.9IzOHb4ybMhUfHeTxmGMrWsd' }
    
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    my_json = json.loads(response.read()) #.decode('utf8')
    creds = []
    for key, value in my_json['data'].items():
        creds.append(key)
        creds.append(value)

    return hashlib.sha256((creds[0] + creds[1]).encode()).hexdigest()

def acg_login_view(request, *args, **kwargs):
    
    credsHash = hashlib.sha256((request.POST['InputEmail'] + request.POST['InputPassword']).encode()).hexdigest()
    if get_hashed_vault_creds() == credsHash:
        return HttpResponse('Authorized', status=200)
    else:
        #raise Http404("Forbiden")
        return HttpResponse('Unauthorized', status=401)
         


