from django.shortcuts import render #Library imports
from django.http import HttpResponse
import urllib.request
import json
import unidecode
import datetime
from math import floor

#Access token from the graph API to allow retrieval of user data
token = 'EAACEdEose0cBADkODArPqME1lkTdHhXsFd4CXtpDicfTqD1Dx0UZASl79eziveddbVp0ZA8qdGnIZB7SDkmXZClGHXHbGOZA76maZBZAMdtTuRe3VnR5a0S6FA12YurEZBNfpAV8BD4cs2cGF7YJjulGFarWYrtwdOFpL9Vn9EkYirh814NmbO9tdztszg2ZCfcTNKDi97AUQogZDZD'
#Hard coded pathway for internal directory
path = "/connecter/"
#This dictionary is for the bookmarks the user can make. It is a global variable to maintain its values even after the user leaves the bookmarks page, where it would have been stored temporarily
bookmark_dict = {}

def strnorm(inname): # This function normalises strings by removing all diacritics and converting the strings to lowercase
    outname = unidecode.unidecode(inname.lower())
    return outname # this returns the normalised string to whereever the function was called

def getnum(reqget, agebound): # This function verifies that the name submitted for the criteria is a number,and if it arrives as a string, if the browser dosent support HTML 5, converts it to a integer
    if agebound in reqget: #Checks to see if a variable called age was passed through the request
        numtemp = reqget.get(agebound)
        if numtemp:
            try:
                agenum = int(numtemp)#tries to convert the input age to an interger, if it can be converted or alreaady is, it gets returned as an INT, if it cant be converted, a type error is passed and returned to the procedure
                return agenum
            except TypeError:
                return None#if it cant be converted, a type error is passed and returned to the procedure
        return None

def getage(indob): # as the graph api dosent return the ages of the users, this function converts the given birthday to a age in years
    now = datetime.datetime.now()# the current date and time is found using datetime function
    # the graph API return the birthday in the american style, and the datetime function used a Y/M/D style, so it has to be converted
    dob = datetime.datetime.strptime(datetime.datetime.strptime(indob, '%m/%d/%Y').strftime('%Y/%m/%d'), '%Y/%m/%d')
    age = floor(((now - dob).days) / 365)#The age in days is calculated and divied to give the age in years.
    return age

def errormsg(msg): #If an error occurs this function is called
    return '<p style="color: red">' + msg +'</p>\n' # The error message specific to the error is printed as a red paragraph

def pageheader(extra_header = ''):# This is HTML for the page header, containing the meta data for the site, including CSS and the favicon which is retrieved from an Amazon server
    output = '\
        <!DOCTYPE html>\n\
        <html lang="en">\n\
        <head>\n\
            <link href="https://fonts.googleapis.com/css?family=Raleway|Roboto+Condensed|Ubuntu" rel="stylesheet">\n\
            <meta charset="UTF-8">\n\
            <link rel="shortcut icon" href="https://s3.eu-west-2.amazonaws.com/connecter/Favicon.ico" type="image/x-icon">\n\
            <meta name="viewport" content="width=device-width, initial-scale=1">\n\
            <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n\
            <title>Connecter</title>\n' +\
            extra_header +\
            '<style>\n\
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

def pagetop(): #this fuction contain the code to allow the user to return to the index page
    output = '<a href="' + path + '">Home Page</a>'#creates a hyperlink to the index page
    return output

def pagefooter():#this function is a disclaimer as a page footer, as this website was planned to include twitter and linkdin for data gathering
    output = '<footer>\n\
                <p>This website currently only supports Facebook</p>\n\
            </footer>\n\
        </body>\n\
    </html>\n';
    return output

