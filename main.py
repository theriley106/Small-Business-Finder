#Finding reviews for a particular restaurant
#import http.client
import json
#import urllib
#import urllib.parse
import requests
import bs4
import urllib

headers = {
'authorization': "Bearer pzSBkPRXCSnVAHgDo49RNMAiymCWupi9-DE723hfZr29Dd1eN9i3J5UTzrwlNN2tp9ByGht-gbVnsm1tXXibgVQUygiKFCocIiGFqEvBJNdGQsLiUJCNY2oRi-pSXXYx",
'cache-control': "no-cache",
}

def get_mobile_site(url):
	# Gets the URL from Yelp
	headers = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
	for i in range(3):
		try:
			res = requests.get(url, headers=headers)
			if res.status_code == 200:
				return res
		except:
			pass

#need the following parameters (type dict) to perform business search. 
#params = {'name':'walmart supercenter', 'address1':'406 S Walton Blvd', 'city':'bentonville', 'state':'ar', 'country':'US'}
params = {'term':'grocery', 'location':'bentonville ar'}

#param_string = urllib.parse.urlencode(params)
#conn = http.client.HTTPSConnection("api.yelp.com")
x = "address1="
#res = requests.get("https://api.yelp.com/v3/businesses/matches/best?", headers=headers, params=params)
res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)

#res = conn.getresponse()
#data = res.read()
#data = json.loads(data.decode("utf-8"))
data = res.json()
print json.dumps(data["businesses"], indent=4)
a = []
#raw_input("AYY")
for val in data["businesses"]:
	url = val['url'].replace("https://www.yelp.com", "https://m.yelp.com")
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	headers = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
	res = requests.get(url, headers=headers)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	buttonInfo = page.select(".js-external-link-action-button")
	val['hasWebsite'] = len(buttonInfo) != 0
	if len(buttonInfo) == 0:
		val['website'] = None
	else:
		val['website'] = urllib.unquote(str(buttonInfo).partition('" href="')[2].partition('"')[0]).partition('&amp')[0].partition('?url=')[2]
	a.append(val)

print a

