"""Stripper takes the raw JSON data for Reddit submissions and filters it down to only the desired tags."""

import ijson.backends.yajl2 as ijson
import json
import sys
from os import path

def strip(filename, outfile, tags):
    """Take a JSON file and write another JSON file to disk with only the desired tags."""
    try:
        with open(filename) as json_data:
            if not path.isfile("fixed.json"):
                w = open("fixed.json", "w")
                w.write("[")
                for line in json_data:
                    line = line.replace("}\n", "},")
                    w.write(line)
                # seek one back to replace the last comma with a right brace
                w.seek(w.tell()-2, 1)
                w.write("]")
                print("All done fixing the original.")
            else:
                print("Original already found.")
            print("Now to convert!")
            new = open(outfile, "w")
            new.write("[") # make it an array
            for item in ijson.items(open("fixed.json", "rb"), "item"):
                obj = {}
                for tag in tags:
                    try:
                        obj[tag] = item[tag]
                    except KeyError:
                        pass
                        # print(tag, "could not be found.")
                json.dump(obj, new)
                new.write(",")
            new.write("]")

    except:
        print(sys.exc_info()[1])

tags = ["permalink", "ups", "downs", "score", "over_18", "url", "author", "retrieved_on",
        "created", "subreddit_id", "name", "subreddit", "num_comments", "title", "id", "domain"]

strip("RS_2010-08.json", "shortened08.json", tags)
