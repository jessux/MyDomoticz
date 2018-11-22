import requests
from settings import *
import json
import datetime
from tokenstore import TOKEN

def login():
    login1 = requests.get("https://account.withings.com/oauth2_user/authorize2?response_type=code&client_id="+CLIENT_ID+"&scope="+SCOPE+"&redirect_uri="+CALLBACK_URI+"&state=mydomoticz&selecteduser=4435001")
    print login1.url
    code = raw_input("Code :")
    token = requests.post('https://account.withings.com/oauth2/token',
                          data="grant_type=authorization_code&"
                               "client_id=" + CLIENT_ID + "&"
                               "client_secret=" + CLIENT_SECRET + "&"
                               "code=" + code + "&"
                               "redirect_uri=" + CALLBACK_URI)

    d = json.loads(token.text)
    return d

def refresh(RT):
    token = requests.post("https://account.withings.com/oauth2/token",data="grant_type=refresh_token&"
                                                                   "client_id="+CLIENT_ID+"&"
                                                                   "client_secret="+CLIENT_SECRET+"&"
                                                                   "refresh_token="+RT)
    d = json.loads(token.text)
    with open("tokenstore.py", "w") as outfile:
        outfile.write("TOKEN='")
        json.dump(d,outfile)
        outfile.write("'")
    from tokenstore import TOKEN
    return d


def api(AT,MEASURE):
    metrics = requests.get(
        "https://wbsapi.withings.net/measure?action=getmeas&access_token=" + AT + "&meastype="+str(MEASURE)+"&category=1")
    d = json.loads(metrics.text)

    return d


#d = login()
#print d

d = json.loads(TOKEN)
weight={}
height={}
fatfree={}
fatratio={}
fatmassweight={}
bpm={}
while True:
    try:
        for measure in MEASURES:
            if measure == 1:
                weight=api(d[u'access_token'],measure)
                with open("dataweight.json", "w") as outfile:
                    outfile.write('{"date": "'+datetime.datetime.fromtimestamp(weight[u'body'][u'measuregrps'][0][u'created']).strftime('%d-%m-%Y %H:%M:%S')+'",')
                    outfile.write('"poids":')
                    for p in weight[u'body'][u'measuregrps'][0][u'measures']:
                        outfile.write(str(p[u'value'])[:-3] + "." + str(p[u'value'])[len(str(p[u'value'])) - 3:])
                    outfile.write("}")
            elif measure == 4:
                height=api(d[u'access_token'],measure)
                print height
            elif measure == 5:
                fatfree=api(d[u'access_token'], measure)
                print fatfree
            elif measure == 6:
                fatratio=api(d[u'access_token'], measure)
                with open("datafatratio.json", "w") as outfile:
                    outfile.write(
                        '{"date": "' + datetime.datetime.fromtimestamp(fatratio[u'body'][u'measuregrps'][0][u'created']).strftime(
                        '%d-%m-%Y %H:%M:%S') + '",')
                    outfile.write('"ratio":')
                    for p in fatratio[u'body'][u'measuregrps'][0][u'measures']:
                        outfile.write(str(p[u'value'])[:-3] + "." + str(p[u'value'])[len(str(p[u'value'])) - 3:])
                    outfile.write("}")
            elif measure == 8:
                fatmassweight=api(d[u'access_token'],measure)
                print fatmassweight
            elif measure == 11:
                bpm=api(d[u'access_token'], measure)
                print bpm
    except:
        d = refresh(d[u'refresh_token'])