from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import json
import unidecode
import datetime
from math import floor

users = {'1':'Szilard','2':'Mariann','3':'Albert'}
token = 'EAACEdEose0cBANVZBZCoBDNhYeGbJ83kxlZApelD1Xk2eHtDDgP4KzrZBhAP5RxvUiC2gopuwMcb1HZBY6omQwt8DyG8KDfgNHEZB02ucY0lk1LwAKE5uyfqftjeSdan1uWoDZBZBjIpIGrSYMRlOEbM06wp761LchyAIqN5CzBxytgn079CJofzLvgirAMSu6DplY2nee2ZAVQZDZD'
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
            <link href="https://fonts.googleapis.com/css?family=Raleway|Roboto+Condensed|Ubuntu" rel="stylesheet">\n\
            <meta charset="UTF-8">\n\
            <link rel="shortcut icon" href="https://lh4.googleusercontent.com/I_ymSvUYuvWh-rROSsaoRY6NVdL8oCW0F9v_u-2fprB7Z7UPkzM1SalwaP5QTNP4HR4qy1346rMBhSt6m3TX=w1920-h949" type="image/x-icon">\n\
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
                .important_text { \n\
                    font-family: Raleway,sans-serif; \n\
                    font-weight: bold;\n\
                    font-size: 110%;\n\
                }\n\
            </style>\n\
        </head>\n\
        <body class="w3-content" style="max-width:1300px">'

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
                         <img src="https://lh4.googleusercontent.com/cj98H6b1RFwRJrjgK8tFm6WL3Ckbtq9nrblJ5G6b-l-_P2GCekMxsZYQ6WmNH_ay1il7TUyYuNwRVPaNFGcO=w1920-h949-rw" style="width:50%">\n\
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
    fbresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.11/me?fields=id%2Cname%2Cfriends%7Bfirst_name%2Clast_name%2Cid%7D&access_token=' + token).read()
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
    now = datetime.datetime.now()
    work = "N/A"
    results = "N/A"
    education = "N/A"
    location = "N/A"
    email = "N/A"
    age = "N/A"
    name = "N/A"
    quotes = "N/A"
    about = "N/A"
    user_id = request.GET.get('id')

    if not user_id:
        output = page_header() + page_footer()
        output += errormsg('No user id was recieved, search again')
        return HttpResponse(output)


    picresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.5/' + user_id + '/picture?height=200&width=200&redirect=false&access_token=' + token).read()
    picresp = json.loads(picresp_str)
    pic_url = picresp['data']['url']
    fbresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.11/' + user_id + '?fields=birthday%2Cquotes%2Cname%2Ceducation%2Cemail%2Cwork%2Cabout%2Cfriends%2Clocation&access_token=' + token).read()
    fbresp = json.loads(fbresp_str.decode('utf-8'))



    if 'location' in fbresp:
        location = fbresp['location']['name']

    if 'about' in fbresp:
        about = fbresp['about']

    if 'quotes' in fbresp:
        quotes = fbresp['quotes']

    if 'email' in fbresp:
        email = fbresp['email']
    if 'birthday' in fbresp:
        age = ""
        dob = fbresp['birthday']
        dob = datetime.datetime.strptime(datetime.datetime.strptime(dob, '%m/%d/%Y').strftime('%Y/%m/%d'), '%Y/%m/%d')
        age = str(floor(((now - dob).days)/365))

    if 'work' in fbresp:
        work = ""
        for job in fbresp['work']:
            employer = job['employer']
            job_location = job['location']
            if employer:
                work += employer['name']
                if job_location:
                    work += ' (' + job_location['name'] + ')'
                work += '<br>'\

    if 'education' in fbresp:
        education = ""
        for edu in fbresp['education']:
            school = edu['school']
            if school:
                education += school['name'] + '<br>'

    if 'friends' in fbresp:
        results = ""
        frdata = fbresp['friends']['data']
        for fr in frdata:
                results += '<a href="results?id=' + fr['id'] + '">' + fr['name'] +  '<a><br>'

    if 'name' in fbresp:
        name = fbresp['name']

    output = pageheader() + pagetop()
    output += '<table width=1300 style="border-spacing: 0px;"><tr>\n\
        <td width="30%" align="center" valign="top" style="background-color:#607d8b; color:white">\n\
            <div class="w3-padding-64 w3-center">\n\
                <div style="font-family:Raleway,sans-serif; font-size:30px">\n' +\
                    name + \
                '</div>\n\
                    <img src="' + pic_url + '">\n\
                    <div class="w3-left-align w3-padding-large">\n\
                        <p class="important_text"><b>About</b></p>\n' + \
                        about + \
                        '<p class="important_text"><b>Favorite Quotes</b></p>\n' + \
                        quotes + \
                    '</div>\n\
            </div>\n\
        </td>\n\
        <td align="center" valign="top" style="background-color:black; color:white">\n\
            <div class="w3-padding-8">\n\
                <p class="important_text">Age</p>\n' +\
                    age +\
                    '<p class="important_text"><b>Location</b></p>\n' +\
                    location +\
                    '<p class="important_text"><b>Work</b></p>\n' +\
                    work + \
                    '<p class="important_text"><b>Education</b></p>\n' + \
                    education + \
                    '<p class="important_text"><b>E-mail</b></p>\n' + \
                    email + \
                    '<p class="important_text"><b>Friends</b></p>\n'+\
                    results +\
            '</div>\n\
        </td>\n\
        </tr></table>'

    output += pagefooter()
    return HttpResponse(output)
