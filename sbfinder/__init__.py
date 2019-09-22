import json
import requests
import bs4
import threading
try:
	from urllib import unquote
except:
	from urllib.parse import unquote
import csv
from argparse import ArgumentParser

try:
    input = raw_input
except NameError:
    pass

parser = ArgumentParser()

parser.add_argument("-key", "--key", dest="apiKey",
                    help="Input Yelp fusion api key")

parser.add_argument("-v", "--verbose", dest="verbose",
                    help="Set verbosity level")

args = parser.parse_args()



headers = {
'authorization': "Bearer ",
'cache-control': "no-cache",
}

VERBOSE = [False]

def log(string):
	if VERBOSE[0] != False:
		print(string)

def chunks(l, n):
	for i in range(0, len(l), n):
		yield l[i:i + n]

def get_mobile_site(url):
	log("Getting URL: {}".format(url))
	# Gets the mobile site
	headers = { 'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
	for i in range(3):
		try:
			res = requests.get(url, headers=headers, timeout=10)
			if res.status_code == 200:
				return res
		except Exception as exp:
			log("Network Call Failed #{} | URL: {} | Exception: {}".format(i, url, exp))
	log("Final Network Call Failed: {}".format(url))

def get_desktop_site(url):
	# Gets the desktop site
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	for i in range(3):
		try:
			res = requests.get(url, headers=headers, timeout=10)
			if res.status_code == 200:
				return res
		except Exception as exp:
			log("Network Call Failed #{} | URL: {} | Exception: {}".format(i, url, exp))
	log("Final Network Call Failed: {}".format(url))
 
#need the following parameters (type dict) to perform business search. 
#params = {'name':'walmart supercenter', 'address1':'406 S Walton Blvd', 'city':'bentonville', 'state':'ar', 'country':'US'}


def search(term, threadCount, location, saveAs="file.csv"):
	params = {'term':term, 'location':location}
	log("Searching: {} in {}".format(term, location))
	#param_string = urllib.parse.urlencode(params)
	#conn = http.client.HTTPSConnection("api.yelp.com")
	#res = requests.get("https://api.yelp.com/v3/businesses/matches/best?", headers=headers, params=params)
	res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)

	#res = conn.getresponse()
	#data = res.read()
	#data = json.loads(data.decode("utf-8"))
	data = res.json()
	log(json.dumps(data, indent=4))
	#input("CONTINUE")
	a = []
	# Iterate over all of the results for this search

	results = data["businesses"]
	#print(len(results))

	listOfPins = chunks(results, int(len(results)/threadCount))
	#print len(list(listOfPins))

	def process(listOfResults):
		for val in listOfResults:
			log(val)
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
				val['website'] = unquote(str(buttonInfo).partition('" href="')[2].partition('"')[0]).partition('&amp')[0].partition('?url=')[2]
			a.append(val)
			#print val.keys()
			if val['hasWebsite'] == False:
				phone = val['display_phone']
				if len(phone) < 2:
					phone = "NO PHONE NUMBER"
				print("{} | {}".format(val['name'],  phone))
			log("Finished with {}".format(val['website']))

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

def main(key, verbose):
	VERBOSE[0] = verbose
	headers["authorization"] = "Bearer " + key
	print("""
** SMALL BUSINESS FINDER 2.0 **
\nThis script uses the Yelp fusion API to find
nearby small businesses with no online presence\n\n
	""")
	threads = input("Number of threads [Default 20]: ")
	if len(threads) == 0:
		threads = 20
	search_term = input("Search Term: ")
	location = input("City: ")
	state = input("State: ")
	saveAs = input("CSV Filename [leave blank for stdout only]: ")
	print("\n\n")
	if len(saveAs) == 0:
		search(search_term, int(threads), location + " " + state)
	else:
		search(search_term, int(threads), location + " " + state, saveAs)


if __name__ == '__main__':
	print("""
** SMALL BUSINESS FINDER 2.0 **
\nThis script uses the Yelp fusion API to find
nearby small businesses with no online presence\n\n
	""")
	threads = input("Number of threads [Default 20]: ")
	if len(threads) == 0:
		threads = 20
	search_term = input("Search Term: ")
	location = input("City: ")
	state = input("State: ")
	saveAs = input("CSV Filename [leave blank for stdout only]: ")
	print("\n\n")
	if len(saveAs) == 0:
		search(search_term, int(threads), location + " " + state)
	else:
		search(search_term, int(threads), location + " " + state, saveAs)
	