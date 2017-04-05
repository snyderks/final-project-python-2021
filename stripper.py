"""Stripper takes the raw JSON data for Reddit submissions and filters it down to only the desired tags."""

import ijson
import json
import sys
from os import path

def strip(filename, outfile, tags):
    """Take a JSON file and write another JSON file to disk with only the desired tags."""
    try:
        with open(filename) as json_data:
            if not path.isfile("fixed.json"):
                w = open("fixed.json", "w")
                for line in json_data:
                    line = line.replace("}\n", "},\n")
                    w.write(line)
            new = open(outfile, "w")
            new.write("[") # make it an array
            for item in ijson.items(open("fixed.json", "r"), "item"):
                obj = {}
                for tag in tags:
                    try:
                        obj[tag] = item[tag]
                    except KeyError:
                        pass
                        #print(tag, "could not be found.")
                json.dump(obj, new)
                new.write(",")
            new.write("]")

    except:
        print(sys.exc_info()[0])

tags = ["permalink", "ups", "downs", "score", "over_18", "url", "author", "retrieved_on",
        "created", "subreddit_id", "name", "subreddit", "num_comments", "title", "id", "domain"]

strip("RS_2014-07", "shortened.json", tags)
