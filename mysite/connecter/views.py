from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import json
import unidecode

users = {'1':'Szilard','2':'Mariann','3':'Albert'}
token = 'EAACEdEose0cBAL8JaHXzTWZB0113D6vw7ap1Da9S35JSaneqiYiFE4U8h8bZCrVzkwH0C4SiMj5a3gUPPvD4oQ9bSkNlY0wqfAczTtJGYcdl5GJNKoZARsGue5GGxZCUBAv5cxTm4ZBR183260ybwEwLFoRIa9GW45guFg8FqcxRGdhG2Txm6fZAtACgWa8w6ZBbXN8NUp4QAZDZD'
path = "/connecter/"

def strnorm(inname):
    outname = unidecode.unidecode(inname.lower())
    return outname

def errormsg(msg):
    return '<p style="color: red">' + msg +'</p>\n'

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
                input[type=text]:focus {\n\
                    width: 100%;\n\
                }\n\
            </style>\n\
        </head>\n\
        <body class="w3-content" style="max-width:1300px">\n'
    return output


def pagetop():
    output = '<a href="' + path + '">Home Page</a>'
    return output


def pagefooter():
    output = '<footer>\n\
                <p>This website currently only supports Facebook</p>\n\
            </footer>\n\
        </body>\n\
    </html>\n';
    return output


def index(request):
    error = request.GET.get("error")
    output = pageheader()
    output += '<div class="w3-row">\n\
                  <div class="w3-blue-grey w3-container w3-center" style="height:1080px">\n\
                    <div class="w3-padding-64">\n\
                      <h1>Connecter</h1>\n\
                         <img src="Logo_Design.jpg"  style="width:50%">\n\
                    </div>\n\
                    <div class="w3-padding-64">\n\
                      <p>Welcome to Connecter, the website for all your prospective employee research needs.</p>\n'
    if error == "emptystring":
        output += errormsg('No name was input to the field, please try again')
    output += '<p>Please enter the name of the prospective employee you would like to learn more about.</p>\n\
                        <form action="list_of_names" method="GET">\n\
                             <input type="text" name="search" placeholder="Search..." requried maxlength=30 >\n\
                            </form>\n\
                        </form>\n\
                    </div>\n\
                  </div>\n\
                </div>\n'
    output += pagefooter()
    return HttpResponse(output)


def list_of_names(request):
    restriction = ''
    result_num = 0
    search_exp = request.GET.get('search')

    if not search_exp:
        #In case of empty search string, redirect to index page
        output = '\
            <!DOCTYPE html>\n\
            <html lang="en">\n\
                <head>\n\
                    <meta http-equiv="refresh" content="0; URL=' + request.scheme + '://' + request.META.get('HTTP_HOST') + path +'?error=emptystring" />\n\
                </head>\n\
            </html>'
        return HttpResponse(output)

    #Main search logic starts here
    search_exp = search_exp[:30]
    search_words = search_exp.split()
    normal_search_words = [(strnorm(word)) for word in search_words]
    fbresp_str = urllib.request.urlopen(
        'https://graph.facebook.com/v2.11/me?fields=id%2Cname%2Cfriends%7Bfirst_name%2Clast_name%2Cid%7D&access_token=' + token).read()
    fbresp = json.loads(fbresp_str.decode('utf-8'))
    frdata = fbresp['friends']['data']
    results = ''
    for fr in frdata:
        nml = strnorm(fr['last_name'])
        nmf = strnorm(fr['first_name'])
        matched = False
        for qs in normal_search_words:
            if nml.find(qs) > -1 or nmf.find(qs) > -1:
                matched = True
        if matched:
            results += '<a href="results?id=' + fr['id'] + '">' + fr['last_name'] + ', ' + fr['first_name'] + '<a><br>'
            result_num += 1

    #Genetaring output
    output = pageheader() + pagetop()
    if result_num > 20:
        restriction = '<form action="list_of_names" method="GET">\n\
                             <input type="text" name="search" placeholder="Restrict search..." requried maxlength=30 value="' + search_exp + '" >\n'
    output +=   '<div class="w3-row">\n\
                    <div class="w3-black w3-container w3-center" style="height:1080px">\n\
                        <div class="w3-padding-64">\n\
                            <h1>You Searched For "' + search_exp + '"</h1>\n' +\
                            restriction +\
                        '</div>\n\
                        <div class="w3-padding-64">\
                            <p>Please Choose The User You Meant</p>\n' +\
                         results +\
                        '</div>\n\
                    </div>\n\
                </div>'
    output += pagefooter()
    return HttpResponse(output)


def results(request):
    work = "this failed"
    user_id = request.GET.get('id')

    if not user_id:
        output = page_header() + page_footer()
        output += errormsg('No user id was recieved, search again')
        return HttpResponse(output)

    fbresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.11/'+ user_id +'?fields=birthday%2Ceducation%2Cemail%2Cwork%2Cabout%2Cfriends%2Clocation&access_token=' + token).read()
    fbresp = json.loads(fbresp_str.decode('utf-8'))
    #TODO find out how about is stored
    #about = fbresp['about']
    #TODO Find age of user
    #age = fbresp['about']
    location = fbresp['location']['name']
    for job in fbresp['work']:
        if job == "employer":
            work += job['name']
    frdata = fbresp['friends']['data']
    results = ''
    for fr in frdata:
            results += '<a style= "text-decoration:none;" href="results?id=' + fr['id'] + '">' + fr['name'] + ', ' + '<a><br>'

    output = pageheader()
    output += '<div class="w3-row">\n\
                    <div class="w3-half w3-black w3-container w3-center" style="height:1080px">\n\
                        <div class="w3-padding-64">\n\
                            <h1>Name of Person</h1>\n\
                        </div>\n\
                        <div class="w3-padding-64">\n\
                            <p><u>Personal Bio</u></p>\n\
                            <p><u>Age</u></p>\n\
                            <p><u>Location</u></p>\n' +\
                            location +\
                            '<p><u>Work/Education</u></p>\n' +\
                            work +\
                            '<p><u>Friends</u></p>\n'+\
                            results +\
                        '</div>\n\
                    </div>\n\
                    <div class="w3-half w3-blue-grey w3-container" style="height:1080px">\n\
                        <div class="w3-padding-64 w3-center">\n\
                            <h1>Placeholder</h1>\n\
                            <img src="Image Placeholder.jpg"  style="width:50%">\n\
                                <div class="w3-left-align w3-padding-large">\n\
                                    <p>Lorem ipusm sed vitae justo condimentum, porta lectus vitae, ultricies congue gravida diam non fringilla.</p>\n\
                                    <p>Lorem ipusm sed vitae justo condimentum, porta lectus vitae, ultricies congue gravida diam non fringilla.</p>\n\
                                </div>\n\
                            </div>\n\
                        </div>\n\
                    </div>'
    output += pagefooter()
    return HttpResponse(output)
