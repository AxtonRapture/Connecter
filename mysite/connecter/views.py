from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import json
import unidecode

# Create your views here.

users = {'1':'Szilard','2':'Mariann','3':'Albert'}
token = 'EAACEdEose0cBAL8yP4pFJy8zPzwhNlAr65CqKqSd1nbZAiwCtZCvqRME1AV9ZA7aZAMLao4Yp4Xvb8prVs3QqZCewnkBukfgrAsWrzMVti8YWG4B4OoQVTwHnzNZCUXgjHn7WUROpW6ZACmy9PuDAyDvpYSt7DbLVJbGCNKGnKZAY7A1w2PZBDNERqZA4ZAuNLuZCEZC2eI3PPZBrJlAZDZD'

def strnorm(inname):
    outname = unidecode.unidecode(inname.lower())
    return outname

def pageheader():
    output = '\
        <!DOCTYPE html>\n\
        <html lang="en">\n\
        <head>\n\
            <meta charset="UTF-8">\n\
            <link rel="shortcut icon" href="favicon.ico" type="image/x-icon">\n\
            <meta name="viewport" content="width=device-width, initial-scale=1">\n\
            <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n\
            <title>Connecter</title>\n\
            <style>\n\
                input[type=text] {\n\
                    width: 130px;\n\
                    box-sizing: border-box;\n\
                    border: 2px solid #ccc;\n\
                    border-radius: 4px;\n\
                    font-size: 16px;\n\
                    background-color: white;\n\
                    background-image: url(''searchicon.png'');\n\
                    background-position: 10px 10px;\n\
                    background-repeat: no-repeat;\n\
                    padding: 12px 20px 12px 40px;\n\
                    -webkit-transition: width 0.4s ease-in-out;\n\
                    transition: width 0.4s ease-in-out;\n\
                }\n\
    \n\
                input[type=text]:focus {\n\
                    width: 100%;\n\
                }\n\
            </style>\n\
        </head>\n\
        <body class="w3-content" style="max-width:1300px">\n'
    return output

def pagefooter():
    output = '<footer>\n\
                <p>This website currently only supports Facebook</p>\n\
            </footer>\n\
        </body>\n\
    </html>\n';
    return output

def index(request):
    output = pageheader()
    output += '<div class="w3-row">\n\
                  <div class="w3-blue-grey w3-container w3-center" style="height:1080px">\n\
                    <div class="w3-padding-64">\n\
                      <h1>Connecter</h1>\n\
                         <img src="Logo_Design.jpg"  style="width:50%">\n\
                    </div>\n\
                    <div class="w3-padding-64">\n\
                      <p>Welcome to Connecter, the website for all your prospective employee research needs.</p>\n\
                        <p>Please enter the name of the prospective employee you would like to learn more about.</p>\n\
                        <form>\n\
                             <form action="/Main Page.py" method="post">\n\
                             <input type="text" name="search" placeholder="Search..">\n\
                            </form>\n\
                        </form>\n\
                    </div>\n\
                  </div>\n\
                </div>\n'
    output += pagefooter()
    return HttpResponse(output)

def list_of_names(request):
    output = pageheader()
    output += pagefooter()
    return HttpResponse(output)

def results(request):
    output = pageheader()
    output += pagefooter()
    return HttpResponse(output)
    """qs = 'o'

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

    return HttpResponse(output);"""

    """for id,name in users.items():
        output += '<li><a href="show_user?id=' + id + '">' + name + '</a></li>'
    return HttpResponse(output)"""