from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
import json
import unidecode
import datetime
from math import floor

token = 'EAACEdEose0cBAGZC66LRbFLJFjwrd2ky2DXw46UzhZCwceZBBjCjGGrnB3WwiSrClft5l11z1Qa4V8kcVBywHoFuztvFxZCfc9HD3qbTw1UZBPVjbhNcZBhNRrxeQEYHWGNQq1dciKZBLtndNhcZBCWgVRnWsrspF6DeWuGZA46toBYBfNZAS19lhTEFzN2O0ZAZBJpX4VgbYrIOLQZDZD'
path = "/connecter/"
bookmark_dict = {}

def strnorm(inname):
    outname = unidecode.unidecode(inname.lower())
    return outname

def getnum(reqget, agebound):
    if agebound in reqget:
        numtemp = reqget.get(agebound)
        if numtemp:
            try:
                agenum = int(numtemp)
                return agenum
            except TypeError:
                return None
        return None

def getage(indob):
    now = datetime.datetime.now()
    dob = datetime.datetime.strptime(datetime.datetime.strptime(indob, '%m/%d/%Y').strftime('%Y/%m/%d'), '%Y/%m/%d')
    age = floor(((now - dob).days) / 365)
    return age

def errormsg(msg):
    return '<p style="color: red">' + msg +'</p>\n'

