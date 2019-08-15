import main

if __name__ == '__main__':
	print """
** SMALL BUSINESS FINDER 2.0 **
\nThis script uses the Yelp fusion API to find
nearby small businesses with no online presence\n\n
	"""
	threads = raw_input("Number of threads [Default 20]: ")
	search_term = raw_input("Search Term: ")
	location = raw_input("City: ")
	state = raw_input("State: ")
	saveAs = raw_input("CSV Filename [leave blank for stdout only]: ")
	print("\n\n")
	if len(saveAs) == 0:
		main.search(search_term, int(threads), location + " " + state)
	else:
		main.search(search_term, int(threads), location + " " + state, saveAs)