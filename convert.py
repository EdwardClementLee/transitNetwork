import sys, csv, json, math

# source folder
folder = sys.argv[1]
if folder[-1] != "/":
	folder += "/"

# destination file
dest = sys.argv[2]

# proximity tolerance
prox = 0.001
proxName = 0.01 # proximity tolerance if the name is the same
if len(sys.argv) > 3:
	prox = float(sys.argv[3])

# reads csv file and returns keyed dictionary of objects
def readFile(path, idField, multiple):
	d = {}
	with open(path, "r") as f:

		reader = csv.reader(f, delimiter=",")
		headers = reader.next()

		for row in reader:
			obj = {}

			for i, col in enumerate(row):
				obj[headers[i]] = col

			if idField in obj:
				if multiple == True:
					if obj[idField] not in d:
						d[obj[idField]] = [obj]
					else:
						d[obj[idField]].append(obj)

				else:				
					d[obj[idField]] = obj
			else:
				print "Error: could not find column " + idField + " in " + path

	return d

if folder is not None:

	# read csv files	
	stopsAll = readFile(folder+"stops.txt", "stop_id", False)
	routes = readFile(folder+"routes.txt", "route_id", False)
	trips = readFile(folder+"trips.txt", "trip_id", False)
	stopTimes = readFile(folder+"stop_times.txt", "trip_id", True)

	# remove redundancy from the stops array
	# this uses proximity to test and merge if close enough
	nodes = [] # reduced list of stops becomes the node array
	stopIds = {} # map of original ids to stop keys
	for k in stopsAll:
		stop = stopsAll[k]		
		match = None
		for i, check in enumerate(nodes):
			x = float(check["stop_lon"]) - float(stop["stop_lon"])
			y = float(check["stop_lat"]) - float(stop["stop_lat"])
			p = math.hypot(x, y)
			if check["stop_name"] == stop["stop_name"]:
				pr = proxName
			else:
				pr = prox
			if p < pr:
				match = i
				# uncomment the following two lines to see proximate stops being merged
				# if p > 0.0:
				# 	print stop["stop_name"] + " >>> " + check["stop_name"] + " prox: " + str(math.hypot(x,y))
				break
		if match is None:
			nodes.append(stop)
			stopIds[stop["stop_id"]] = len(nodes)-1
		else:
			stopIds[stop["stop_id"]] = i

	# create edges between stops based on stop times
	edges = {}
	for k in stopTimes:
		trip = trips[k]
		route = routes[trip["route_id"]]
		lastIndex = None
		for s in stopTimes[k]:
			thisIndex = stopIds[s["stop_id"]]
			if lastIndex == None:
				lastIndex = thisIndex
			else:
				edgeId = route["route_id"]+"-"+str(lastIndex)+"-"+str(thisIndex)
				if edgeId not in edges:
					edges[edgeId] = { 
							"source": lastIndex, 
							"target": thisIndex, 
							"value": 1, 
							"sourceName": nodes[lastIndex]["stop_name"],
							"targetName": nodes[thisIndex]["stop_name"],
							"routeId": route["route_id"],
							"routeName": route["route_short_name"],
							"routeColor": route["route_color"]
						}
				else:
					edges[edgeId]["value"] += 1
				lastIndex = thisIndex

	# stats
	print "################"
	print str(len(nodes)) + " nodes"
	print str(len(edges)) + " edges"

	# write JSON file
	output = open(dest, "w")
	output.write(json.dumps({ "nodes": nodes, "edges": edges.values() }))
	output.close()