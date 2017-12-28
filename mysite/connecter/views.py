from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import json
import unidecode

# Create your views here.

users = {'1':'Szilard','2':'Mariann','3':'Albert'}
token = 'EAACEdEose0cBAL8yP4pFJy8zPzwhNlAr65CqKqSd1nbZAiwCtZCvqRME1AV9ZA7aZAMLao4Yp4Xvb8prVs3QqZCewnkBukfgrAsWrzMVti8YWG4B4OoQVTwHnzNZCUXgjHn7WUROpW6ZACmy9PuDAyDvpYSt7DbLVJbGCNKGnKZAY7A1w2PZBDNERqZA4ZAuNLuZCEZC2eI3PPZBrJlAZDZD'

def index(request):
    output = '<html>\
            <head>\
            <title>Connecter</title>\
            </head>\
                    <body>\
                    <p>Hello, world</p><ul>'
    for id,name in users.items():
        output += '<li><a href="show_user?id=' + id + '">' + name + '</a></li>'
    output += '</ul></body>\
                    </html>';
    return HttpResponse(output)

def show_user(request):
    return HttpResponse('Hello ' + users[request.GET.get('id')])

def strnorm(inname):
    outname = unidecode.unidecode(inname.lower())
    return outname

def get_fb(request):
    qs = 'o'

    fbresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.11/me?fields=id%2Cname%2Cfriends%7Bfirst_name%2Clast_name%2Cid%7D&access_token=' + token).read()
    fbresp = json.loads(fbresp_str.decode('utf-8'))
    friends = fbresp['friends']
    frdata = friends['data']
    output = '<html>\
            <head>\
            <title>Connecter</title>\
            </head>\
            <body>\
            <ul>'
    for fr in frdata:
        nml = strnorm(fr['last_name'])
        nmf = strnorm(fr['first_name'])
        if nml.find(qs) > -1  or nmf.find(qs) > -1:
            output += '<li><a href="show_fr?id=' + fr['id'] + '">' + fr['last_name'] + ', ' + fr['first_name'] + '<a></li>'
   
    output += '</ul>\
            </body>\
            </html>';

    return HttpResponse(output);
