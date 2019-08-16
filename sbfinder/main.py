import json
#import urllib
#import urllib.parse
import requests
import bs4
import threading
import urllib
import csv

headers = {
'authorization': None,
'cache-control': "no-cache",
}

def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i + n]

def set_api_key(apiKey):
	headers['authorization'] = "Bearer " + apiKey

def get_mobile_site(url):
	# Gets the mobile site
	headers = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
	for i in range(3):
		try:
			res = requests.get(url, headers=headers, timeout=10)
			if res.status_code == 200:
				return res
		except:
			pass

def get_desktop_site(url):
	# Gets the desktop site
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	for i in range(3):
		try:
			res = requests.get(url, headers=headers, timeout=10)
			if res.status_code == 200:
				return res
		except:
			pass
 
#need the following parameters (type dict) to perform business search. 
#params = {'name':'walmart supercenter', 'address1':'406 S Walton Blvd', 'city':'bentonville', 'state':'ar', 'country':'US'}


def search(term, threadCount, location, saveAs="file.csv"):
	params = {'term':term, 'location':location}

	#param_string = urllib.parse.urlencode(params)
	#conn = http.client.HTTPSConnection("api.yelp.com")
	x = "address1="
	#res = requests.get("https://api.yelp.com/v3/businesses/matches/best?", headers=headers, params=params)
	res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)

	#res = conn.getresponse()
	#data = res.read()
	#data = json.loads(data.decode("utf-8"))
	data = res.json()
	print json.dumps(data, indent=4)
	#raw_input("CONTINUE")
	a = []
	# Iterate over all of the results for this search

	results = data["businesses"]
	#print(len(results))

	listOfPins = chunks(results, int(len(results)/threadCount))
	#print len(list(listOfPins))

	def process(listOfResults):
		for val in listOfResults:
			print(val)
			# Replace the URL with a valid mobile URL
			url = val['url'].replace("https://www.yelp.com", "https://m.yelp.com")
			# Grab the site using mobile headers | yelp will redirect if not
			res = get_mobile_site(url)
			# Parse the mobile site as a bs4 object
			page = bs4.BeautifulSoup(res.text, 'lxml')
			# Select the "website" button src
			buttonInfo = page.select(".js-external-link-action-button")
			val['hasWebsite'] = len(buttonInfo) != 0
			if len(buttonInfo) == 0:
				val['website'] = None
			else:
				val['website'] = urllib.unquote(str(buttonInfo).partition('" href="')[2].partition('"')[0]).partition('&amp')[0].partition('?url=')[2]
			a.append(val)
			#print val.keys()
			if val['hasWebsite'] == False:
				phone = val['display_phone']
				if len(phone) < 2:
					phone = "NO PHONE NUMBER"
				print("{} | {}".format(val['name'],  phone))
			#print val['website']

	threads = [threading.Thread(target=process, args=(ar,)) for ar in listOfPins]

	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	if saveAs != None:
		if len(a) > 0:
			g = a[0].keys()
			new = [g]
			for val in a:
				new.append([val.get(v, "") for v in g])
			with open(saveAs, "wb") as f:
				writer = csv.writer(f)
				writer.writerows(new)
	return a
