# implemented features
# shorten
# retrieve
# qr

# not implemented features
# create
# update
# expand
# finish clicks
# Get a Clicks Summary for a Bitlink
# Get Metrics for a Bitlink by Country
# getMetricsForBitlinkByCities
# getMetricsForBitlinkByDevices
# getMetricsForBitlinkByReferrers
# getMetricsForBitlinkByReferringDomains
# getMetricsForBitlinkByReferrersByDomains
# getBitlinksByGroup
# getSortedBitlinks
# no account support
# free qr


import sys
import requests
import qrcode
import json
import os
from selenium.webdriver.firefox import webdriver
import webbrowser

driver = None
config = os.path.dirname(__file__) + "/config.json"
TOKEN = None

if len(sys.argv) > 1:
    if (sys.argv[1].lower() == "deletetoken"):
        os.remove(config)
        print("Token deleted!")
        print()

if os.path.exists(config):
    with open(config) as json_data_file:
        TOKEN = json.load(json_data_file)["token"]
        if str(TOKEN).lower() == "notoken":
            TOKEN = None
            print("No Token saved! type 'bitly deletetoken' if you want to link your account")
else:
    print(
        "You have to input your access token if you want to use a account! Create on here: https://bitly.is/accesstoken")
    print("If you dont enter a token you could only create links!")
    print(
        "The access token will be stored in plain text in the root directory of this application. You could always delete the token with bitly deletetoken")
    print("If you dont want to link an account type 'notoken' instead of the token")
    with open(config, "w") as outfile:
        token = input("TOKEN? ")
        json.dump({"token": token}, outfile)
        TOKEN = token
        if str(TOKEN).lower() == "notoken":
            TOKEN = None
            print("No Token saved! type 'bitly deletetoken' if you want to link your account")


def helpUser():
    print("__HELP__")

    if TOKEN == None:
        print("You have no Token specified! add one to access more options via 'bitly deletetoken'")
    else:
        print("-Delete your Token, input another: bitly deletetoken")
        print("-Short a link: bitly shorten https://dev.bitly.com/")
        print("-Get the original link: bitly retreive bit.ly/12a4b6c")
        print("-Generate Qr code even without bitly pro: bitly qr bit.ly/12a4b6c")
    print("-Short a link without an account: bitly shorten-noaccount https://dev.bitly.com/")


def shorten(url):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }
    data = '{ "long_url": "' + url + '", "domain": "bit.ly" }'
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    return response.json()["link"], response


def shortenNoAccount(url):
    pass


def retrieve(url):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
    }
    response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/' + url, headers=headers)
    return response.json()["long_url"], response


def qr(url):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
    }
    response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/' + url + '/qr', headers=headers)
    try:
        return response.json()["qr_code"], response
    except KeyError:
        response = response.json()
        print(response["message"])
        print(response["description"])
        print("Generating qr code not via bitlink:")
        img = freeqr(biturl)
        img.save(biturl[biturl.index("/") + 1:-1] + ".png")
        img.show()
        return None


def freeqr(url):
    img = qrcode.make(url)
    return img


def getClicks(url):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
    }
    response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/' + url + '/clicks/summary', headers=headers)
    return response.json()["total_clicks"], response


if not len(sys.argv) == 3:
    helpUser()
    exit()

action = sys.argv[1]
url = sys.argv[2]

if not TOKEN == None:
    try:
        biturl = sys.argv[2][sys.argv[2].index("bit"):len(sys.argv[2])]
    except Exception:
        biturl = None

    try:
        if str(action).lower() == "shorten":
            returned = shorten(url)
            response = returned[1]
            print(returned[0])

        elif str(action).lower() == "retrieve":
            returned = retrieve(biturl)
            response = returned[1]
            print(returned[0])

        elif str(action).lower() == "qr":
            returned = qr(biturl)
            if not returned == None:
                response = returned[1]
                print(returned[0])


        elif str(action).lower() == "clicks":
            returned = getClicks(biturl)
            response = returned[1]
            print(returned[0])
    except KeyError:
        print(response["message"])
        print(response["description"])

try:
    if str(action).lower() == "shorten-noaccount":
        print("Make sure Firefox is installed")
        if not os.path.exists("geckodriver.exe"):
            print("No Geckodriver installed. Please download, extreact, and move to the application folder")
            webbrowser.open("https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-win64.zip")
            print("Application Folder "+os.path.dirname(__file__))

        if driver is None:
            driver = webdriver.firefox

except KeyError:
    print(response["message"])
    print(response["description"])
