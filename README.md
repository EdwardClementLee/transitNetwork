transitNetwork
==============

Python script for transforming [GTFS](https://developers.google.com/transit/gtfs/reference) data to node-edge graph data.

This script attempts to transform the transit data from a General Transit Feed Specification (GTFS) folder into a JSON object with nodes as stops and edges as the routes between them.

**Usage**
```
python convert.py <data folder> <output file>
python convert.py ./sample/nyc_gtfs/ ./sample/nyc.json
```