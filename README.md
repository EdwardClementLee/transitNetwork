transitNetwork
==============

Python script for transforming [GTFS](https://developers.google.com/transit/gtfs/reference) data to node-edge graph data.

This script attempts to transform the transit data from a General Transit Feed Specification (GTFS) folder into a JSON object with nodes as stops and edges as the routes between them.

**Usage**
```
python convert.py <data folder> <output file>
python convert.py ./mta_gtfs/ ./mta.json
```

**Examples**

The /sample/ folder contains several JSON files assembled from real GTFS data as well as a very basic graph visualization to view them. The visualization allows toggling between force-directed and geographic views.

**Notes**
- The GTFS format does not contain a simple data structure for what one would commonly consider the stops along each route (i.e., the map). The network assembled by this script may contain unmaplike edges between nodes, especially where express trips are made between stops.
- Some GTFS files contain very large stop_times.txt files, for instance the file for the Brooklyn bus stop times is ~320MB. Running the script on such a file should work, but will take a long time to execute.
