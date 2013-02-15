import sys, csv, json

# source folder
folder = sys.argv[1]
if folder[-1] != "/":
	folder += "/"

# destination file
dest = sys.argv[2]

# special map of stop ids to names
stopIds = {}

# reads csv file and returns keyed dictionary of objects
def readFile(path, idField, special):
	d = {}
	with open(path, "r") as f:

		reader = csv.reader(f, delimiter=",")
		headers = reader.next()

		for row in reader:
			obj = {}

			for i, col in enumerate(row):
				obj[headers[i]] = col

			if special == "stops":
				stopIds[obj["stop_id"]] = obj["stop_name"]

			if special == "multiple":
				if obj[idField] not in d:
					d[obj[idField]] = [obj]
				else:
					d[obj[idField]].append(obj)

			else:
				d[obj[idField]] = obj

	return d

if folder is not None:

	# read csv files	
	stops = readFile(folder+"stops.txt", "stop_name", "stops")
	routes = readFile(folder+"routes.txt", "route_id", None)
	trips = readFile(folder+"trips.txt", "trip_id", None)
	stopTimes = readFile(folder+"stop_times.txt", "trip_id", "multiple")

	# find longest set of stoptimes for each route
	for k in stopTimes:
		trip = trips[k]
		s = stopTimes[k]
		r = routes[trip["route_id"]]
		if "stops" not in r:
			r["stops"] = s
		elif len(r["stops"]) < len(s):
			r["stops"] = s

	# create nodes array based on stops
	nodes = []
	nodeIndices = {}
	i = 0
	for k in stops:
		n = stops[k]
		nodeIndices[n["stop_name"]] = i
		i += 1
		nodes.append({ "name": n["stop_name"], "lat": n["stop_lat"], "lng": n["stop_lon"] })

	# create edges between stops based on stop times
	edges = {}
	for k in routes:
		r = routes[k]
		lastIndex = None
		if "stops" in r:
			print "Finding stops for "+r["route_short_name"]
			for s in r["stops"]:
				thisIndex = nodeIndices[stopIds[s["stop_id"]]]
				if lastIndex == None:
					lastIndex = thisIndex
				else:
					edgeId = r["route_id"]+"-"+str(lastIndex)+"-"+str(thisIndex)
					if edgeId not in edges:
						edges[edgeId] = { 
								"source": lastIndex, 
								"target": thisIndex, 
								"value": 1, 
								"sourceName": nodes[lastIndex]["name"],
								"targetName": nodes[thisIndex]["name"],
								"routeId": r["route_id"],
								"routeName": r["route_short_name"],
								"routeColor": r["route_color"]
							}
					else:
						edges[edgeId]["value"] += 1
					lastIndex = thisIndex

	# write JSON file
	output = open(dest, "w")
	output.write(json.dumps({ "nodes": nodes, "edges": edges.values() }))
	output.close()