def index(request):#ah yes, the main page function
    any_checked = ''#these variables are declared to ensure that the checkboxes are checked depending on whether it is the first time visiting the page or a redirect
    male_checked = ''
    female_checked = ''

    error = request.GET.get("error")#Checks to see if an error had occured in an eariler part of the program that required changes to the page
    output = pageheader() # This takes the HTMlL code and adds it to the output which will be read and displayed as the pages HTML
    gender = request.GET.get('gender')#gets the gender field from the HTTP request, returned by the results page, if is is empty, it has a nulltype value
    max_age = request.GET.get('max_age')#gets the max age field from the HTTP request, returned by the results page, if is is empty, it has a nulltype value
    min_age = request.GET.get('min_age')#gets the min age field from the HTTP request, returned by the results page,  if is is empty, it has a nulltype value

    if not gender or gender == 'any':#this statment sees if there is a prefequiste box to be checked if the results page sends back a box, and if there is no prerequiste, the "any" box is checked
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

    #This is the HTML for the Index page, where you can enter your search terms and visit the bookmarks page
    #This output is for the connecter logo and the slogan
    output += '<div class="w3-row">\n\
                  <div class="w3-blue-grey w3-container w3-center" style="height:1080px">\n\
                    <div class="w3-padding-64">\n\
                      <h1>Connecter</h1>\n\
                         <img src="https://s3.eu-west-2.amazonaws.com/connecter/Logo_Design.png" style="width:50%">\n\
                    </div>\n\
                    <div class="w3-padding-64">\n\
                      <p>Welcome to Connecter, the website for all your prospective employee research needs.</p>\n'
    #A search bar is generated where the user can inout a name to search, if left blank, no search term will be passed. Under the bar are 3 checkboxes for gender, male female and any, and an age range selector,
    #where you can provide a upper and lower boundry for the ages you wish to search. There is a link to the bookmarks page underneath the boxes to directly access the bookmarks page.
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
    fr_gender = ''
    search_exp = request.GET.get('search')#Retrieves the search name from the http request
    gender = request.GET.get('gender')#Retrieves the gender from the http request
    max_age = getnum(request.GET, 'max_age')#Retrieves the max age from the http request
    min_age = getnum(request.GET, 'min_age')#Retrieves the min age from the http request
    male_count = 0
    female_count = 0
    unknown_count = 0
    age18_29 = 0
    age30_44 = 0
    age45_60 = 0
    unknown_age = 0
    search_exp = search_exp[:30] #This limits the length of the search term to 30 characters, both to prevent attemps at code injection and to reduce the search times
    search_words = search_exp.split()#Splits the search term into an array consisting of any separate words in the search term
    normal_search_words = [(strnorm(word)) for word in search_words]#Calls the normalisation function for each of the split search words
    #the following line of code opens a connection to the facebook servers via an access token, and reads the response into a variable, it retreives specific data, namely the birthday, gender and name
    fbresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.5/me?fields=friends%7Bgender%2Cbirthday%2Cfirst_name%2Clast_name%7D&access_token=' + token).read()
    fbresp = json.loads(fbresp_str.decode('utf-8'))#The variable is then decoded from its native JSON format into the common utf-8 standard
    # this hyperlink returns the user to the main page with all the search terms ready to be replaced in the boxes
    search_return = '<a href="' + path + '?search='+ search_exp + '&gender=' + gender + '&min_age=' + str(min_age) + '&max_age=' + str(max_age) + '">Return to Index Page</a>'
    results = ''
    # Main search logic starts here
    frdata = fbresp['friends']['data']#The decoded JSON file is a dictionary of dictionaries containing the users information, this retrieves the data of all search results from the list
    for fr in frdata:
        nml = strnorm(fr['last_name'])#Both the first and last names of the results are then normalised
        nmf = strnorm(fr['first_name'])

        matched_name = False# If this is true, it means that at least of the search terms was found in the user name, this later prevents from the users name being added to the list more than once

        if search_exp:#If the search term was found in the name, or there is no search term, matched_name turn true
            for qs in normal_search_words:
                if nml.find(qs) > -1 or nmf.find(qs) > -1:
                    matched_name = True
        else:
            matched_name = True

        matched_gender = False

        if 'gender' in fr:
            fr_gender = fr['gender']  # retreives the results gender from the results dictionary

        if gender != "any":#if the selected gender matches the gender of the user or there is no preference matched_gender will be true
            if fr_gender and fr_gender == gender:
                matched_gender = True
            else:
                print('gender nor found')
        else:
            matched_gender = True

        matched_age = False# If there is no age range or the users age falls between the limits matched_age is true
        if 'birthday' in fr:
            age = getage(fr['birthday'])#retreives the results birthday from the results dictionary and converts it into an age in years
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

        if matched_name and matched_age and matched_gender:#If all 3 requirements are met, the user id and name are passed to a list of hyperlinks to the users profiles
            print('gender =' + fr_gender)
            if fr_gender == 'male':
                male_count += 1
            elif fr_gender == 'female':
                female_count += 1
            else:
                unknown_count += 1
            if age < 30:
                age18_29 += 1
            elif 29 < age <45:
                age30_44 += 1
            elif 44 < age:
                age45_60 += 1
            else:
                unknown_age += 1
            results += '<a href="results?id=' + fr['id'] + '">' + fr['last_name'] + ', ' + fr['first_name'] + '<a><br>'
            result_num += 1 #the number of results is incremented

    # Generating output
    output = pageheader() + pagetop()#the page top and header are added to the output
    if result_num > 20:#If more than 20 results are found, the user is given the choice to refine their search by redirecting to the main page
        restriction =  '<p>Your returned list is over 20 individuals long, please click on the link to refine your search</p>\n\
                        ' + search_return #This returns all the search data to the index page, so that it appears in the boxes to remind the user what they where searching for
    if result_num == 0:#If no reesults are found, the user is informed and redirected to the index page
        output += '<div class="w3-row">\n\
                    <div class="w3-black w3-container w3-center" style="height:1080px">\n\
                        <div class="w3-padding-64">\n\
                            <h1>There are no users matching your search, please try again</h1>\n ' +\
                        search_return +\
                        '</div>\n\
                    </div>\n\
                </div>'
    else:#if there are results, the user is shown the list and if the list is longer than 20, the redirection option is also displayed
        output +=   '<div class="w3-row">\n\
                        <div class="w3-black w3-container w3-center" style="height:1080px">\n\
                            <div class="w3-padding-64">\n\
                                <h1>Search Results</h1>\n' +\
                                restriction + \
                                '<a href="' + path + 'gender_graphs?male_count=' + str(male_count) + '&female_count=' + str(female_count) + '&unknown_count=' + str(unknown_count) + '">Gender report</a> \n\
                                <a href="' + path + 'age_graphs?age18_29=' + str(age18_29) + '&age30_44=' + str(age30_44) + '&age45_60=' + str(age45_60) + '">Age report</a> \n\
                            </div>\n\
                            <div class="w3-padding-64">\
                                <p>Please Choose The User You Meant</p>\n' +\
                                results +\
                            '</div>\n\
                        </div>\n\
                    </div>'
    output += pagefooter()
    return HttpResponse(output)


