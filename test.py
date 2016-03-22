# -*- coding: utf-8 -*-

import urllib2
import requests

user='Calamar'
passw=urllib2.quote('poulpe')
baseurl='http://wikipast.world/wiki/'
login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)
summary='Calamarisation'

# Login request
r1=requests.post(baseurl+'api.php'+login_params)
login_token=r1.json()['login']['token']

#login confirm
login_params2=login_params+'&lgtoken=%s'% login_token
r2=requests.post(baseurl+'api.php'+login_params2,cookies=r1.cookies)

#get edit token2
params3='?format=json&action=query&meta=tokens&continue='
r3=requests.get(baseurl+'api.php'+params3,cookies=r2.cookies)
edit_token=r3.json()['query']['tokens']['csrftoken']

edit_cookie=r2.cookies.copy()
edit_cookie.update(r3.cookies)

#actual code

