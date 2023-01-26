#!/usr/bin/env python3

import cgi
import cgitb
import secret

# user will be able to do what they want to do
cgitb.enable()

import os
import json
from templates import login_page, secret_page, after_login_incorrect
from http.cookies import SimpleCookie


# how the posted data gets to cgi
s = cgi.FieldStorage() # creates the fields

# get first element in that html file
username = s.getfirst("username") # get the first field with the name username
password = s.getfirst("password") # send the data using these fields (getfirst after fieldstorage)

form_ok = username == secret.username and password == secret.password

# stores user data, give you relevant info/ads
cookie = SimpleCookie(os.environ["HTTP_COOKIE"])
cookie_username = None
cookie_password = None
if cookie.get("username"):
    cookie_username = cookie.get("username").value
if cookie.get("password"):
    cookie_password = cookie.get("password").value

cookie_ok = cookie_username == secret.username and cookie_password == secret.password

if cookie_ok:
    username = cookie_username
    password = cookie_password


print("Content-type: text/html")
if form_ok:
    # How we set a cookie - we defined what the cookie key should be (http header - set cookie)
    print(f"Set-Cookie: username = {username}")
    print(f"Set-Cookie: password = {password}")
    # in browser, http_cookie sends the value of the cookie back
print()

if not username and not password:
    print(login_page()) # refreshes the page
elif username == secret.username and password == secret.password:
    print(secret_page(username, password))
else:
    print(login_page()) # display login page
    print("username & password: ", username, password)