def results(request):
    work = "N/A"#all retrivable data variables are set to a default so if no results exist, N/A is shown to the user
    results = "N/A"
    education = "N/A"
    location = "N/A"
    email = "N/A"
    age = "N/A"
    name = "N/A"
    quotes = "N/A"
    about = "N/A"
    user_id = request.GET.get('id')

    if not user_id:#ifby any chance nouser id is retreived form the  HTTP request the user is redirected to the index page to try again
        output = page_header() + page_footer()
        output += errormsg('No user id was recieved, search again')#this is the message to be displayed in red to the user
        return HttpResponse(output)

    picresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.5/' + user_id + '/picture?height=200&width=200&redirect=false&access_token=' + token).read()#This retreives the users profile picture using the ID and the acces token
    picresp = json.loads(picresp_str)# the pictures url has to be decoded from its JSON format so it can be displayed on screen
    pic_url = picresp['data']['url']#the url of the picture is separated from the JSON file and saved as a variable
    #the following line of code opens a connection to the facebook servers via an access token, and reads the response into a variable, it retreives specific data, namely the birthday, gender, quotes, education, work, location, email and name
    fbresp_str = urllib.request.urlopen('https://graph.facebook.com/v2.11/' + user_id + '?fields=birthday%2Cquotes%2Cname%2Ceducation%2Cemail%2Cwork%2Cabout%2Cfriends%2Clocation&access_token=' + token).read()
    fbresp = json.loads(fbresp_str.decode('utf-8'))#The variable is then decoded from its native JSON format into the common utf-8 standard

    if 'location' in fbresp:#The following if statments check to see if the information we want displayed exists in the JSON file
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
        age = getage(dob)#Once again the birthday need to be converted to an age in years

    if 'work' in fbresp:#creates a list of the places the user has worked
        work = ""
        for job in fbresp['work']:
            employer = job['employer']
            job_location = job['location']
            if employer:
                work += employer['name']
                if job_location:
                    work += ' (' + job_location['name'] + ')'
                work += '<br>'\

    if 'education' in fbresp:#creates a list of the places the user has had education
        education = ""
        for edu in fbresp['education']:
            school = edu['school']
            if school:
                education += school['name'] + '<br>'

    if 'friends' in fbresp:#creates a list of the users friends
        results = ""
        frdata = fbresp['friends']['data']
        for fr in frdata:
                results += '<a href="results?id=' + fr['id'] + '">' + fr['name'] +  '<a><br>'

    if 'name' in fbresp:
        name = fbresp['name']

    if user_id in bookmark_dict:#if the user has been bookmarked an option to unbookmark is shown, if the users id is in the bookmark dictionary
        action = '<a href="bookmarks?key=' + user_id + '">Unbookmark profile</a>'
    else:#if the user has not been bookmarked an option to bookmark is shown, if the users id is not in the bookmark dictionary
        action = '<a href="bookmarks?id=' + user_id + '&name=' + name + '&action=' + 'unbookmark' + '">Bookmark profile</a>'

    output = pageheader() + pagetop()
    #The information is printed to the user in 2 columns, one for the personal information and one for the persons about sedction and favorite quotes
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

