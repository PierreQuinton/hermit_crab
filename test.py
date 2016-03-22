# -*- coding: utf-8 -*-

import urllib2
import requests

user='Calamar'
passw=urllib2.quote('bot2016')
baseurl='http://wikipast.world/wiki/'
login_params='?action=login&lgname=%s&lgpassword=%s&format=json'% (user,passw)
summary='Créatibot update'

# Login request
r1=requests.post(baseurl+'api.php'+login_params)
login_token=r1.json()['login']['token']

#login confirm
login_params2=login_params+'&lgtoken=%s'% login_token
r2=requests.post(baseurl+'api.php'+login_params2,cookies=r1.cookies)