def pageheader():
    output = '\
        <!DOCTYPE html>\n\
        <html lang="en">\n\
        <head>\n\
            <link href="https://fonts.googleapis.com/css?family=Raleway|Roboto+Condensed|Ubuntu" rel="stylesheet">\n\
            <meta charset="UTF-8">\n\
            <link rel="shortcut icon" href="https://s3.eu-west-2.amazonaws.com/connecter/Favicon.ico" type="image/x-icon">\n\
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
                table.center{\n\
                    margin-left:auto; \n\
                    margin-right:auto; \n\
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
    any_checked = ''
    male_checked = ''
    female_checked = ''

    error = request.GET.get("error")
    output = pageheader()
    gender = request.GET.get('gender')
    max_age = request.GET.get('max_age')
    min_age = request.GET.get('min_age')

    if not gender or gender == 'any':
        any_checked = 'checked'
    else:
        if gender == 'male':
            male_checked = 'checked'
        else:
            female_checked = 'checked'
    if max_age:
        max_age = str(max_age)
    else:
        max_age = ''

    if min_age:
        min_age = str(min_age)
    else:
        min_age = ''

    output += '<div class="w3-row">\n\
                  <div class="w3-blue-grey w3-container w3-center" style="height:1080px">\n\
                    <div class="w3-padding-64">\n\
                      <h1>Connecter</h1>\n\
                         <img src="https://s3.eu-west-2.amazonaws.com/connecter/Logo_Design.png" style="width:50%">\n\
                    </div>\n\
                    <div class="w3-padding-64">\n\
                      <p>Welcome to Connecter, the website for all your prospective employee research needs.</p>\n'
    if error == "emptystring":
        output += errormsg('No name was input to the field, please try again')
    output += '<p>Please enter the name of the prospective employee you would like to learn more about.</p>\n\
                        <form action="list_of_names" method="GET">\n\
                            <input type="text" name="search" placeholder="Search..." requried maxlength=30 ><br>\n\
                            <table class="center" border="1">\n\
                                <tr>\n\
                                    <th>\n\
                                        <p>Gender</p>\n\
                                        <form>\n\
                                            <input type = "radio" name = "gender" value = "any" ' + any_checked +'> Any <br>\n\
                                            <input type = "radio" name = "gender" value = "male" ' + male_checked +'> Male <br>\n\
                                            <input type = "radio" name = "gender" value = "female" ' + female_checked +'> Female<br>\n\
                                        </form >\n\
                                    </th>\n\
                                    <th>\n\
                                        <p>Minimum age</p>\n\
                                        <input type="number" name="min_age" min="18" value="' + min_age + '">\n\
                                    </th>\n\
                                    <th>\n\
                                        <p>Maximum age</p>\n\
                                        <input type="number" name="max_age" min="18" value="' + max_age + '">\n\
                                    </th>\n\
                                </tr>\n\
                            </table>\n\
                            <input type="submit" value="Submit">\n\
                        </form>\n\
                        <p><a href = "' + path + 'bookmarks">Bookmarks</a></p>\n\
                    </div>\n\
                  </div>\n\
                </div>\n'
    output += pagefooter()
    return HttpResponse(output)


def list_of_names(request):
    restriction = ''
    empty_list = ''
    result_num = 0
    search_exp = request.GET.get('search')
    gender = request.GET.get('gender')

    max_age = getnum(request.GET, 'max_age')
    min_age = getnum(request.GET, 'min_age')

    search_exp = search_exp[:30]
    search_words = search_exp.split()
    normal_search_words = [(strnorm(word)) for word in search_words]
    fbresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.5/me?fields=friends%7Bgender%2Cbirthday%2Cfirst_name%2Clast_name%7D&access_token=' + token).read()
    fbresp = json.loads(fbresp_str.decode('utf-8'))
    frdata = fbresp['friends']['data']
    search_return = '<a href="' + path + '?search='+ search_exp + '&gender=' + gender + '&min_age=' + str(min_age) + '&max_age=' + str(max_age) + '">Return to Index Page</a>'
    results = ''

    # Main search logic starts here
    for fr in frdata:
        nml = strnorm(fr['last_name'])
        nmf = strnorm(fr['first_name'])

        matched_name = False
        if search_exp:
            for qs in normal_search_words:
                if nml.find(qs) > -1 or nmf.find(qs) > -1:
                    matched_name = True
        else:
            matched_name = True

        matched_gender = False
        if gender != "any":
            if 'gender' in fr:
                fr_gender = fr['gender']
                if fr_gender:
                    if fr_gender == gender:
                        matched_gender = True
        else:
            matched_gender = True

        matched_age = False
        if 'birthday' in fr:
            age = getage(fr['birthday'])
            if min_age:
                if max_age:
                    matched_age = min_age <= age <= max_age
                else:
                    matched_age = min_age < age
            else:
                if max_age:
                    matched_age = age < max_age
                else:
                    matched_age = True

        if matched_name and matched_age and matched_gender:
            results += '<a href="results?id=' + fr['id'] + '">' + fr['last_name'] + ', ' + fr['first_name'] + '<a><br>'
            result_num += 1

    # Generating output
    output = pageheader() + pagetop()
    if result_num > 20:
        restriction =  '<p>Your returned list is over 20 individuals long, please click on the link to refine your search</p>\n\
                        ' + search_return
    if result_num == 0:
        output += '<div class="w3-row">\n\
                    <div class="w3-black w3-container w3-center" style="height:1080px">\n\
                        <div class="w3-padding-64">\n\
                            <h1>There are no users matching your search, please try again</h1>\n ' +\
                        search_return +\
                        '</div>\n\
                    </div>\n\
                </div>'
    else:
        output +=   '<div class="w3-row">\n\
                        <div class="w3-black w3-container w3-center" style="height:1080px">\n\
                            <div class="w3-padding-64">\n\
                                <h1>Search Results</h1>\n' +\
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
        age = getage(dob)

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

    if user_id in bookmark_dict:
        action = '<a href="bookmarks?key=' + user_id + '">Unbookmark profile</a>'
    else:
        action = '<a href="bookmarks?id=' + user_id + '&name=' + name + '&action=' + 'unbookmark' + '">Bookmark profile</a>'

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
                        '<br><br>' + action +'\n\
                    </div>\n\
            </div>\n\
        </td>\n\
        <td align="center" valign="top" style="background-color:black; color:white">\n\
            <div class="w3-padding-8">\n\
                <p class="important_text">Age</p>\n' +\
                    str(age) +\
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

def bookmarks(request):
    output = pageheader() + pagetop()
    results = "You have no bookmarked individuals"
    key = request.GET.get('key')
    if key and key in bookmark_dict:
        del bookmark_dict[key]
    bookmark_name = ""
    bookmark_id = ""
    name = request.GET.get('name')
    id = request.GET.get('id')
    if name:
        bookmark_name = name
    if id:
        bookmark_id = id
    if name and id:
        bookmark_dict[bookmark_id] = bookmark_name
    if bool(bookmark_dict) == True:
        results = ""
        for bookmark in bookmark_dict.keys():
            results += '<a href="results?id=' + bookmark + '">' +  str(bookmark_dict[bookmark]) +'<a>\
            <a href="bookmarks?key=' + bookmark + '">X<a><br>'


    output += ' <div class="w3-row">\n\
                    <div class="w3-black w3-container w3-center" style="height:1080px">\n\
                        <div class="w3-padding-64">\n\
                            <h1>Your bookmarks</h1><br><br>\n' + \
                            results + \
                        '</div>\n\
                    </div>\n\
                </div>'

    return HttpResponse(output)