def bookmarks(request):#this is the bookmarks page
    output = pageheader() + pagetop()
    results = "You have no bookmarked individuals"# The default response is that there are no bookmarks, this get overwritten when the bookmarks are recovered, if any exist
    key = request.GET.get('key')#This is a marker that says you wish to unbookmark this user
    if key and key in bookmark_dict:#if the key exists and the key is in the bookmarks dictionary, that key and value will be deleted
        del bookmark_dict[key]
    bookmark_name = ""
    bookmark_id = ""
    name = request.GET.get('name')#The name and ID of the person to be bookmarks is retrieved from the request
    id = request.GET.get('id')
    if name:#if both the name and the id exist, the users name and id are added to the bookmarks dictionary with the unique ID as the key and the naem as the value
        bookmark_name = name
    if id:
        bookmark_id = id
    if name and id:
        bookmark_dict[bookmark_id] = bookmark_name
    if bool(bookmark_dict) == True:#if the bookmark dictionary is not empty
        results = ""
        for bookmark in bookmark_dict.keys(): #all the bookmarks are printed out in a list as links to their respective resulst pages, and an option to remove the bookmarks is also present next to the name as an X
            results += '<a href="results?id=' + bookmark + '">' +  str(bookmark_dict[bookmark]) +'<a>\
            <a href="bookmarks?key=' + bookmark + '">X<a><br>'

    #The actual HTML display and the list are positioned here
    output += ' <div class="w3-row">\n\
                    <div class="w3-black w3-container w3-center" style="height:1080px">\n\
                        <div class="w3-padding-64">\n\
                            <h1>Your bookmarks</h1><br><br>\n' + \
                            results + \
                        '</div>\n\
                    </div>\n\
                </div>'
    output += pagefooter()
    return HttpResponse(output)


def age_graphs(request):
    age18_29 = ''
    age18_29 = request.GET.get('age18_29')
    age30_44 = ''
    age30_44 = request.GET.get('age30_44')
    age45_60 = ''
    age45_60 = request.GET.get('age45_60')
    if not age18_29:
        age18_29 = ''
    if not age30_44:
        age30_44 = ''
    if not age45_60:
        age45_60 = ''
    extra = '<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script> \n\
            <script type="text/javascript">\n\
              google.charts.load(\'current\', {\'packages\':[\'bar\']});\n\
              google.charts.setOnLoadCallback(drawChart);\n\
              function drawChart() {\n\
                var data = google.visualization.arrayToDataTable([\n\
                  [\'Age range\', \'Number of matches\', { role: \'style\' }],\n\
                  [\'18-25\', ' + age18_29 + ', \'#ff0000\'],\n\
                  [\'30-45\', ' + age30_44 + ', \'silver\'],\n\
                  [\'40+\', ' + age45_60 + ', \'green\'],\n\
                ]);\n\
                var options = {\n\
                  chart: {\n\
                    title: \'Age Range\',\n\
                  },\n\
                bars: \'horizontal\'\n\
                };\n\
                var chart = new google.charts.Bar(document.getElementById(\'columnchart_material\'));\n\
                chart.draw(data, google.charts.Bar.convertOptions(options));\n\
              }\n\
            </script>'
    output = pageheader(extra) +pagetop()
    output +=   '<div class="w3-row">\n\
                    <div class="w3-blue-grey w3-container w3-center" style="height:1080px">\n\
                        <div class="w3-padding-64">\n\
                            <h1>Age Report</h1>\n\
                            <div id="columnchart_material" style="width: 800px; height: 500px; display: block; margin: 0 auto;">\n\
                            </div>\n\
                        </div>\n\
                    </div>\n\
                </div>\n'
    output += pagefooter()
    return HttpResponse(output)

def gender_graphs(request):
    male_count = ''
    female_count = ''
    unknown_count = ''
    male_count = request.GET.get('male_count')
    female_count = request.GET.get('female_count')
    unknown_count = request.GET.get('unknown_count')
    if not male_count:
        male_count = ''
    if not female_count:
        female_count = ''
    if not unknown_count:
        unknown_count = ''
    extra = '<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script> \n\
            <script type="text/javascript">\n\
              google.charts.load(\'current\', {\'packages\':[\'bar\']});\n\
              google.charts.setOnLoadCallback(drawChart);\n\
              function drawChart() {\n\
                var data = google.visualization.arrayToDataTable([\n\
                  [\'Gender\', \'Number of matches\', { role: \'style\' }],\n\
                  [\'Male\', ' + male_count + ', \'#ff0000\'],\n\
                  [\'Female\', ' + female_count + ', \'silver\'],\n\
                  [\'Unknown\', ' + unknown_count + ', \'green\'],\n\
                ]);\n\
                var options = {\n\
                  chart: {\n\
                    title: \'Gender distribution\',\n\
                  }\n\
                };\n\
                var chart = new google.charts.Bar(document.getElementById(\'columnchart_material\'));\n\
                chart.draw(data, google.charts.Bar.convertOptions(options));\n\
              }\n\
            </script>'
    output = pageheader(extra) +pagetop()
    output +=   '<div class="w3-row">\n\
                    <div class="w3-blue-grey w3-container w3-center" style="height:1080px">\n\
                        <div class="w3-padding-64">\n\
                            <h1>Gender Report</h1>\n\
                                <div id="columnchart_material" style="width: 800px; height: 500px; display: block; margin: 0 auto;">\n\
                            </div>\n\
                        </div>\n\
                    </div>\n\
                </div>\n'
    output += pagefooter()
    return HttpResponse(output)